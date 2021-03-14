# -*- coding: utf-8 -*-
import html5
from network import NetworkService
from priorityqueue import viewDelegateSelector
from widgets.table import DataTable
from time import time

try:
	from vi_plugins.dynatable import DynaTable
except:
	DynaTable = None


class SortIndexControl(html5.Div):
	def __init__(self, module, data, *args, **kwargs):
		super(SortIndexControl, self).__init__()
		self.addClass("vi-sortindex")

		self.sinkEvent("onClick", "onMouseDown", "onDragStart", "onDragEnd", "onDrop", "onDragOver", "onDragLeave")

		self.module = module
		self.data = data

		#self.appendChild(data["sortindex"])

	def onAttach(self):
		super(SortIndexControl, self).onAttach()

		table = self.getDataTable()

		if table is not None:
			self["draggable"] = True
			self.parent().addClass("vi-sortindex-wrap")

	def getDataTable(self):
		try:
			table = self.parent().parent().parent().parent().parent()
		except:
			table = None

		if table and DynaTable and not (isinstance(table, DataTable) or isinstance(table, DynaTable)):
			table = None

		return table

	def onClick(self, event):
		event.stopPropagation()
		event.preventDefault()

	def onMouseDown(self, event):
		event.stopPropagation()

	def onDragOver(self, event):
		self.addClass("vi-sortindex-can-drop")

		event.preventDefault()
		event.stopPropagation()

	def onDragLeave(self, event):
		self.removeClass("vi-sortindex-can-drop")

		super(SortIndexControl,self).onDragLeave(event)

	def onDragStart(self, event):
		self.addClass("vi-sortindex-is-dragged")

		event.dataTransfer.setData("text/plain", str(self.data["key"]))
		event.stopPropagation()

	def onDragEnd(self, event):
		self.removeClass("vi-sortindex-is-dragged")
		event.stopPropagation()

	def onDrop(self, event):
		self.removeClass("vi-sortindex-can-drop")

		event.stopPropagation()
		event.preventDefault()

		srcKey = event.dataTransfer.getData("text")
		assert srcKey

		if self.data["key"] == srcKey: #Drop on same element!
			return

		table = self.getDataTable()

		if DynaTable and isinstance(table, DynaTable):
			data = table.data
		else:
			data = table._model

		src = srcIdx = None

		for idx, row in enumerate(data):
			if row["key"] == srcKey:
				src = row
				srcIdx = idx
				break

		assert src is not None

		if self.data is data[-1]:
			print("DROP TO LAST", self.data.get("sortindex") or 0)
			sortindex = time() + (self.data.get("sortindex") or 0)
		elif self.data is data[0]:
			print("DROP TO FIRST", (self.data.get("sortindex") or 0))
			sortindex = self.data.get("sortindex") or 0
		else:
			if srcIdx < data.index(self.data):
				idx = -1
			else:
				idx = 1

			print("DROP INSIDE", self.data.get("sortindex") or 0)

			sortindex = (data[data.index(self.data) - idx].get("sortindex") or 0) + (self.data.get("sortindex") or 0)

		print("sortindex", sortindex)

		self.setIndex(sortindex / 2.0, srcKey, data.index(src), data.index(self.data))

	def setIndex(self, index, key, src, dst):
		print("setIndex", key, index)

		req = NetworkService.request(self.module, "setSortIndex",
				                        params={"key": key, "index": str(index)},
				                        successHandler=self.setIndexSuccess,
				                        secure=True,
				                        kickoff=False)
		req.src = src
		req.dst = dst

		req.kickoff()

	def setIndexSuccess(self, req):
		answ = NetworkService.decode(req)

		if answ["action"] == "setSortIndexSuccess":
			table = self.getDataTable()

			if DynaTable and isinstance(table, DynaTable):
				data = table.data
			else:
				data = table._model

			data[req.src]["sortindex"] = float(answ["values"]["sortindex"])

			print("retrieved new sortindex", data[req.src]["sortindex"])

			self.switchRows(req.src, req.dst)

	def switchRows(self, src, dst):
		if src == dst:
			return

		table = self.getDataTable()

		if DynaTable and isinstance(table, DynaTable):
			table.reload()
			return

		#print("src = %d" % src)
		#print("dst = %d" % dst)

		srcTr = table.table.getTrByIndex(src)
		dstTr = table.table.getTrByIndex(dst)

		assert srcTr and dstTr

		#print(srcTr, dstTr)
		data = table._model
		entry = data[src]

		if src < dst:
			dstTr = table.table.getTrByIndex(dst + 1)
			if dstTr is None:
				table.table.body.appendChild(srcTr)

				data.remove(entry)
				data.append(entry)

			else:
				table.table.body.insertBefore(srcTr, dstTr)

				data.remove(entry)
				data.insert(dst + 1, entry)

		else:
			table.table.body.insertBefore(srcTr, dstTr)

			data.remove(entry)
			data.insert(dst, entry)


class SortIndexViewBoneDelegate(object):
	def __init__(self, moduleName, boneName, skelStructure, *args, **kwargs):
		super(SortIndexViewBoneDelegate, self).__init__()
		self.skelStructure = skelStructure
		self.boneName = boneName
		self.moduleName = moduleName

	def render(self, data, field):
		return SortIndexControl(self.moduleName, data)

	@staticmethod
	def checkFor(moduleName, boneName, skelStucture, *args, **kwargs):
		return boneName == "sortindex"

viewDelegateSelector.insert(5, SortIndexViewBoneDelegate.checkFor, SortIndexViewBoneDelegate)
