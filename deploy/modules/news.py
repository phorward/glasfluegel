#-*- coding: utf-8 -*-
from server.prototypes import List

class news(List):
	listTemplate = "news_list"

	adminInfo = {
		"name": u"Neuigkeiten",
		"handler": "list",
		"icon": "icons/modules/news.svg",
		"filter": {"orderby": "creationdate", "orderdir": "1"},
		"columns": ["creationdate", "headline"]
	}

	def listFilter(self, filter):
		return filter
