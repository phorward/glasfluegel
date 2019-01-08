# -*- coding: utf-8 -*-
from server.modules.formmailer import Formmailer
from skeletons.contact import contactSkel
from server import exposed, utils, securitykey, errors
from server.bones import baseBone

class contact(Formmailer):
	mailSkel = contactSkel
	mailTemplate = "contact"

	def canUse( self ):
		return True
	
	def getRcpts( self,  skel ):
		return [ "info@glasfluegel.net" ]

	@exposed
	def index( self, *args, **kwargs ):
		if not self.canUse():
			raise errors.HTTPError(401) #Unauthorized

		skel = self.mailSkel()

		if len( kwargs ) == 0:
			return self.render.add( skel=skel, failed=False)

		if not skel.fromClient( kwargs ) or not "skey" in kwargs.keys():
			return self.render.add(  skel=skel, failed=True )

		if not securitykey.validate( kwargs["skey"] ):
			raise errors.PreconditionFailed()

		# Allow bones to perform outstanding "magic" operations before sending the mail
		for key, _bone in skel.items():
			if isinstance(_bone, baseBone):
				_bone.performMagic(isAdd=True)

		rcpts = self.getRcpts(skel)
		#utils.sendEMail(rcpts, self.mailTemplate, skel, replyTo=skel["email"])
		utils.sendEMail(rcpts, self.mailTemplate, skel)
		self.onItemAdded(skel)

		return self.render.addItemSuccess( skel )

contact.json=True
contact.internalExposed = True
