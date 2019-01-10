# -*- coding: utf-8 -*-
from server.prototypes.singleton import Singleton
from server.tasks import callDeferred

from skeletons.reg import regSkel

import logging

class appconf(Singleton):
	adminInfo = {"name": u"Einstellungen",
	             "handler": "singleton",
	             "icon": "icons/modules/settings.svg",
	             "sortIndex": -10
	}

	def canView(self):
		return True

	@callDeferred
	def updateStatistics(self, *args, **kwargs):
		logging.info("Updating statistics in appconf")

		skel = self.getContents()

		skel["total_persons"] = 0
		skel["total_vegetarier"] = 0
		skel["total_aircraft"] = 10

		cursor = None
		while True:
			q = regSkel().all()

			if cursor:
				q.cursor(cursor)

			regs = q.fetch(limit=99)

			for reg in regs:
				skel["total_persons"] += reg["persons"]
				skel["total_vegetarier"] += (reg["vegetarier"] or 0)

				if reg["aircraft"] and not reg["aircraft_ignore"]:
					skel["total_aircraft"] += 1

			if not len(regs):
				break

			cursor = regs.cursor

		logging.info("::: Updating statistics :::")
		logging.info("Total persons count: %d" % skel["total_persons"])
		logging.info("Total vegetarians count: %d" % skel["total_vegetarier"])
		logging.info("Total aircraft count: %d" % skel["total_aircraft"])

		skel.toDB()


appconf.html = True
