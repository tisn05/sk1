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

class StructuralItem(QtGui.QGraphicsItem):

	def __init__(self, gvcanvas, obj):
		QtGui.QGraphicsItem.__init__(self)
		self.Type = QtGui.QGraphicsItem.UserType + model.STRUCTURAL_CLASS
		self.canvas = gvcanvas
		self.presenter = gvcanvas.presenter
		self.obj = obj

	def type(self):
		return self.Type

	def boundingRect(self):
		return self.childrenBoundingRect()

	def paint(self, *args):
		pass

class DocumentItem(StructuralItem):

	def __init__(self, gvcanvas, obj):
		StructuralItem.__init__(self, gvcanvas, obj)
		self.Type = QtGui.QGraphicsItem.UserType + model.DOCUMENT

	def boundingRect(self):
		p0 = self.canvas.mapToScene(0, 0)
		p1 = self.canvas.mapToScene(self.canvas.width(), self.canvas.height())
		return QtCore.QRectF(p0.x(), p0.y(),
							p1.x() - p0.x(), p1.y() - p0.y()).normalized()

class PagesItem(StructuralItem):

	def __init__(self, gvcanvas, obj):
		StructuralItem.__init__(self, gvcanvas, obj)
		self.Type = QtGui.QGraphicsItem.UserType + model.PAGES

	def boundingRect(self):
		p0 = self.canvas.mapToScene(0, 0)
		p1 = self.canvas.mapToScene(self.canvas.width(), self.canvas.height())
		return QtCore.QRectF(p0.x(), p0.y(),
							p1.x() - p0.x(), p1.y() - p0.y()).normalized()

class LayerGroupItem(StructuralItem):

	def __init__(self, gvcanvas, obj):
		StructuralItem.__init__(self, gvcanvas, obj)
		self.Type = QtGui.QGraphicsItem.UserType + model.LAYER_GROUP

class MasterLayersItem(StructuralItem):

	def __init__(self, gvcanvas, obj):
		StructuralItem.__init__(self, gvcanvas, obj)
		self.Type = QtGui.QGraphicsItem.UserType + model.MASTER_LAYERS

class LayerItem(StructuralItem):

	def __init__(self, gvcanvas, obj):
		StructuralItem.__init__(self, gvcanvas, obj)
		self.Type = QtGui.QGraphicsItem.UserType + model.LAYER

class GridLayerItem(StructuralItem):

	def __init__(self, gvcanvas, obj):
		StructuralItem.__init__(self, gvcanvas, obj)
		self.Type = QtGui.QGraphicsItem.UserType + model.GRID_LAYER

	def boundingRect(self):
		p0 = self.canvas.mapToScene(0, 0)
		p1 = self.canvas.mapToScene(self.canvas.width(), self.canvas.height())
		return QtCore.QRectF(p0.x(), p0.y(),
							p1.x() - p0.x(), p1.y() - p0.y()).normalized()

	def paint(self, *args):
		pass

class GuideLayerItem(StructuralItem):

	def __init__(self, gvcanvas, obj):
		StructuralItem.__init__(self, gvcanvas, obj)
		self.Type = QtGui.QGraphicsItem.UserType + model.GUIDE_LAYER

	def boundingRect(self):
		p0 = self.canvas.mapToScene(0, 0)
		p1 = self.canvas.mapToScene(self.canvas.width(), self.canvas.height())
		return QtCore.QRectF(p0.x(), p0.y(),
							p1.x() - p0.x(), p1.y() - p0.y()).normalized()

	def paint(self, *args):
		pass

PAGEBORDER = 5.0

class PageItem(StructuralItem):

	def __init__(self, gvcanvas, obj):
		StructuralItem.__init__(self, gvcanvas, obj)
		self.Type = QtGui.QGraphicsItem.UserType + model.PAGE
		self.pageborder_color = Qt.QColor('#B1AAA5')

	def boundingRect(self):
		p0 = self.canvas.mapToScene(0, 0)
		p1 = self.canvas.mapToScene(self.canvas.width(), self.canvas.height())
		return QtCore.QRectF(p0.x(), p0.y(),
							p1.x() - p0.x(), p1.y() - p0.y()).normalized()

	def paint(self, painter, option, widget):
		w, h = self.presenter.get_page_size(self.obj)
		factor = self.canvas.get_factor()
		line = 1.0 / factor
		pen = QtGui.QPen(QtCore.Qt.black, line,
						Qt.Qt.SolidLine, join=Qt.Qt.MiterJoin)
		painter.setPen(pen)

		offset = PAGEBORDER / factor
		x = -w / 2.0
		y = -h / 2.0

		#SHADOW		
		rect = QtCore.QRectF(offset + x, -offset + y, w, h)
		painter.fillRect(rect, self.pageborder_color)

		#PAGE BORDER
		painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
		rect = QtCore.QRectF(x, y, w, h)
		painter.fillRect(rect, QtCore.Qt.white)
		painter.drawRect(rect)
		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
