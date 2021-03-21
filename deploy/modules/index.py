# -*- coding: utf-8 -*-
from server import conf, errors, tasks, exposed
from server.render.html import default
import logging

class index(default):

	@exposed
	def index(self, alias="", *args, **kwargs):
		q = conf["viur.mainApp"].page.listFilter(conf["viur.mainApp"].page.viewSkel().all())
		if not q:
			raise errors.NotFound()

		if alias:
			q.filter("alias.idx", alias.lower())

		key = q.run(keysOnly=True, limit=1)
		if not key:
			raise errors.NotFound()

		return conf["viur.mainApp"].page.view(key)


index.html = True
