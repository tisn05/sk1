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

from PyQt4 import QtCore

from docbrowser import DocBrowser

class DockManager:
	
	docks = {}
	
	def __init__(self, mw):
		self.mw = mw
		self.app = mw.app
		self.create_docks()
		self.create_actions()
		
	def create_docks(self):
		self.docks['DocBrowser'] = DocBrowser(self.mw)
		self.add_dock(self.docks['DocBrowser'])
		self.docks['DocBrowser'].setVisible(False)
		
	def add_dock(self, dock):
		self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
		
	def create_actions(self):
		actions = self.app.actions	
		actions['DOCK_DocBrowser'] = self.docks['DocBrowser'].toggleViewAction()
		
		
		
	
	
	
	
	