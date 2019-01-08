# -*- coding: utf-8 -*-

from server import conf, utils, request
from server.render.html.utils import jinjaGlobalFunction, jinjaGlobalFilter

from server.render import html
from server.render import json
from server.render import vi

# html
# -------------------------------------------------------------------------------------------------

@jinjaGlobalFunction
def getConf(render, key):
	return conf.get(key)

@jinjaGlobalFunction
def prepend(render, obj, s):
	return ["%s%s" % (s, x) for x in iter(obj)]

@jinjaGlobalFunction
def setForRequest(render, key, value):
	request.current.get().kwargs[key] = value

@jinjaGlobalFilter
def isDict(render, val):
	return isinstance(val, dict)

@jinjaGlobalFilter
def isList(render, val):
	return isinstance(val, list)
