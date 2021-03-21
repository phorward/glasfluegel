#-*- coding: utf-8 -*-
import logging
from server import db, request, skeleton
from server.bones import baseBone


def setSkelForRequest(skelName, key):
	request.current.get().kwargs["@%s" % skelName] = str(key)

def getSkelForRequest(skelName, key = None, attr = None):
	"""
	Retrieves a skeleton with a key and caches it in the current request.
	If no key is given, the function tries to retrieve the key for the requested object
	from the request parameters, by preceding an "@" sign to the skelName as parameter.

	So adding "@project=abc" will try to load a "project"-Skeleton with the key "abc".
	"""
	#print("getSkelForRequest", skelName, key, attr)

	if key is None:
		key = request.current.get().kwargs.get("@%s" % skelName)
		if key is None or not key:
			return None

	reqData = request.current.requestData()

	if "%s.%s" % (skelName, key) in reqData.keys():
		skel = reqData["%s.%s" % (skelName, key)]

		if skel and attr is not None:
			return skel[attr]

		return skel

	skel = skeleton.skeletonByKind(skelName)
	if skel:
		skel = skel()

		if skel.fromDB(key):
			skel = skel.clone()
		else:
			skel = None

	reqData["%s.%s" % (skelName, key)] = skel

	if skel and attr is not None:
		return skel[attr]

	return skel

def mergeSkel(skel, *args):
	ret = skel.clone()

	for idx, skel in enumerate(args):
		assert isinstance(skel, skeleton.BaseSkeleton)

		for boneName in skel.__dataDict__.keys():
			bone = getattr(skel, boneName)

			if bone and isinstance(bone, baseBone):
				destBoneName = "%s.%s" % (skel.kindName, boneName)

				setattr(ret, destBoneName, bone)
				ret[destBoneName] = skel[boneName]

	return ret

def formatString(format, data, structure = None, prefix = None, language = None, _rec = 0):
	"""
	Parses a string given by format and substitutes placeholders using values specified by data.

	The syntax for the placeholders is $(%s).
	Its possible to traverse to sub-dictionarys by using a dot as seperator.
	If data is a list, the result each element from this list applied to the given string; joined by ", ".

	Example:

		data = {"name": "Test","subdict": {"a":"1","b":"2"}}
		formatString = "Name: $(name), subdict.a: $(subdict.a)"

	Result: "Name: Test, subdict.a: 1"

	:param format: String containing the format.
	:type format: str

	:param data: Data applied to the format String
	:type data: list | dict

	:param structure: Parses along the structure of the given skeleton.
	:type structure: dict

	:return: The traversed string with the replaced values.
	:rtype: str
	"""
	if structure and isinstance(structure, list):
		structure = {k:v for k, v in structure}

	prefix = prefix or []

	#logging.debug("%s--- format = %r ---", _rec * " ", format)
	#logging.debug("%sdata      = %r", _rec * " ", data)
	#logging.debug("%sstructure = %r", _rec * " ", structure)
	#logging.debug("%sprefix    = %r", _rec * " ", prefix)
	#logging.debug("%slanguage  = %r", _rec * " ", language)

	res = format

	if isinstance(data,  list):
		return ", ".join([formatString(format, x, structure, prefix, language, _rec = _rec + 1) for x in data])

	elif isinstance(data, (str, unicode)):
		return data

	elif not data:
		return res

	for key, val in data.items():

		# Get structure if available
		struct = structure.get(key) if structure else None
		if isinstance(struct, list):
			struct = {k: v for k, v in struct}

		#logging.debug("%s%s = %r", _rec * " ", key, val)

		if isinstance(val, dict):
			#print("%s%s: dict" % (_rec * " ", key))
			if struct and ("$(%s)" % ".".join(prefix + [key])) in res:
				langs = struct.get("languages")
				if langs:
					if language and language in langs and language in val.keys():
						val = val[language]
					else:
						val = ", ".join(val.values())

				else:
					continue

			else:
				res = formatString(res, val, struct, prefix + [key], language, _rec = _rec + 1)

		elif isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
			if struct and "dest" in val[0] and "rel" in val[0]:
				if "relskel" in struct and "format" in struct:
					format = struct["format"]
					struct = struct["relskel"]

				res = res.replace("$(%s)" % ".".join(prefix + [key]), ", ".join([formatString(format, v, struct, [], language, _rec=_rec + 1) for v in val]))
			else:
				res = formatString(res, val[0], struct, prefix + [key], language, _rec = _rec + 1)

		elif isinstance(val, list):
			val = ", ".join([unicode(v) for v in val])

		# Check for select-bones
		if isinstance(struct, dict) and "values" in struct and struct["values"]:
			vals = struct["values"]

			if isinstance(vals, list):
				vals = {k: v for k, v in vals}

			# NO elif!
			if isinstance(vals, dict):
				if val in vals:
					val = vals[val]

		res = res.replace("$(%s)" % (".".join(prefix + [key])), unicode(val))

	return res

def shortKey(key):
	try:
		return str(db.Key(encoded=key).id_or_name())
	except:
		return key

def getHostUrl():
	url = request.current.get().request.url
	url = url[ :url.find("/", url.find("://")+5) ]

	if not request.current.get().isDevServer and url.startswith("http://"):
		url = "https://" + url[7:]

	return url

def setStatus(key, values=None, check=None, func=None):
	"""
	Universal function to set a status within a transaction.

	:param key: Entity key to change
	:param values: A dict of key-values to update on the entry
	:param check: An optional dict of key-values to check on the entry before
	:param func: A function that is called inside the transaction

	If the function does not raise, all went well.
	"""
	assert isinstance(values, dict), "'values' has to be a dict, you diggi!"

	def transaction():
		obj = db.Get(key)

		if check:
			assert isinstance(check, dict), "'check' has to be a dict, you diggi!"
			assert all([obj[bone] == value for bone, value in check.items()])

		if values:
			for bone, value in values.items():
				if bone[0] == "+":
					obj[bone[1:]] += value
				elif bone[0] == "-":
					obj[bone[1:]] -= value
				else:
					obj[bone] = value

		if func and callable(func):
			func(obj)

		db.Put(obj)

	db.RunInTransaction(transaction)
