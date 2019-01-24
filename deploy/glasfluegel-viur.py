#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#                 iii
#                iii
#               iii
#
#           vvv iii uu      uu rrrrrrrr
#          vvvv iii uu      uu rr     rr
#   v     vvvv  iii uu      uu rr     rr
#  vvv   vvvv   iii uu      uu rr rrrrr
# vvvvv vvvv    iii uu      uu rr rrr
#  vvvvvvvv     iii uu      uu rr  rrr
#   vvvvvv      iii  uu    uu  rr   rrr
#    vvvv       iii   uuuuuu   rr    rrr
#
#   I N F O R M A T I O N    S Y S T E M
# ------------------------------------------------------------------------------
#
# Project:      glasfluegel-viur
# Initiated:    2019-01-07 22:50:17
# Copyright:    neo @ Mausbrand Informationssysteme GmbH
# Author:       neo
#
# ------------------------------------------------------------------------------

from server import conf

# ------------------------------------------------------------------------------
# General configuration
#

conf["viur.forceSSL"] = True
#conf["viur.disableCache"] = True

#conf["viur.exportPassword"] = "de1c3c15b33daaf1486ccbe39fda9f88"
#conf["viur.importPassword"] = "00261bb9ce93268b752c578b0b3fe636"

# ------------------------------------------------------------------------------
# Project configuration
#

conf["sections"] = ["start", "glasfluegel", "news", "ausschreibung", "register", "kontakt"]

# ------------------------------------------------------------------------------
# Language-specific configuration
#

#conf["viur.languageMethod"] = "url"
#conf["viur.availableLanguages"] = ["en", "de"]

# ------------------------------------------------------------------------------
# ViUR admin tool specific configurations
#

conf["admin.vi.name"] = "glasfluegel-viur"
#conf["admin.vi.logo"] = "/static/meta/logo.svg"

# ------------------------------------------------------------------------------
# Content Security Policy
#

conf["viur.security.contentSecurityPolicy"] = {}

# ------------------------------------------------------------------------------
# Bugsnag: Tell us what is wrong!
#

#conf["bugsnag.apiKey" ] = "INSERT YOUR BUGSNAG API KEY HERE"

# ------------------------------------------------------------------------------
# Server startup
#

import server, modules, render

#server.setDefaultLanguage("en") #set default language!
application = server.setup(modules, render)

if __name__ == '__main__':
	server.run()
