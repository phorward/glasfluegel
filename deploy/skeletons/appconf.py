# -*- coding: utf-8 -*-
from server.bones import *
from server.skeleton import Skeleton

class appconfSkel(Skeleton):
	# Formmailer
	contact_rcpts = emailBone(
		descr=u"Empfänger für Kontaktanfrage",
		params={"category": "Formmailer"},
		required=True
	)
