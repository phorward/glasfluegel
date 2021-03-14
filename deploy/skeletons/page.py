# -*- coding: utf-8 -*-
import sys
from server.bones import *
from server.skeleton import Skeleton, RelSkel


class pageSkel(Skeleton):
	sortindex = numericBone(
		descr="SortIndex",
		indexed=True,
		visible=False,
		readOnly=True,
		mode="float",
		max=sys.maxint
	)

	online = booleanBone(
		descr=u"Aktiv",
		indexed=True,
		defaultValue=True
	)

	alias = stringBone(
		descr=u"Alias",
		required=True,
		caseSensitive=False,
		indexed=True,
		unique=u"Name muss eindeutig sein!"
	)

	name = stringBone(
		descr=u"Name im Menü",
		required=True
	)

	static = booleanBone(
		descr=u"Statisches Template 'content-<alias>.html' verwenden",
		defaultValue=False
	)

	title = stringBone(
		descr=u"Titel",
		params={
			"logic.visibleIf": "not static"
		}
	)

	content = textBone(
		descr=u"Inhalt",
		params={
			"logic.visibleIf": "not static"
		}
	)

	parallax = fileBone(
		descr=u"Parallax",
		params={
			"logic.visibleIf": "not static"
		}
	)
