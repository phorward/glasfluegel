#-*- coding: utf-8 -*-
from server.prototypes import List

class forum(List):

	adminInfo = {
		"name": u"Forum: Kategorie",
		"handler": "list.forum.category",
		"icon": "icons/modules/category.svg",
		"filter": {"orderby": "creationdate", "orderdir": "1"},
		"columns": ["creationdate", "headline"]
	}

	def listFilter(self, filter):
		return filter
