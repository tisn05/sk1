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

from PyQt4 import QtGui

from sk1app import events

class AppMenuBar(QtGui.QMenuBar):
	
	def __init__(self, mw):
		
		QtGui.QMenuBar.__init__(self, mw)
		self.mw = mw
		self.build()
		
	def build(self):
		actions = self.mw.app.actions
		
		#--- FILE ---
		self.file_menu = self.addMenu(self.tr('&File'))
		self.file_menu.addAction(actions['NEW'])
		self.file_menu.addSeparator()
		self.file_menu.addAction(actions['OPEN'])
		self.file_menu.addSeparator()
		self.file_menu.addAction(actions['SAVE'])
		self.file_menu.addAction(actions['SAVE_AS'])
		self.file_menu.addAction(actions['SAVE_ALL'])
		self.file_menu.addSeparator()
		self.file_menu.addAction(actions['CLOSE'])
		self.file_menu.addAction(actions['CLOSE_ALL'])
		self.file_menu.addSeparator()
		self.file_menu.addAction(actions['EXIT'])
		
		
		self.edit_menu = self.addMenu(self.tr('&Edit'))
		self.edit_menu.addAction(actions['UNDO'])
		self.edit_menu.addAction(actions['REDO'])
		self.edit_menu.addAction(actions['CLEAR_HISTORY'])
		self.edit_menu.addSeparator()
		self.edit_menu.addAction(actions['DELETE'])
		self.edit_menu.addAction(actions['CUT'])
		self.edit_menu.addAction(actions['COPY'])
		self.edit_menu.addAction(actions['PASTE'])
		self.edit_menu.addSeparator()
		self.edit_menu.addAction(actions['SELECT_ALL'])
		self.edit_menu.addAction(actions['DESELECT'])
		
		
		self.view_menu = self.addMenu(self.tr('&View'))
		self.view_menu.addAction(actions['ZOOM_100'])		
		self.view_menu.addAction(actions['ZOOM_IN'])		
		self.view_menu.addAction(actions['ZOOM_OUT'])			
		self.view_menu.addAction(actions['ZOOM_PREVIOUS'])
		self.view_menu.addSeparator()
		self.view_menu.addAction(actions['ZOOM_AREA'])					
		self.view_menu.addSeparator()		
		self.view_menu.addAction(actions['ZOOM_PAGE'])		
		self.view_menu.addAction(actions['ZOOM_SELECT'])
		
		
		self.layout_menu = self.addMenu(self.tr('&Layout'))
		self.layout_menu.addAction(actions['DOCK_DocBrowser'])
		
		self.arrange_menu = self.addMenu(self.tr('&Arrange'))
		self.effects_menu = self.addMenu(self.tr('Effe&cts'))
		self.bitmaps_menu = self.addMenu(self.tr('&Bitmaps'))
		self.style_menu = self.addMenu(self.tr('&Style'))
		
		#--- WINDOWS ---
		self.windows_menu = self.addMenu(self.tr('&Window'))
		self.windows_menu_sep = self.create_separator()	
		self.rebuild_window_menu()
		
		self.Settings_menu = self.addMenu(self.tr('Se&ttings'))
		self.help_menu = self.addMenu(self.tr('&Help'))
		self.help_menu.addAction(actions['HELP'])
		self.help_menu.addSeparator()
		self.help_menu.addAction(actions['HOME'])
		self.help_menu.addAction(actions['FORUM'])
		self.help_menu.addAction(actions['BUGS'])
		self.help_menu.addSeparator()
		self.help_menu.addAction(actions['ABOUT'])
		
	def create_separator(self):
		action = QtGui.QAction(self)
		action.setSeparator(True)
		return action
	
	def rebuild_window_menu(self):
		actions = self.mw.app.actions
		
		self.windows_menu.clear()
		self.windows_menu.addAction(actions['CLOSE'])
		self.windows_menu.addAction(actions['CLOSE_ALL'])
		self.windows_menu.addSeparator()
		self.windows_menu.addAction(actions['TABBED'])
		self.windows_menu.addAction(actions['WINDOWED'])
		self.windows_menu.addSeparator()
		self.windows_menu.addAction(actions['TILE'])
		self.windows_menu.addAction(actions['CASCADE'])
		self.windows_menu.addSeparator()
		self.windows_menu.addAction(actions['NEXT'])
		self.windows_menu.addAction(actions['PREVIOUS'])
		
		self.windows_menu.addAction(self.windows_menu_sep)

		windows = self.mw.mdiArea.subWindowList()
		self.windows_menu_sep.setVisible(len(windows) != 0)
		
		actions['TILE'].setEnabled(len(windows) != 0)
		actions['CASCADE'].setEnabled(len(windows) != 0)
		actions['NEXT'].setEnabled(len(windows) != 0)
		actions['PREVIOUS'].setEnabled(len(windows) != 0)		
		
		actions['TABBED'].setChecked(self.mw.app.config.interface_type == 0)
		actions['WINDOWED'].setChecked(self.mw.app.config.interface_type == 1)

		for i, window in enumerate(windows):
			child = window.widget()
			doc=child.presenter
			
			text = "%d %s" % (i + 1, doc.doc_name)
			if doc.doc_file:
				text+='['+doc.doc_file+']'
			if i < 9:
				text = '&' + text

			action = self.windows_menu.addAction(text)
			action.setCheckable(True)
			action.setChecked(child == self.mw.active_child())
			action.triggered.connect(self.mw.windowMapper.map)
			self.mw.windowMapper.setMapping(action, child)

	
