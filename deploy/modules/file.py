# -*- coding: utf-8 -*-
from server.modules.file import File
from server import utils

class file(File):

	def canAdd(self, type, skel):
		return type == "leaf"

	def getAvailableRootNodes(self, name, *args, **kwargs):
		thisuser = utils.getCurrentUser()

		if thisuser:
			repo = self.ensureOwnModuleRootNode()
			res = [{"name": _(u"Shared Files"), "key": str(repo.key())}]
			return res

		return []
