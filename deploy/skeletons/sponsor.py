#-*- coding: utf-8 -*-
from server.skeleton import Skeleton
from server.bones import *

import sys, time

class sponsorSkel(Skeleton):

	sortindex = numericBone(
		descr="SortIndex",
		indexed=True,
		visible=False,
		readOnly=True,
		mode="float",
		max=sys.maxint
	)

	logo = fileBone(
		descr=u"Logo",
		required=True
	)

	name = stringBone(
		descr=u"Name",
		required=True,
		indexed=True
	)

	link = stringBone(
		descr=u"Link"
	)

	active = booleanBone(
		descr=u"Aktiv",
		defaultValue=True,
		indexed=True
	)

	def preProcessSerializedData(self, dbfields):
		if not ("sortindex" in dbfields and dbfields["sortindex"]):
			dbfields["sortindex"] = time.time()
		return dbfields
