# -*- coding: utf-8 -*-
from server.modules.user import User
from server.render.html import default as htmlRender
from server import utils, errors, request, exposed
from server.tasks import callDeferred
from bones import passwordBone

from skeletons.user import userSkel

import logging, json


class user(User):
	viewTemplate = "user_view"
	addTemplate = "user_add"
	addSuccessTemplate = "user_add_success"
	editTemplate = "user_edit"
	editSuccessTemplate = "user_edit_success"

	adminInfo = {
		"name": "Mitglied",
		"handler": "list.user",
		"icon": "icons/modules/users.svg",
		"filter": {"orderby": "lastname"},
		"actions": ["resetpassword"]
	}

	roles = {
		"*": ["view"],
		"executive": ["view", "add", "edit", "delete"]
	}

	def listFilter(self, query):
		if not utils.getCurrentUser():
			query.mergeExternalFilter({
				"contact$gt": 0
			})
			return query

		return super(user, self).listFilter(query)

	def canEdit(self, skel):
		return super(user, self).canView(skel) #All users can edit themself!

	def canView(self, skel):
		user = self.getCurrentUser()
		if user:
			if skel["key"] == user["key"]:
				return True

			if "root" in user["access"]:
				return True

		return False

	def addSkel(self):
		skel = super(user, self).addSkel()
		skel["password"] = utils.generateRandomString(10)
		skel["changepassword"] = True

		'''
		if True:
			skel = skel.ensureIsCloned()

			skel["role"] = "member"
			skel["status"] = 10

			for name, bone in skel.items():
				if name in ["name", "firstname", "lastname"]:
					bone.readOnly = False
					bone.visible = True
				else:
					bone.visible = False
					bone.readOnly = True

			return skel
		'''

		if isinstance(self.render, htmlRender):
			skel = skel.ensureIsCloned()

			skel["role"] = "member"
			skel["status"] = 10

			for name, bone in skel.items():
				if name in ["name", "firstname", "nickname", "lastname", "airbatch_daec", "interests", "duties"]:
					bone.readOnly = False
					bone.visible = True

				else:
					bone.visible = False
					bone.readOnly = True

		return skel

	'''
	def viewSkel(self):
		cuser = utils.getCurrentUser()
		if cuser and "root" in cuser["access"]:
			return super(user, self).viewSkel()

		return super(user, self).viewSkel().subSkel("restricted")
	'''

	@exposed
	def list(self, *args, **kwargs):
		cuser = utils.getCurrentUser()
		if cuser and "root" in cuser["access"]:
			return super(user, self).list(*args, **kwargs)

		# This is a restricted access
		query = self.listFilter(super(user, self).viewSkel().subSkel("restricted").all().mergeExternalFilter(kwargs))
		if query is None:
			raise errors.Unauthorized()

		res = query.fetch()
		return self.render.list(res)

	def editSkel(self):
		skel = super(user, self).editSkel()
		skel.password = passwordBone(descr=u"Passwort", required=False) #scheiss ViUR...

		if isinstance(self.render, htmlRender):
			for name, bone in skel.items():
				if name in ["name", "password", "interests"]:
					bone.readOnly = False
					bone.visible = True
				elif name in []:
					bone.readOnly = True
					bone.visible = True
				else:
					bone.readOnly = True
					bone.visible = False

		return skel

	def onItemAdded(self, skel):
		#if skel["password"]:
		#	self.sendWelcomeMail(str(skel["key"]), skel["password"])

		return super(user, self).onItemAdded(skel)

	@exposed
	def resetPassword(self, key, *args, **kwargs):
		cuser = utils.getCurrentUser()
		if not (cuser and "root" in cuser["access"]):
			raise errors.Unauthorized("Only 'root' can do this!")

		skel = self.editSkel()
		if not skel.fromDB(key):
			raise errors.NotFound()

		skel["password"] = utils.generateRandomString(10)
		skel["changepassword"] = True
		assert skel.toDB()

		self.sendWelcomeMail(str(skel["key"]), skel["password"])
		return json.dumps("OK")

	@callDeferred
	def sendWelcomeMail(self, key, initial):
		skel = self.viewSkel()
		assert skel.fromDB(key)

		skel["password"] = initial

		if request.current.get().isDevServer:
			logging.info("initial = %r", initial)

		utils.sendEMail(
			skel["name"],
			"user_welcome",
			skel
		)

	@exposed
	def view(self, key="self", *args, **kwargs):
		try:
			ret = super(user, self).view(key, *args, **kwargs)
		except errors.Unauthorized:
			if isinstance(self.render, htmlRender):
				raise errors.Redirect("/user/login")

			raise

		return ret

	@exposed
	def login(self, *args, **kwargs):
		if utils.getCurrentUser():
			raise errors.Redirect("/user/view")

		return super(user, self).login(*args, **kwargs)


user.json = True
