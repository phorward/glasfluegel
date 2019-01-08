#-*- coding: utf-8 -*-
from server.skeleton import Skeleton
from server.bones import *

class newsSkel(Skeleton):
	kindName = "news"

	headline = stringBone(descr=u"Überschrift", required=True)
	images = fileBone(descr=u"Bild", multiple=True)
	content = textBone(descr=u"Inhalt", required=True)

	active = booleanBone(descr=u"Aktiv", defaultValue=False, indexed=True)