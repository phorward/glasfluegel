#-*- coding: utf-8 -*-
from server.prototypes import List
from server import securitykey, errors, exposed, forceSSL, forcePost

class sponsor(List):

	adminInfo = {
		"name": u"Sponsoren",
		"handler": "list",
		"icon": "icons/modules/cooperation.svg",
		"filter": {"orderby": "sortindex"},
		"columns": ["sortindex", "logo", "name", "link"]
	}

	def listFilter(self, filter):
		return filter

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
		skel.toDB()

		self.onItemEdited(skel)

		return self.render.renderEntry(skel, "setSortIndexSuccess")

