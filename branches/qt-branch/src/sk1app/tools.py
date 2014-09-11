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

from sk1app import events
from actions import AppAction
from utils.color import qt_lighter_color, qt_middle_color
from sk1app import modes

TOOL_SIZE = 26

class AppToolAction(QtGui.QAction):
	
	def __init__(self, icon, text, obj, method, shortcut, mode):
		
		QtGui.QAction.__init__(self, icon, text, obj)

		if shortcut:
			self.setShortcut(shortcut)
			
		self.method = method
		self.mode = mode
		self.setCheckable(True)		
		obj.connect(self, QtCore.SIGNAL('triggered()'), method)
		
class ToolsTitleWidget(QtGui.QWidget):
	
	def __init__(self, dock):
		
		QtGui.QWidget.__init__(self)
		
		self.dock = dock
		self.setMinimumSize(10, 10)
		self.policy = QtGui.QSizePolicy()
		self.policy.setVerticalPolicy(QtGui.QSizePolicy.Fixed)
		self.policy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
		
		linearGradient = QtGui.QLinearGradient(0, 0, 0, 10)
		linearGradient.setColorAt(0.0, qt_lighter_color(self.palette().background().color(), 0.95))
		linearGradient.setColorAt(1.0, self.palette().background().color())
		self.brush = QtGui.QBrush(linearGradient)
		self.line_color = qt_middle_color(self.palette().mid().color(), self.palette().background().color(), 0.5)
		
	def sizeHint(self):
		return Qt.QSize(20, 13)
	
	def minimumSizeHint(self):
		return Qt.QSize(20, 13)		
	
	def paintEvent(self, *args):		
		painter = QtGui.QPainter(self)
		painter.save()
		painter.fillRect(0, 3, self.width() - 1, self.height() - 1, self.brush)
		painter.setPen(self.line_color)
		painter.drawLine(0, self.height() - 1, self.width() - 1, self.height() - 1)
		painter.restore()

class skTools(QtGui.QDockWidget):
	
	actions = {}
	
	main_tools_layout = None
	
	def __init__(self, mw):
		
		QtGui.QDockWidget.__init__(self, mw.tr(''), mw)
		self.mw = mw
		self.app = mw.app
		self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
		self.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
		self.policy = QtGui.QSizePolicy()
		self.policy.setVerticalPolicy(QtGui.QSizePolicy.Fixed)
		self.policy.setHorizontalPolicy(QtGui.QSizePolicy.Fixed)
		self.layout().setAlignment(Qt.Qt.AlignTop)
		self.setContentsMargins(2, 0, 0, 0)
		self.setTitleBarWidget(ToolsTitleWidget(self))
		
		self.action_group = QtGui.QActionGroup(self)
		self.build()
		events.connect(events.DOC_CHANGED, self.show_hide)
		events.connect(events.NO_DOCS, self.show_hide)
		
	def tools_action(self):
		mode = None
		for action in self.actions.keys():
			if not self.actions[action].mode is None:
				if self.actions[action].isChecked():
					mode = self.actions[action].mode
					break
		if not mode is None:
			if not self.app.current_doc is None:
				self.app.current_doc.view.set_mode(mode)
			
	def check_mode(self):
		if not self.app.current_doc is None:
			mode = self.app.current_doc.view.mode
			for action in self.actions.keys():
				if not self.actions[action].mode is None:
					if mode == self.actions[action].mode:
						if not self.actions[action].isChecked():
							self.actions[action].setChecked(True)
							break
	
	def outline_action(self):
#		print 'works!'		
		pass	
	
	def fill_action(self):
