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
from actions import AppAction
from widgets import palette_widget

class PaletteBar(QtGui.QToolBar):

	actions = {}
	palwidget = None

	def __init__(self, mw):

		QtGui.QToolBar.__init__(self, mw.tr('PaletteBar'), mw)
		self.mw = mw
		self.app = mw.app
		self.cur_orient = Qt.Qt.Horizontal

		self.setAllowedAreas(Qt.Qt.ToolBarAreas(Qt.Qt.BottomToolBarArea +
											Qt.Qt.RightToolBarArea))
		self.setIconSize(Qt.QSize(12, 12))
		self.setMinimumSize(26, 26)
		self.setFloatable(False)
		self.h_icons = [
					QtGui.QIcon(':/palette/double-arrow-left.png'),
					QtGui.QIcon(':/palette/arrow-left.png'),
					QtGui.QIcon(':/palette/arrow-right.png'),
					QtGui.QIcon(':/palette/double-arrow-right.png')
					]
		self.v_icons = [
					QtGui.QIcon(':/palette/double-arrow-top.png'),
					QtGui.QIcon(':/palette/arrow-top.png'),
					QtGui.QIcon(':/palette/arrow-bottom.png'),
					QtGui.QIcon(':/palette/double-arrow-bottom.png')
					]
		self.build()

	def check_orientation(self):
		if not self.orientation() == self.cur_orient:
			if self.orientation() == Qt.Qt.Horizontal:
				self.actions['DBACK'].setIcon(self.h_icons[0])
				self.actions['BACK'].setIcon(self.h_icons[1])
				self.actions['FORWARD'].setIcon(self.h_icons[2])
				self.actions['DFORWARD'].setIcon(self.h_icons[3])
			else:
				self.actions['DBACK'].setIcon(self.v_icons[0])
				self.actions['BACK'].setIcon(self.v_icons[1])
				self.actions['FORWARD'].setIcon(self.v_icons[2])
				self.actions['DFORWARD'].setIcon(self.v_icons[3])

			self.cur_orient = self.orientation()
			self.palwidget.set_orient(self.orientation())
			self.mw.app.config.palette_orientation = self.orientation()

	def build(self):

		self.actions['DBACK'] = AppAction(self.h_icons[0], '', self, self.dback, '')
		self.addAction(self.actions['DBACK'])

		self.actions['BACK'] = AppAction(self.h_icons[1], '', self, self.back, '')
		self.addAction(self.actions['BACK'])

		self.palwidget = palette_widget.PaletteWidget(self)
		self.addWidget(self.palwidget)

		policy = QtGui.QSizePolicy()
		policy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
		policy.setVerticalPolicy(QtGui.QSizePolicy.Expanding)

		self.palwidget.setSizePolicy(policy)

		self.actions['FORWARD'] = AppAction(self.h_icons[2], '', self, self.forward, '')
		self.addAction(self.actions['FORWARD'])

		self.actions['DFORWARD'] = AppAction(self.h_icons[3], '', self, self.dforward, '')
		self.addAction(self.actions['DFORWARD'])

		self.setContextMenuPolicy(Qt.Qt.PreventContextMenu)
	
	def dforward(self):
		self.palwidget.position -= 10
		if self.palwidget.position < -self.palwidget.max_pos: 
			self.palwidget.position = -self.palwidget.max_pos
		self.palwidget.update()

	def forward(self):
		self.palwidget.position -= 1
		if self.palwidget.position < -self.palwidget.max_pos: 
			self.palwidget.position = -self.palwidget.max_pos
		self.palwidget.update()

	def back(self):
		self.palwidget.position += 1
		if self.palwidget.position > 0: 
			self.palwidget.position = 0
		self.palwidget.update()
		
	def dback(self):
		self.palwidget.position += 10
		if self.palwidget.position > 0:
			self.palwidget.position = 0
		self.palwidget.update()
