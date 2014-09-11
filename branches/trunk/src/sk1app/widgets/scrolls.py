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

from uc2.uc_conf import mm_to_pt

WORKSPACE_HEIGHT = 2000 * mm_to_pt
WORKSPACE_WIDTH = 4000 * mm_to_pt
SCALE = 1000.0

class DrawingScroll(QtGui.QScrollBar):
	
	def __init__(self, orient, parent, app, presenter):
		
		QtGui.QScrollBar.__init__(self, orient, parent)
		
		self.app = app
		self.presenter = presenter		
		self.orient = orient
		self.eventloop = presenter.eventloop	
		self.value_ = 0				
		self.my_change = False
		self.programmatical = False
		
		if self.orient == Qt.Qt.Horizontal:
			self.setMinimum(int(-SCALE / 2))
			self.setMaximum(int(SCALE / 2))		
			self.setSingleStep(int(SCALE / 100))
			self.setValue(self.value_)
		else:
			self.setMinimum(int(-SCALE / 2))
			self.setMaximum(int(SCALE / 2))
			self.setSingleStep(int(SCALE / 100))
			self.setValue(self.value_)
		self.eventloop.connect(self.eventloop.VIEW_CHANGED, self.update_value)	
		self.valueChanged.connect(self.value_udated)	
		self.sliderMoved.connect(self.update_trafo)
		
	def update_value(self, *args):
		self.viewport = self.presenter.viewport
		if self.my_change:
			self.my_change = False
			return
		x, y = self.viewport.center
		x = int(SCALE * x / WORKSPACE_WIDTH)
		y = int(SCALE * y / WORKSPACE_HEIGHT)
		if self.orient == Qt.Qt.Horizontal: 
			if not x: x = 0
			if not x == int(self.value_):
				self.value_ = x
				self.programmatical = True	
				self.setValue(-x)
		else:
			if not y: y = 0
			if not y == int(self.value_):
				self.value_ = y
				self.programmatical = True	
				self.setValue(-y)
				
	def value_udated(self):
		if not self.programmatical:
			self.update_trafo()
		else:
			self.programmatical = False
	
	def update_trafo(self):
		if not int(self.value_) == -self.value():
			self.value_ = -self.value()
			self.viewport = self.presenter.viewport
			value = -1.0 * self.value()
			x0, y0 = self.viewport.center
			if self.orient == Qt.Qt.Horizontal:
				x1 = value * WORKSPACE_WIDTH / SCALE
				y1 = y0
			else:
				x1 = x0
				y1 = value * WORKSPACE_HEIGHT / SCALE	
			self.my_change = True
			self.viewport.center = [x1, y1]
			self.viewport.change_trafo()


