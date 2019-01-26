# -*- coding: utf-8 -*-
from server.modules.user import User
from server import utils

class user(User):

	def viewSkel(self):
		if utils.getCurrentUser():
			return super(user, self).viewSkel()

		return super(user, self).viewSkel().subSkel("restricted")

	def listFilter(self, filter):
		if not utils.getCurrentUser():
			filter.filter("contact", True)

		return filter
