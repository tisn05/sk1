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
from sk1app.resources import cmyk_palette

class PaletteWidget(QtGui.QWidget):

	def __init__(self, parent=None):

		QtGui.QWidget.__init__(self, parent)
		self.parent = parent
		self.app = parent.app
		self.config = parent.app.config
		self.cur_orient = Qt.Qt.Horizontal
		self.pal = cmyk_palette.palette

		self.setMinimumSize(16, 16)
		self.setAutoFillBackground(True)
		self.update()
		self.position = 0
		self.max_pos = 0
		self.max_position()

	def set_orient(self, orient):
		self.cur_orient = orient
		self.max_position()

	def max_position(self):
		if self.width() and self.height():
			if self.cur_orient == Qt.Qt.Horizontal:
				size = float(self.config.palette_cell_horizontal)
				self.max_pos = len(self.pal) * size / self.width() - 1.0
				self.max_pos *= self.width() / size
			else:
				size = float(self.config.palette_cell_vertical)
				self.max_pos = len(self.pal) * size / self.height() - 1.0
				self.max_pos *= self.height() / size

	def wheelEvent(self, event):
		shift = int(event.delta() / 12)
		self.position += shift
		if self.position > 0: self.position = 0
		if self.position < -self.max_pos: self.position = -self.max_pos
		self.update()

	def paintEvent(self, *args):
		self.parent.check_orientation()
		self.max_position()
		if self.position < -self.max_pos: self.position = -self.max_pos

		painter = QtGui.QPainter(self)
		painter.setPen(QtGui.QColor(0, 0, 0))
		if self.cur_orient == Qt.Qt.Horizontal:
			x0 = 0.0; y0 = 3.0
			x1 = self.config.palette_cell_horizontal
			y1 = self.height()*1.0 - 4

			i = self.position
			for color in self.pal:
				painter.save()
				x0 = i * self.config.palette_cell_horizontal
				x1 = x0 + self.config.palette_cell_horizontal - 1
				rect = QtCore.QRect(QtCore.QPoint(x0, y0), QtCore.QPoint(x1, y1))
				qclr = self.app.default_cms.get_qcolor(color)
				painter.setBrush(qclr)
				painter.drawRect(rect)
				painter.restore()
				i += 1
		else:
			x0 = 3.0; y0 = 0.0
			x1 = self.width()*1.0 - 4; y1 = self.config.palette_cell_vertical

			i = self.position
			for color in self.pal:
				painter.save()
				y0 = i * self.config.palette_cell_vertical
				y1 = y0 + self.config.palette_cell_vertical - 1
				rect = QtCore.QRect(QtCore.QPoint(x0, y0), QtCore.QPoint(x1, y1))
				qclr = self.app.default_cms.get_qcolor(color)
				painter.setBrush(qclr)
				painter.drawRect(rect)
				painter.restore()
				i += 1




