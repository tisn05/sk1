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

from PyQt4 import QtGui, Qt

from sk1app import events

class DocModifier(QtGui.QPushButton):
	
	def __init__(self, app):
		
		QtGui.QPushButton.__init__(self, 'Modify doc')
		self.app = app
		self.clicked.connect(self.modify)
		
	def modify(self, event):
		if self.app.current_doc:
			print 'emit modification'
			self.app.current_doc.modified()
		
class AppContextBar(QtGui.QToolBar):
	
	def __init__(self, mw):
		
		QtGui.QToolBar.__init__(self, mw.tr('ContextToolBar'), mw)
		self.mw = mw
		self.app = mw.app
		self.build()
		events.connect(events.DOC_CHANGED, self.show_hide)
		events.connect(events.NO_DOCS, self.show_hide)
		
	def build(self):
		self.setAllowedAreas(Qt.Qt.ToolBarAreas(Qt.Qt.TopToolBarArea))
		self.setFloatable(False)
		frame = QtGui.QFrame(self)
		frame.setSizeIncrement(0, 0)
		self.addWidget(frame)
		layout = QtGui.QHBoxLayout()
		layout.setSpacing(2)
		layout.setMargin(0)
		frame.setLayout(layout)
		
		label = QtGui.QLabel('Context Panel')
		layout.addWidget(label)
		
		layout.addWidget(DocModifier(self.app))
		
	def show_hide(self, *args):
		if self.app.inspector.is_doc():
			self.setVisible(True)
		else:
			self.setVisible(False)
