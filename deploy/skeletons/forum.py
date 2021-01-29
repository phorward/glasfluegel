#-*- coding: utf-8 -*-
from server.skeleton import Skeleton
from server.bones import *

class forumSkel(Skeleton):
	subSkels = {
		"*": ["kind", "title", "content", "active"],
		"category": [],
		"topic": ["author"],
		"post": ["author"]
	}

	kind = selectBone(
		descr=u"Typ",
		values=[
			"category",
			"topic",
			"post"
		],
		required=True,
		visible=False,
		readOnly=True,
		indexed=True
	)

	author = userBone(
		descr=u"Autor",
		creationMagic=True,
		readOnly=True,
		indexed=True
	)

	title = stringBone(
		descr=u"Titel",
		required=True
	)

	content = textBone(
		descr=u"Inhalt",
		required=True
	)

	active = booleanBone(
		descr=u"Aktiv",
		defaultValue=False,
		indexed=True
	)
