from server.prototypes import List
from skeletons.reg import regSkel
from server import utils, db, errors, securitykey, forceSSL, exposed, request
from server.config import conf
from server.tasks import callDeferred
import logging

class reg(List):
	editSuccessTemplate = "reg_questionaire_thanks"
	listTemplate = "reg_list"
	viewTemplate = "reg_view"

	adminInfo = {"name": u"Anmeldungen",
	             "handler": "list",
	             "icon": "icons/modules/shoutbox.svg",
	             "sortIndex": -20,
				 "filter": {"orderby": "creationdate", "orderdir": "1"},
	             "columns": ["email", "firstname", "lastname", "persons", "visible",
	                            "aircraft_type", "aircraft_reg",
	                                "aircraft_wb", "aircraft_pic", "aircraft_pic_ok"],
	             "actions": ["exportcsv"],
	             "previewurls": {"View": "/{{module}}/questionaire/{{key}}?code={{code}}"}
	}

	def addSkel(self):
		return regSkel.subSkel("regform")

	def canAdd(self):
		return True

	def viewSkel(self):
		return self.regformSkel()

	def canView(self, skel):
		return True

	def onItemAdded(self, skel):
		conf["viur.mainApp"].appconf.updateStatistics()

		if skel["nomail"].value:
			logging.info("No mail to user.")
			return

		utils.sendEMail(skel["email"].value, "reg_add_success", skel, replyTo="info@glasfluegel.net")
		utils.sendEMail("info@glasfluegel.net", "reg_add_success_to_orga", skel, replyTo=skel["email"].value)

	def onItemEdited(self, skel):
		conf["viur.mainApp"].appconf.updateStatistics()

		if not utils.getCurrentUser() and not skel["nomail"].value:
			self.sendQuestionaireEmail(str(skel["key"].value))

	@callDeferred
	def sendQuestionaireEmail(self, key):
		skel = self.regformSkel()
		if not skel.fromDB(key):
			logging.error("Entity not found")
			return

		if skel["nomail"].value:
			logging.info("No mail to user.")
			return

		try:
			utils.sendEMail(skel["email"].value, "reg_questionaire_success",
			                skel, replyTo="info@glasfluegel.net")
		except:
			logging.error("Error sending mail to attendee")

		try:
			utils.sendEMail("info@glasfluegel.net", "reg_questionaire_success_to_orga",
		                    skel, replyTo=skel["email"].value)
		except:
			logging.error("Error sending mail to orga")


	def onItemDeleted(self, skel):
		conf["viur.mainApp"].appconf.updateStatistics()

	def regformSkel(self):
		return regSkel.subSkel("regform")

	def viewSkel(self):
		if utils.getCurrentUser():
			return super(reg, self).viewSkel()

		return regSkel.subSkel("restricted")

	def editSkel(self):
		if utils.getCurrentUser():
			return super(reg, self).editSkel()

		# Restricted skel for the user questionair
		skel = regSkel.subSkel("regform")
		for k, b in skel.items():
			if b.required:
				b.required = False
				b.readOnly = True

		return skel


	def listFilter(self, filter):
		if not utils.getCurrentUser():
			filter.filter("visible", True)

		return filter

	@exposed
	def sendQuestionaires(self, *args, **kwargs):
		if not utils.getCurrentUser():
			raise errors.Unauthorized()

		#q = regSkel().all().filter("questionaire_filled", False)
		q = regSkel().all().filter("questionaire_sent", False)

		count = 0
		txt = ""
		for skel in q.fetch(limit=99):
			#if skel["email"].value == "jmm@phorward.de":
			self.sendQuestionaire(str(skel["key"].value))
			txt += skel["email"].value + "\n"
			count += 1

		return "<html><pre>%s</pre><hr />%d questionaires sent</html>" % (txt, count)

	@callDeferred
	def sendQuestionaire(self, key, *args, **kwargs):
		skel = regSkel()
		if not skel.fromDB(key):
			return

		#if skel["questionaire_filled"].value:
		if skel["questionaire_sent"].value:
			logging.warning("Questionaire already sent!")
			return

		if not skel["nomail"].value:
			try:
					utils.sendEMail(skel["email"].value, "reg_questionaire", skel, replyTo="info@glasfluegel.net")
			except:
				logging.error("Can't send newsletter to attendee")
				return
		else:
			logging.info("Sending mail disabled for user")

		skel["questionaire_sent"].value = True
		skel.toDB()

		logging.info("Newsletter was sent! :)")

	@exposed
	def questionaire(self, *args, **kwargs):
		if "skey" in kwargs:
			skey = kwargs["skey"]
		else:
			skey = ""

		if "key" in kwargs:
			key = kwargs["key"]
		elif len(args) == 1:
			key = args[0]
		else:
			raise errors.NotAcceptable()

		skel = self.editSkel()

		if not skel.fromDB(key):
			raise errors.NotAcceptable()

		# Check for key
		if not utils.getCurrentUser():
			if not ("code" in kwargs.keys() and skel["code"].value == kwargs["code"]):
				raise errors.Unauthorized()

			del kwargs["code"]

		elif not self.canEdit(skel):
			raise errors.Unauthorized()

		err = False
		for k, v in kwargs.items():
			if k in skel.keys() and k not in ["key"]:
				logging.info("Read value '%s' for %s" % (v, k))
				if skel[k].fromClient(k, kwargs) and skel[k].required:
					err = True
					logging.error("Error on reading")

		if (len(kwargs) == 0  # no data supplied
		    or skey == ""  # no security key
			or err
		    or not request.current.get().isPostRequest  # failure if not using POST-method
		    or ("bounce" in list(kwargs.keys()) and kwargs["bounce"] == "1")  # review before changing
		    ):
			# render the skeleton in the version it could as far as it could be read.
			return self.render.edit(skel, tpl="reg_questionaire")

		if not securitykey.validate(skey, acceptSessionKey=True):
			raise errors.PreconditionFailed()

		# Reset the code now!
		skel["code"].value = None
		skel["questionaire_filled"].value = True

		skel.toDB()  # write it!
		self.onItemEdited(skel)

		return self.render.editItemSuccess(skel, tpl="reg_questionaire_thanks")

reg.json = True
reg.jinja2 = True
