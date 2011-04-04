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

from PyQt4 import Qt, QtGui, QtCore

import dialogs
from sk1app import events
from sk1app.docks import DockManager
from menubar import AppMenuBar
from maintoolbar import AppMainBar
from ctxtoolbar import AppContextBar
from tools import skTools
from palette import PaletteBar
from statusbar import AppStatusBar
from utils.color import qt_middle_color

class MainWindow(QtGui.QMainWindow):
	"""
	The class represents main application window.
	
	app - sK1 Application class instance 
	"""
	
	mdiArea = None
	
	def __init__(self, app):
		
		super(MainWindow, self).__init__()
			
		self.app = app
		self.set_title()
		
		self.mdiArea = QtGui.QMdiArea()
		self.setCentralWidget(self.mdiArea)
		self.mdiArea.setDocumentMode(True)
		clr = qt_middle_color(self.palette().text().color(), self.palette().background().color(), 0.4)
		self.mdiArea.setBackground(Qt.QBrush(clr))
		
		self.windowMapper = QtCore.QSignalMapper(self)
		self.windowMapper.mapped[QtGui.QWidget].connect(self.set_active_child)
		self.mdiArea.subWindowActivated.connect(self.child_activated)
		
		self.docks = DockManager(self)
		
		self.create_actions()
		
		self.menubar = AppMenuBar(self)
		self.setMenuBar(self.menubar)
		
		self.maintoolbar = AppMainBar(self)
		self.addToolBar(self.maintoolbar)		
		
