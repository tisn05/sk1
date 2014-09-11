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

class AppMainBar(QtGui.QToolBar):
	
	def __init__(self, mw):
		
		QtGui.QToolBar.__init__(self, mw.tr('MainToolBar'), mw)
		self.mw = mw
		self.app = mw.app
		self.build()
		
	def build(self):
		self.setFloatable(False)
		self.setAllowedAreas(Qt.Qt.ToolBarAreas(Qt.Qt.TopToolBarArea))

		self.addAction(self.app.actions['NEW'])
		self.addAction(self.app.actions['OPEN'])
		
		self.insertSeparator(self.app.actions['SAVE'])
				
		self.addAction(self.app.actions['SAVE'])
		self.addAction(self.app.actions['SAVE_AS'])	
		
		self.insertSeparator(self.app.actions['PRINT'])
		
		self.addAction(self.app.actions['PRINT'])	
		
		self.insertSeparator(self.app.actions['CLOSE'])
		
		self.addAction(self.app.actions['CLOSE'])
		
		self.insertSeparator(self.app.actions['UNDO'])
		
		self.addAction(self.app.actions['UNDO'])
		self.addAction(self.app.actions['REDO'])
		
		self.insertSeparator(self.app.actions['CUT'])
		
		self.addAction(self.app.actions['DELETE'])
		self.addAction(self.app.actions['CUT'])
		self.addAction(self.app.actions['COPY'])
		self.addAction(self.app.actions['PASTE'])
		
		self.insertSeparator(self.app.actions['ZOOM_IN'])
		
		self.addAction(self.app.actions['ZOOM_IN'])
		self.addAction(self.app.actions['ZOOM_OUT'])
		self.addAction(self.app.actions['ZOOM_100'])
		self.addAction(self.app.actions['ZOOM_PAGE'])
		self.addAction(self.app.actions['ZOOM_SELECT'])
		
		self.insertSeparator(self.app.actions['CONFIGURE'])
		
		self.addAction(self.app.actions['CONFIGURE'])



	
		