# -*- coding: utf-8 -*-
from server.prototypes.list import List
from server import bones, conf, utils, errors, securitykey, tasks, exposed
from helpers import setStatus
import datetime, json, logging


class Newsletter(List):
	viewTemplate = "newsletter_view"

	adminInfo = {
		"name": u"Newsletter",
		"handler": "list.place",
		"icon": "icons/modules/newsletter.svg",
		"filter": {"orderby": "creationdate", "orderdir": 1},
		"columns": ["creationdate", "sentdate", "name", "recipients"],
		"preview": "/{{module}}/view/{{key}}",
		"actions": ["newsletter.send"]
	}

	roles = {
		"*": ["view"],
		"executive": ["view", "add", "edit", "delete"]
	}

	@exposed
	def triggerSendNewsletter(self, key, skey, *args, **kwargs):
		if not securitykey.validate(skey):
			raise errors.PreconditionFailed()

		user = utils.getCurrentUser()
		if not (user and "root" in user["access"]):
			raise errors.Unauthorized()

		skel = self.viewSkel()
		if not skel.fromDB(key):
			raise errors.NotFound()

		if skel["triggered"] or skel["sent"]:
			raise errors.Forbidden("This newsletter was already sent.")

		try:
			setStatus(
				skel["key"],
			    values={
					"triggered": True,
					"triggereddate": datetime.datetime.now(),
				},
			    check={
				    "triggered": False,
				    "sent": False
			    })
		except Exception as e:
			logging.exception(e)
			raise errors.Forbidden()

		self.fetchNewsletterRecipients(str(skel["key"]))

		return json.dumps("OKAY")

	@tasks.callDeferred
	def fetchNewsletterRecipients(self, key, cursor=None, total=0, *args, **kwargs):
		skel = self.viewSkel()
		if not skel.fromDB(key):
			logging.error("Newsletter does not exist")
			return

		assert skel["triggered"] and not skel["sent"]

		q = conf["viur.mainApp"].user.viewSkel().all()
		q.filter("interests", skel["recipients"])
		q.cursor(cursor)

		count = 0
		for user in q.run(keysOnly=True):
			self.sendNewsletter(key, str(user))
			count += 1

		if count:
			self.fetchNewsletterRecipients(key, q.getCursor().urlsafe(), total=total + count)
			return

		logging.info("All %d recipients fetched", total)

		setStatus(
			skel["key"],
			values={
				"sent": True,
				"sentdate": datetime.datetime.now(),
				"sentto": total
			}
		)

	@tasks.callDeferred
	def sendNewsletter(self, key, userKey):
		skel = self.viewSkel().clone()
		if not skel.fromDB(key):
			logging.error("Newsletter does not exist")
			return

		userSkel = conf["viur.mainApp"].user.viewSkel()
		if not userSkel.fromDB(userKey):
			logging.error("Cannot find user %r", userKey)
			return

		skel.user = bones.userBone()
		skel.setBoneValue("user", userKey)

		utils.sendEMail(
			userSkel["name"],
			"newsletter",
			skel
		)

		logging.info("Sent newsletter successfully to %r", userSkel["name"])
