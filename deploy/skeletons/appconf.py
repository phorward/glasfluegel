# -*- coding: utf-8 -*-
from server.bones import *
from server.skeleton import Skeleton

class appconfSkel(Skeleton):
	recipients = stringBone(
		descr=u"E-Mail-Empfänger",
		multiple=True,
		required=True
	)
