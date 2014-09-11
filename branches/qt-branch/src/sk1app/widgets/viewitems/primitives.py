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


from PyQt4 import QtCore, QtGui, Qt

from uc2.sk1doc import model

from sk1app import modes

class SelectableItem(QtGui.QGraphicsItem):

	def __init__(self, gvcanvas, obj):
		QtGui.QGraphicsItem.__init__(self)
		self.Type = QtGui.QGraphicsItem.UserType + model.SELECTABLE_CLASS
		self.canvas = gvcanvas
		self.presenter = gvcanvas.presenter
		self.obj = obj
		self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
		self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)

	def type(self):
		return self.Type

	def boundingRect(self):
		return self.childrenBoundingRect()

	def paint(self, *args):
		pass

class PrimitiveItem(SelectableItem):

	def __init__(self, gvcanvas, obj):
		SelectableItem.__init__(self, gvcanvas, obj)
		self.Type = QtGui.QGraphicsItem.UserType + model.PRIMITIVE_CLASS
		self.orig_path = QtGui.QPainterPath()
		self.path = None

	def type(self):
		return self.Type

	def boundingRect(self):
		return self.childrenBoundingRect()

	def paint(self, *args):
		pass


import random

class RectangleItem(PrimitiveItem):

	def __init__(self, gvcanvas, obj):
		PrimitiveItem.__init__(self, gvcanvas, obj)

		self.Type = QtGui.QGraphicsItem.UserType + model.RECTANGLE
		self.fill = QtGui.QBrush(QtGui.QColor(random.randint(0, 255),
									random.randint(0, 255),
									random.randint(0, 255),
									255))
		self.outline = QtGui.QPen(QtCore.Qt.black, 0)
		self.update_item()
		self.setSelected(True)

	def update_item(self):
		m11, m12, m21, m22, dx, dy = self.obj.trafo
		self.trafo = QtGui.QMatrix(m11, m12, m21, m22, dx, dy)
		rect = self.obj
		path = self.orig_path
		path.moveTo(rect.start[0], rect.start[1])
		path.lineTo(rect.start[0] + rect.width, rect.start[1])
		path.lineTo(rect.start[0] + rect.width, rect.start[1] + rect.height)
		path.lineTo(rect.start[0], rect.start[1] + rect.height)
		path.lineTo(rect.start[0], rect.start[1])
		self.path = path.__mul__(self.trafo)

	def boundingRect(self):
		return self.path.boundingRect()

	def shape(self):
		return self.path

	def paint(self, painter, option, widget):
		painter.setBrush(self.fill)
		painter.setPen(self.outline)
		painter.drawPath(self.path)

	def apply_trafo(self, matrix):
		self.prepareGeometryChange()
		self.trafo *= matrix
		self.path = self.orig_path.__mul__(self.trafo)
		self.obj.trafo = [self.trafo.m11(), self.trafo.m12(),
						self.trafo.m21(), self.trafo.m22(),
						self.trafo.dx(), self.trafo.dy()]
