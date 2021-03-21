# -*- coding: utf-8 -*-
from server.bones import userBone as userBone_orig

class userBone(userBone_orig):
	def __init__(self, format="$(dest.firstname) $(dest.lastname)", refKeys=["key", "name", "lastname", "firstname"],
	                *args, **kwargs):
		super(userBone, self).__init__(format=format, refKeys=refKeys, *args, **kwargs)
