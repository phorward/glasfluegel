# -*- coding: utf-8 -*-
from server.bones import *
from server.skeleton import Skeleton

class contactSkel(Skeleton):
	key = None

	name = stringBone(
		descr="Dein Name",
		required=True
	)
	email = emailBone(
		descr="Deine E-Mail Adresse",
		required=True
	)
	message = textBone(
		descr="Deine Nachricht",
		required=True,
		validHtml=None
	)

	privacy_confirm = booleanBone(
		descr=u"privacy_confirm", required=True
	)
