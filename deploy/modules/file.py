# -*- coding: utf-8 -*-
from server.modules.file import File
from server import utils, request


class file(File):
	viewTemplate = "file_view"

	roles = {
		"*": ["view"]
	}

	def getAvailableRootNodes(self, *args, **kwargs):
		if utils.getCurrentUser():
			repo = self.ensureOwnModuleRootNode()
			res = [{"name": _(u"Dateien"), "key": str(repo.key())}]
			return res

		return []
