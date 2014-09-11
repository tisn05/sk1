# -*- coding: utf-8 -*-
#
#	Copyright (C) 2011 by Igor E. Novikov
#	
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#	
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#	
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtGui, Qt, QtCore

from uc2.sk1doc import model
from sk1app import events

from dock import AbstractDock 



class DocBrowser(AbstractDock):
	
	def __init__(self, mw):
		AbstractDock.__init__(self, mw.tr('DOM Model'), mw)
		
		self.mw = mw
		self.app = mw.app
		
		self.model=QtGui.QStandardItemModel()
		self.view = QtGui.QTreeView(self)		
		self.setContentsMargins(0, 0, 0, 0)
		self.setWidget(self.view)
		self.view.setModel(self.model)
		events.connect(events.DOC_CHANGED, self.start)
		events.connect(events.NO_DOCS, self.start)
		events.connect(events.DOC_MODIFIED, self.start)
		
		self.node_icon = self.style().standardIcon(QtGui.QStyle.SP_DirIcon)
		self.leaf_icon = self.style().standardIcon(QtGui.QStyle.SP_FileIcon)
		
		self.start()
		
	def start(self, *args):
		if not self.app.current_doc is None:
			self.view.setEnabled(True)
			self.set_model()
			self.view.expandToDepth(2)
		else:
			self.set_fake_model()
			self.view.setEnabled(False)
			
	def set_fake_model(self):		
		self.model.clear()		
		self.model.setHorizontalHeaderLabels(QtCore.QStringList('Objects'))
		self.model.invisibleRootItem().appendRow(QtGui.QStandardItem("No document"))
					
	def set_model(self):
		self.model.clear()		
		self.model.setHorizontalHeaderLabels(QtCore.QStringList('Objects'))
		self.make_data()
		
	def make_data(self):
		self.rootItem = self.model.invisibleRootItem()
		self.parent = self.rootItem
		doc = self.app.current_doc.model
		self.build_tree(doc)
		
	def build_tree(self, item):
		if item.cid > model.PRIMITIVE_CLASS:
			icon = self.leaf_icon
		else:
			icon = self.node_icon
		point = QtGui.QStandardItem(icon, model.CID_TO_NAME[item.cid])
		self.parent.appendRow(point)
		old_parent = self.parent
		self.parent = point
		for child in item.childs:
			self.build_tree(child)
		self.parent = old_parent
			
