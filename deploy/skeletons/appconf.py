# -*- coding: utf-8 -*-
from server.bones import *
from server.skeleton import Skeleton
from server.config import conf

class appconfSkel(Skeleton):
	kindName = "appconf"

	total_persons = numericBone(descr=u"Anzahl Teilnehmer", defaultValue=0, readOnly=True)
	total_vegetarier = numericBone(descr=u"Anzahl Vegetarier", defaultValue=0, readOnly=True)
	total_aircraft = numericBone(descr=u"Anzahl Flugzeuge", defaultValue=0, readOnly=True)

	for i, sect in enumerate(conf["sections"]):
		catName = "%d - %s" % (i, sect)

		locals()["%s_active" % sect] = booleanBone(
			descr=u"Aktiv", defaultValue=True,
			params={"category": catName}
		)

		locals()["%s_menuname" % sect] = stringBone(
			descr=u"Menüname",
			required=True,
			params={"category": catName}
		)

		locals()["%s_headline" % sect] = stringBone(
			descr=u"Titel",
			required=True,
			params={"category": catName}
		)

		locals()["%s_paralax" % sect] = fileBone(
			descr=u"Paralax",
			params={"category": catName}
		)
