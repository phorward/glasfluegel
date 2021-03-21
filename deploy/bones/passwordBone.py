# -*- coding: utf-8 -*-
from server.bones import passwordBone as passwordBone_orig

class passwordBone(passwordBone_orig):
	passwordTests = [
				lambda val: val.lower()!=val, #Do we have upper-case characters?
				lambda val: val.upper()!=val, #Do we have lower-case characters?
				#lambda val: any([x in val for x in "0123456789"]), #Do we have any digits?
				#lambda val: any([x not in (string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in val]), #Special characters?
			]
	passwordTestThreshold = 2

	def fromClient(self, valuesCache, name, data):
		value = data.get(name)
		if not value:
			return _("No value entered")

		if name + "_reenter" in data and value != data[name + "_reenter"]:
			return _("The entered passwords don't match.")

		err = self.isInvalid(value)
		if err:
			return err

		valuesCache[name] = value