#		print 'works!'		
		pass
		
	def build(self):
				
		self.setContentsMargins(0, 0, 0, 0)
		
		self.tools_frame = QtGui.QFrame()
		self.tools_frame.setSizePolicy(self.policy)
		self.tools_frame_layout = QtGui.QVBoxLayout()
		self.tools_frame_layout.setAlignment(Qt.Qt.AlignTop)
		self.tools_frame_layout.setContentsMargins(1, 3, 0, 0)
		
		self.main_tools = QtGui.QFrame()
		self.main_tools.setSizePolicy(self.policy)
		self.main_tools.setContentsMargins(0, 0, 0, 0)
		self.main_tools_layout = QtGui.QGridLayout()
		self.main_tools_layout.setAlignment(Qt.Qt.AlignTop)
		self.main_tools_layout.setSpacing(0)
		self.main_tools_layout.setContentsMargins(0, 0, 0, 0)
		
		self.actions['SELECT'] = AppToolAction(
					QtGui.QIcon(':/tools/tools_pointer.png'), 
					self.tr('Selection Mode'), self, self.tools_action, 
					'', modes.SELECT_MODE)
		self.add_tool(self.actions['SELECT'], 0, 0)

		self.actions['EDIT'] = AppToolAction(
					QtGui.QIcon(':/tools/tools_shaper.png'), 
					self.tr('Edit Mode'), self, self.tools_action, 
					'', modes.SHARPER_MODE)
		self.add_tool(self.actions['EDIT'], 1, 0)
		
		self.actions['FLEUR'] = AppToolAction(
					QtGui.QIcon(':/tools/tools_fleur.png'), 
					self.tr('Move Canvas'), self, self.tools_action, 
					'', modes.FLEUR_MODE)
		self.add_tool(self.actions['FLEUR'], 2, 0)

		self.actions['ZOOM'] = AppToolAction(
					QtGui.QIcon(':/tools/tools_zoom.png'), 
					self.tr('Zoom Area'), self, self.tools_action, 
					'', modes.ZOOM_MODE)
		self.add_tool(self.actions['ZOOM'], 3, 0)	
		
		self.actions['LINE'] = AppToolAction(
					QtGui.QIcon(':/tools/tools_pencil_line.png'), 
					self.tr('Draw Poly-Line'), self, self.tools_action, 
					'', modes.LINE_MODE)
		self.add_tool(self.actions['LINE'], 4, 0)	
		
		self.actions['CURVE'] = AppToolAction(
					QtGui.QIcon(':/tools/tools_pencil_curve.png'), 
					self.tr('Draw Curve'), self, self.tools_action, 
					'', modes.CURVE_MODE)
		self.add_tool(self.actions['CURVE'], 5, 0)	
		
		self.actions['ELLIPSE'] = AppToolAction(
					QtGui.QIcon(':/tools/tools_ellipse.png'),
					self.tr('Draw Ellipse'), self, self.tools_action, 
					'', modes.ELLIPSE_MODE)
		self.add_tool(self.actions['ELLIPSE'], 6, 0)	
		
		self.actions['RECT'] = AppToolAction(
					QtGui.QIcon(':/tools/tools_rectangle.png'), 
					self.tr('Draw Rectangle'), self, self.tools_action, 
					'', modes.RECT_MODE)
		self.add_tool(self.actions['RECT'], 7, 0)	
		
		self.actions['POLYGON'] = AppToolAction(
					QtGui.QIcon(':/tools/tools_polygon.png'), 
					self.tr('Draw Polygon'), self, self.tools_action, 
					'', modes.POLYGON_MODE)
		self.add_tool(self.actions['POLYGON'], 8, 0)	
		
		self.actions['TEXT'] = AppToolAction(
					QtGui.QIcon(':/tools/tools_text.png'), 
					self.tr('Draw Text'), self, self.tools_action, 
					'', modes.TEXT_MODE)
		self.add_tool(self.actions['TEXT'], 9, 0)
		

		self.toolbuttons_frame = QtGui.QFrame()
		self.toolbuttons_frame.setSizePolicy(self.policy)
		self.toolbuttons_frame_layout = QtGui.QGridLayout()
		self.toolbuttons_frame_layout.setAlignment(Qt.Qt.AlignTop)
		self.toolbuttons_frame_layout.setContentsMargins(0, 0, 0, 0)
		self.toolbuttons_frame_layout.setSpacing(0)
	
		self.actions['OUTLINE'] = AppAction(QtGui.QIcon(':/tools/tools_color_line.png'), 
										self.tr('Outline...'), self, self.outline_action, '', None)
		tool_button = QtGui.QToolButton(self)
		tool_button.setDefaultAction(self.actions['OUTLINE'])
		tool_button.setCheckable(False)
		tool_button.setIconSize(Qt.QSize(TOOL_SIZE, TOOL_SIZE))
		tool_button.setAutoRaise(True)
		self.toolbuttons_frame_layout.addWidget(tool_button, 0, 0)

		self.actions['FILL'] = AppAction(QtGui.QIcon(':/tools/tools_color_fill.png'), 
										self.tr('Fill...'), self, self.fill_action, '', None)
		tool_button = QtGui.QToolButton(self)
		tool_button.setDefaultAction(self.actions['FILL'])
		tool_button.setCheckable(False)
		tool_button.setIconSize(Qt.QSize(TOOL_SIZE, TOOL_SIZE))
		tool_button.setAutoRaise(True)
		self.toolbuttons_frame_layout.addWidget(tool_button, 1, 0)

		self.main_tools.setLayout(self.main_tools_layout)
		self.toolbuttons_frame.setLayout(self.toolbuttons_frame_layout)

		self.tools_frame_layout.addWidget(self.main_tools)
		self.add_line()
		self.tools_frame_layout.addWidget(self.toolbuttons_frame)
		self.add_line()
		
		self.tools_frame.setLayout(self.tools_frame_layout)
		
		self.setWidget(self.tools_frame)
		self.setContextMenuPolicy(Qt.Qt.PreventContextMenu)
		
	def add_line(self):
		line = QtGui.QFrame()
		line.setFrameShape(QtGui.QFrame.HLine)
		line.setFrameShadow(QtGui.QFrame.Sunken)
		self.tools_frame_layout.addWidget(line)
		
	def add_tool(self, action, row, column):
		self.action_group.addAction(action)	
		tool_button = QtGui.QToolButton(self)
		tool_button.setDefaultAction(action)
		tool_button.setIconSize(Qt.QSize(TOOL_SIZE, TOOL_SIZE))
		tool_button.setAutoRaise(True)
		self.main_tools_layout.addWidget(tool_button, row, column)
		
	def show_hide(self, *args):
		if self.app.inspector.is_doc():
			self.setVisible(True)
			self.check_mode()
		else:
			self.setVisible(False)		
