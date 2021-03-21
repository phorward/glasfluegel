# -*- coding: utf-8 -*-
from server.skeleton import Skeleton
from server.bones import *
from server import conf


class newsletter(Skeleton):

	triggered = booleanBone(
		descr=u"Versand angestoßen",
		defaultValue=False,
		indexed=True,
		readOnly=True,
		visible=False
	)

	triggereddate = dateBone(
		descr=u"Versand angestoßen am",
		indexed=True,
		readOnly=True,
		visible=False
	)

	sent = booleanBone(
		descr=u"Verschickt",
		defaultValue=False,
		indexed=True,
		readOnly=True,
		visible=False,
	)

	sentdate = dateBone(
		descr=u"Verschickt am",
		indexed=True,
		readOnly=True
	)

	sentto = numericBone(
		descr=u"Verschickt an",
		readOnly=True,
		visible=False
	)

	name = stringBone(
		descr=u"Titel",
		required=True,
		searchable=True,
		indexed=True
	)

	content = textBone(
		descr=u"Inhalt",
		required=True,
		searchable=True,
		params={
			"tooltip": u"Bitte keine Ansprache verwenden, diese wird automatisch generiert!"
		}
	)

	'''
	appointment = relationalBone(
		kind="appointment",
		module="appointment",
		descr=u"Termin",
		indexed=True
	)

	recipients = selectBone(
		descr=u"Zielgruppe",
		required=True,
		multiple=True,
		defaultValue=["newsletter"],
		sortBy="values",
		values=conf["project.user.interests"],
		params={
			"tooltip": u"Auswahl von Zielgruppen. Bitte diese mit Bedacht wählen!"
		}
	)
	'''