#		self.contextbar = AppContextBar(self)
#		self.addToolBar(self.contextbar)
#		self.insertToolBarBreak(self.contextbar)
		
		self.tools = skTools(self)
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.tools)
		
		self.palette = PaletteBar(self)
		if self.app.config.palette_orientation == Qt.Qt.Horizontal:
			self.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.BottomToolBarArea), self.palette)
		else:
			self.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.RightToolBarArea), self.palette)
		
		self.statusbar = AppStatusBar(self)
		self.setStatusBar(self.statusbar)
		
		self.setMinimumSize(self.app.config.mw_min_width, self.app.config.mw_min_height)
		self.resize(self.app.config.mw_width, self.app.config.mw_height)
		
		if self.app.config.mw_maximized: self.setWindowState(Qt.Qt.WindowMaximized)
			
		self.setWindowIcon(self.app.appdata.app_icon)
		
		if self.app.config.interface_type:
			self.set_windowed_interface()
		else:
			self.set_tab_interface()
			
		screen = QtGui.QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 3)
		
			
		self.setUnifiedTitleAndToolBarOnMac(True)
		
		
	def create_actions(self):
		
		actions = self.app.actions
		

		actions['TABBED'] = QtGui.QAction("Tabbed View", self,
				statusTip="Tabbed document interface",
				triggered=self.set_tab_interface)
		
		actions['TABBED'].setCheckable(True)

		actions['WINDOWED'] = QtGui.QAction("SubWindow View", self,
				statusTip="Windowed document interface",
				triggered=self.set_windowed_interface)
		
		actions['WINDOWED'].setCheckable(True)

		actions['TILE'] = QtGui.QAction("&Tile", self,
				statusTip="Tile the windows",
				triggered=self.set_tiled_windows)

		actions['CASCADE'] = QtGui.QAction("&Cascade", self,
				statusTip="Cascade the windows",
				triggered=self.set_cascade_windows)

		actions['NEXT'] = QtGui.QAction("Ne&xt document", self,
				shortcut=QtGui.QKeySequence.NextChild,
				statusTip="Move the focus to the next document",
				triggered=self.next_child)

		actions['PREVIOUS'] = QtGui.QAction("Pre&vious document", self,
				shortcut=QtGui.QKeySequence.PreviousChild,
				statusTip="Move the focus to the previous document",
				triggered=self.mdiArea.activatePreviousSubWindow)

		actions['HELP'] = QtGui.QAction(self.app.generic_icons['HELP'],"&Help", self,
				statusTip="Help",
				triggered=self.help)
		actions['HELP'].setShortcut('F1')

		actions['HOME'] = QtGui.QAction(self.app.generic_icons['HOME'],"&Project web site", self,
				statusTip="Project web site",
				triggered=self.home)

		actions['FORUM'] = QtGui.QAction("Project &forum", self,
				statusTip="Project forum",
				triggered=self.forum)

		actions['BUGS'] = QtGui.QAction("&Report bug", self,
				statusTip="Project forum",
				triggered=self.bugs)

		actions['ABOUT'] = QtGui.QAction(self.app.appdata.app_icon,"&About sK1", self,
				statusTip="About sK1",
				triggered=self.about)

		actions['ABOUT_QT'] = QtGui.QAction("About &Qt", self,
				statusTip="Show the Qt library's About box",
				triggered=QtGui.qApp.aboutQt)
		
	def set_tab_interface(self):
		self.mdiArea.setViewMode(QtGui.QMdiArea.TabbedView)		
		self.app.config.interface_type = 0
		self.menubar.rebuild_window_menu()
		self._init_tabbar()
		
	def _init_tabbar(self):
		tabbar = self.mdiArea.findChild(QtGui.QTabBar)
		if tabbar:
			tabbar.setExpanding(False)
			tabbar.setMovable(True)
			tabbar.setTabsClosable(True)
			tabbar.tabCloseRequested.connect(self.tab_close_requested)
			tabbar.setContextMenuPolicy(Qt.Qt.PreventContextMenu)
	
	def set_windowed_interface(self):
		self.mdiArea.setViewMode(QtGui.QMdiArea.SubWindowView)
		self.app.config.interface_type = 1
		if self.active_child():
			self.active_child().showMaximized()
		self.menubar.rebuild_window_menu()
		
	def active_child(self):
		if self.mdiArea:
			activeSubWindow = self.mdiArea.activeSubWindow()
			if activeSubWindow:
				return activeSubWindow.widget()
		return None
	
	def set_tiled_windows(self):
		self.set_windowed_interface()		
		self.mdiArea.tileSubWindows()
	
	def set_cascade_windows(self):
		self.set_windowed_interface()
		self.mdiArea.cascadeSubWindows()
		
	def set_active_child(self, window):
		if window:
			self.mdiArea.setActiveSubWindow(window.parent())			
			
	def child_activated(self, window):
		if window:
			for doc in self.app.docs:
				if doc.subwindow == window:
					self.app.set_current_doc(doc)
					self.set_title()
			self.menubar.rebuild_window_menu()
			
	def next_child(self):
		self.mdiArea.activateNextSubWindow()
	
	def previous_child(self):
		self.mdiArea.activatePreviousSubWindow()
		
	def closeEvent(self, event):		
		if self.app.close_all():
			self.app.app_exit()
		else:
			event.ignore()
			
	def tab_close_requested(self, tabnum=0):
		tabbar = self.mdiArea.findChild(QtGui.QTabBar)
		if tabbar:
			tabbar.setCurrentIndex(tabnum)
			self.app.close()
			
	def set_title(self):
		app_name = self.app.appdata.app_name
		self.setWindowTitle(app_name)

	def help(self):
		path = 'http://sk1project.org/modules.php?name=Products&product=sk1'
		QtGui.QDesktopServices.openUrl(Qt.QUrl(path, Qt.QUrl.StrictMode));
	
	def home(self):
		path = 'http://sk1project.org/'
		QtGui.QDesktopServices.openUrl(Qt.QUrl(path, Qt.QUrl.StrictMode));
	
	def forum(self):
		path = 'http://sk1project.org/forum/'
		QtGui.QDesktopServices.openUrl(Qt.QUrl(path, Qt.QUrl.StrictMode));
	
	def bugs(self):
		path = 'http://sk1project.org/forum/viewforum.php?forum_id=4'
		QtGui.QDesktopServices.openUrl(Qt.QUrl(path, Qt.QUrl.StrictMode));
					
	def about(self):
		dialogs.show_about_dialog(self)
		


	
