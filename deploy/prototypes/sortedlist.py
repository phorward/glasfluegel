#-*- coding: utf-8 -*-
from server.prototypes.list import List
from server import securitykey, errors
from server import exposed, forcePost, forceSSL


class SortedList(List):

	def listFilter(self, query):
		query = super(SortedList, self).listFilter(query)

		if query and not query.getOrders():
			query.order("sortindex")

		return query

	@forceSSL
	@forcePost
	@exposed
	def setSortIndex(self, key, index, skey, *args, **kwargs):
		if not securitykey.validate(skey, acceptSessionKey=True):
			raise errors.PreconditionFailed()

		skel = self.editSkel()
		if not skel.fromDB(key):
			raise errors.NotFound()

		skel["sortindex"] = float(index)
		skel.toDB(clearUpdateTag=True)
		return self.render.renderEntry(skel, "setSortIndexSuccess")

