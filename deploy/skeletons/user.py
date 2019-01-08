# -*- coding: utf-8 -*-
from server.modules.user import userSkel
from server.bones import *
from server import conf

class userSkel(userSkel):
	subSkels = {"restricted": ["key", "contact", "photo", "display_name", "tasks", "sortindex"]}

	contact = booleanBone(descr=u"Kontaktperson", indexed=True)
	photo = fileBone(descr=u"Foto")
	display_name = stringBone(descr=u"Anzeigename", indexed=True)
	tasks = stringBone(descr=u"Aufgaben")

	sortindex = numericBone(descr=u"Sortierreihenfole", indexed=True)
