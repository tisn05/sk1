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

class SelectFrame(QtGui.QGraphicsItem):

	Type = QtGui.QGraphicsItem.UserType + 2

	def __init__(self, gvcanvas):
		QtGui.QGraphicsItem.__init__(self)

		self.canvas = gvcanvas
		self.markers = []
		self.rect = QtCore.QRectF(0, 0, 100, 100)
		self.fill = QtGui.QColor(0, 255, 0, 30)
		self.outline = QtGui.QPen(QtCore.Qt.black, 1,
								Qt.Qt.DashLine, join=Qt.Qt.MiterJoin)
		self.bgoutline = QtGui.QPen(QtCore.Qt.white, 1,
								Qt.Qt.SolidLine, join=Qt.Qt.MiterJoin)
		self.path = QtGui.QPainterPath()
		self.path.addRect(self.rect)
		self.setZValue(100)
		self.position = QtCore.QPointF(0, 0)
		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
		self.setVisible(False)

	def type(self):
		return SelectFrame.Type

	def boundingRect(self):
		return self.rect

	def shape(self):
		return self.path

	def paint(self, painter, option, widget):
		painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
		width = 1.0 / self.canvas.get_factor()
		self.bgoutline.setWidthF(width)
		self.outline.setWidthF(width)
		painter.setPen(self.bgoutline)
		painter.drawRect(self.rect)
		painter.setPen(self.outline)
		painter.drawRect(self.rect)
		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
		
	def set_rect_and_matrix(self, rect, matrix=Qt.QMatrix(1,0,0,1,0,0)):
		self.prepareGeometryChange()
		self.rect = QtCore.QRectF()
		self.rect = self.rect.unite(rect)
		self.path = QtGui.QPainterPath()
		self.path.addRect(self.rect)
		self.path = self.path.__mul__(matrix)
		self.position = self.pos()

	def set_rect_by_rect(self, rect):
		self.prepareGeometryChange()
		self.rect = QtCore.QRectF()
		self.rect = self.rect.unite(rect)
		self.path = QtGui.QPainterPath()
		self.path.addRect(self.rect)
		self.position = self.pos()

	def set_rect(self, p0, p1):
		self.prepareGeometryChange()
		self.path = QtGui.QPainterPath()
		p0 = self.canvas.mapToScene(p0)
		p1 = self.canvas.mapToScene(p1)
		self.rect = QtCore.QRectF(p0, p1).normalized()
		self.path.addRect(self.rect)

OFFSET = 10.0
MARKER_SIZE = 7.0
POINT_SIZE = 5.0

class SelectionItem(QtGui.QGraphicsItem):
	Type = QtGui.QGraphicsItem.UserType + 3
	outline = QtGui.QPen(QtCore.Qt.gray, 1,
								Qt.Qt.DashLine, join=Qt.Qt.MiterJoin)
	bgoutline = QtGui.QPen(QtCore.Qt.white, 1,
								Qt.Qt.SolidLine, join=Qt.Qt.MiterJoin)
	marker_border = QtGui.QPen(QtGui.QColor("#004DFF"), 1,
								Qt.Qt.SolidLine, join=Qt.Qt.MiterJoin)
	point_border = QtGui.QPen(QtCore.Qt.black, 1,
								Qt.Qt.SolidLine, join=Qt.Qt.MiterJoin)

	def __init__(self, gvcanvas, obj):
		QtGui.QGraphicsItem.__init__(self)
		self.canvas = gvcanvas
		self.obj = obj
		obj.view_item = self
		self.markers = []
		self.points = []
		self.rect = QtCore.QRectF(0, 0, 100, 100)
		self.brect = QtCore.QRectF(0, 0, 100, 100)
		self.orig_rect = QtCore.QRectF().unite(self.rect)
		self.path = QtGui.QPainterPath()
		self.path.addRect(self.rect)
		self.setZValue(10)
		self.setVisible(False)

	def type(self):
		return SelectFrame.Type

	def boundingRect(self):
		return self.rect

	def bbox(self):
		return self.brect

	def shape(self):
		return self.path

	def paint(self, painter, option, widget):
		painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
		width = 1.0 / self.canvas.get_factor()
		self.recalc()
		self.bgoutline.setWidthF(width)
		self.outline.setWidthF(width)
		self.marker_border.setWidthF(width)
		self.point_border.setWidthF(width)

		painter.setPen(self.point_border)
		painter.setBrush(QtCore.Qt.white)
		for point in self.points:
			painter.drawRect(point)
		painter.setBrush(QtCore.Qt.NoBrush)
		painter.setPen(self.bgoutline)
		painter.drawRect(self.orig_rect)
		painter.setPen(self.outline)
		painter.drawRect(self.orig_rect)
		painter.setPen(self.marker_border)
		painter.setBrush(QtCore.Qt.white)
		for marker in self.markers:
			painter.drawRect(marker)
		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

	def refresh(self):
		if self.obj.items:
			self.setVisible(False)
			self.prepareGeometryChange()
			self.recalc()
			self.setVisible(True)
		else:
			self.setVisible(False)

	def recalc(self):
		factor = self.canvas.get_factor()
		offset = OFFSET / factor
		point_size = POINT_SIZE / factor
		point_offset = point_size / 2.0
		self.rect = QtCore.QRectF()
		self.brect = QtCore.QRectF()
		self.points = []
		for item in self.obj.items:
			rect = item.boundingRect()
			self.rect = self.rect.unite(rect)
			self.points.append(QtCore.QRectF(rect.x() - point_offset,
											rect.y() - point_offset,
											point_size, point_size))
		self.brect = self.brect.unite(self.rect)
		self.rect.setX(self.rect.x() - offset)
		self.rect.setY(self.rect.y() - offset)
		self.rect.setWidth(self.rect.width() + offset)
		self.rect.setHeight(self.rect.height() + offset)
		self.orig_rect = QtCore.QRectF().unite(self.rect)
		self.path = QtGui.QPainterPath()
		self.path.addRect(self.rect)
		self.set_markers()

	def set_markers(self):
		size = MARKER_SIZE / (2.0 * self.canvas.get_factor())
		x0 = self.rect.x() - size
		y0 = self.rect.y() - size
		x1 = x0 + self.rect.width()
		y1 = y0 + self.rect.height()
		mx = x0 + self.rect.width() / 2.0
		my = y0 + self.rect.height() / 2.0
		w = size * 2.0
		self.markers = [
					QtCore.QRectF(x0, y0, w, w),
					QtCore.QRectF(mx, y0, w, w),
					QtCore.QRectF(x1, y0, w, w),
					QtCore.QRectF(x0, my, w, w),
					#QtCore.QRectF(mx, my, w, w),
					QtCore.QRectF(x1, my, w, w),
					QtCore.QRectF(x0, y1, w, w),
					QtCore.QRectF(mx, y1, w, w),
					QtCore.QRectF(x1, y1, w, w),
						]

		self.rect.setX(self.rect.x() - size * 2.0)
		self.rect.setY(self.rect.y() - size * 2.0)
		self.rect.setWidth(self.rect.width() + size * 2.0)
		self.rect.setHeight(self.rect.height() + size * 2.0)
