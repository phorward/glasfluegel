# -*- coding: utf-8 -*-
from server import conf
from server.modules.formmailer import Formmailer
from skeletons.contact import contactSkel

class Contact(Formmailer):
	mailTemplate = "contact"

	def canUse(self):
		return True

	def getRcpts(self,  skel):
		appconf = conf["viur.mainApp"].appconf.getContents()
		assert appconf and appconf["contact_rcpts"]

		return appconf["contact_rcpts"]

	def mailSkel(self):
		return contactSkel()

	def getOptions(self, skel):
		return {
			"replyTo": skel["email"]
		}

Contact.html = True
Contact.json = True
