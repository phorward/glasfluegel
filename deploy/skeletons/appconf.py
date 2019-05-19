# -*- coding: utf-8 -*-
from server.bones import *
from server.skeleton import Skeleton
from server.config import conf

class appconfSkel(Skeleton):

	recipients = stringBone(
		descr=u"E-Mail-Empfänger",
		multiple=True,
		required=True
	)

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
			defaultValue=sect,
			params={"category": catName}
		)

		locals()["%s_headline" % sect] = stringBone(
			descr=u"Titel",
			required=True,
			defaultValue=sect,
			params={"category": catName}
		)

		locals()["%s_paralax" % sect] = fileBone(
			descr=u"Paralax",
			params={"category": catName}
		)

		locals()["%s_static" % sect] = booleanBone(
			descr=u"Statische Seite 'content-%s.html' benutzen" % sect,
			defaultValue=True,
			params={"category": catName}
		)

		locals()["%s_content" % sect] = textBone(
			descr=u"Inhalt",
			params={
				"category": catName,
				"logic.visibleIf": "not %s_static" % sect}
		)
