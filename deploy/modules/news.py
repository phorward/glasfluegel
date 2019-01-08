#-*- coding: utf-8 -*-
from server.prototypes import List

class news(List):

	adminInfo = {"name": u"Neuigkeiten",
	             "handler": "list",
	             "icon": "icons/modules/news.svg",
	             "sortIndex": -15,
				 "filter": {"orderby": "creationdate", "orderdir": "1"},
	             "columns": ["creationdate", "headline"]
	}

	def listFilter(self, filter):
		return filter
