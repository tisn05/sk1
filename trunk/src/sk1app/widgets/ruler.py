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

import operator
from math import floor, ceil

from PyQt4 import QtGui, Qt

from uc2.uc_conf import unit_dict
from uc2 import sk1doc

from sk1app import events
from sk1app.utils.color import qt_middle_color


HORIZONTAL = 0
VERTICAL = 1
FIXED_SIZE = 20

tick_lengths = (5, 4, 2, 2)
text_tick = 9

tick_config = {'in': (1.0, (2, 2, 2, 2)),
               'cm': (1.0, (2, 5)),
               'mm': (10.0, (2, 5)),
               'pt': (100.0, (2, 5, 2, 5)),
               #'pt': (72.0, (2, 3, 12)),
               }

HFONT = {
	'.': (2, [(0, 0, 0, 0)]),
	',': (2, [(0, 0, 0, 0)]),
	'-': (4, [(0, 2, 2, 2)]),
	'0': (5, [(0, 0, 3, 0), (3, 0, 3, 4), (3, 4, 0, 4), (0, 4, 0, 0)]),
	'1': (3, [(1, 0, 1, 4), (1, 4, 0, 4)]),
	'2': (5, [(3, 0, 0, 0), (0, 0, 0, 2), (0, 2, 3, 2), (3, 2, 3, 4), (3, 4, 0, 4)]),
	'3': (5, [(0, 0, 3, 0), (0, 2, 3, 2), (0, 4, 3, 4), (3, 4, 3, 0)]),
	'4': (5, [(0, 4, 0, 1), (0, 1, 3, 1), (3, 0, 3, 4)]),
	'5': (5, [(0, 0, 3, 0), (3, 0, 3, 2), (3, 2, 0, 2), (0, 2, 0, 4), (0, 4, 3, 4)]),
	'6': (5, [(2, 4, 0, 4), (0, 4, 0, 0), (0, 0, 3, 0), (3, 0, 3, 2), (3, 2, 0, 2)]),
	'7': (5, [(0, 4, 3, 4), (3, 3, 1, 1), (1, 1, 1, 0)]),
	'8': (5, [(0, 0, 0, 4), (3, 0, 3, 4), (0, 0, 3, 0), (0, 2, 3, 2), (0, 4, 3, 4)]),
	'9': (5, [(1, 0, 3, 0), (3, 0, 3, 4), (3, 4, 0, 4), (0, 4, 0, 2), (0, 2, 3, 2)]),
}

VFONT = {
	'.': (2, [(0, 0, 0, 0), ]),
	',': (2, [(0, 0, 0, 0), ]),
	'-': (4, [(2, 0, 2, 2), ]),
	'0': (5, [(0, 0, 4, 0), (4, 0, 4, 3), (4, 3, 0, 3), (0, 3, 0, 0)]),
	'1': (3, [(0, 1, 4, 1), (4, 1, 4, 0)]),
	'2': (5, [(0, 3, 0, 0), (0, 0, 2, 0), (2, 0, 2, 3), (2, 3, 4, 3), (4, 3, 4, 0)]),
	'3': (5, [(0, 0, 0, 3), (0, 3, 4, 3), (4, 3, 4, 0), (2, 3, 2, 0)]),
	'4': (5, [(4, 0, 1, 0), (1, 0, 1, 3), (4, 3, 0, 3)]),
	'5': (5, [(4, 3, 4, 0), (4, 0, 2, 0), (2, 0, 2, 3), (2, 3, 0, 3), (0, 3, 0, 0)]),
	'6': (5, [(4, 2, 4, 0), (4, 0, 0, 0), (0, 0, 0, 3), (0, 3, 2, 3), (2, 3, 2, 0)]),
	'7': (5, [(4, 0, 4, 3), (3, 3, 1, 1), (1, 1, 0, 1)]),
	'8': (5, [(0, 0, 0, 3), (0, 3, 4, 3), (4, 3, 4, 0), (2, 3, 2, 0), (4, 0, 0, 0)]),
	'9': (5, [(0, 1, 0, 3), (0, 3, 4, 3), (4, 3, 4, 0), (4, 0, 2, 0), (2, 0, 2, 2)]),
}

SIGN = {
	0: ([1, 1, 10, 16, 10], [1, 15, 9, 15, 11], [1, 8, 2, 8, 16], [1, 7, 3, 9, 3], [0, 2, 16, 14, 4]),
	1: ([1, 3, 2, 3, 16], [1, 2, 3, 4, 3], [1, 1, 14, 16, 14], [1, 15, 13, 15, 15], [0, 5, 12, 15, 2]),
	2: ([1, 3, 2, 3, 16], [1, 2, 15, 4, 15], [1, 1, 4, 16, 4], [1, 15, 3, 15, 5], [0, 3, 4, 13, 14])
}

class RulerCorner(QtGui.QWidget):
	origin = 1

	def __init__(self, parent, app, presenter):

		QtGui.QWidget.__init__(self, parent)
		self.app = app
		self.parent = parent
		self.presenter = presenter
		self.setBackgroundRole(QtGui.QPalette.Base)
		self.setAutoFillBackground(True)
		self.setMaximumWidth(FIXED_SIZE)
		self.setMaximumHeight(FIXED_SIZE)

		self.policy = QtGui.QSizePolicy()
		self.policy.setHorizontalPolicy(QtGui.QSizePolicy.Fixed)
		self.policy.setVerticalPolicy(QtGui.QSizePolicy.Fixed)

		self.eventloop = presenter.eventloop
		self.origin = self.presenter.model.doc_origin

		self.line_color = qt_middle_color(self.palette().mid().color(),
										self.palette().background().color(),
										0.5)
		linearGradient = QtGui.QLinearGradient(0, 0, 20, 20)
		linearGradient.setColorAt(0.0, self.palette().background().color())
		linearGradient.setColorAt(0.5, self.palette().background().color())
		linearGradient.setColorAt(1.0, self.line_color)
		self.brush = QtGui.QBrush(linearGradient)
		self.eventloop.connect(self.eventloop.DOC_MODIFIED, self.check_coords)

	def check_coords(self, *args):
		if not self.origin == self.presenter.model.doc_origin:
			self.origin = self.presenter.model.doc_origin
			self.update()

	def mouseDoubleClickEvent (self, event):
		origin = self.presenter.model.doc_origin
		if origin < sk1doc.ORIGINS[-1]:
			origin += 1
		else:
			origin = sk1doc.ORIGINS[0]
		self.presenter.api.set_doc_origin(origin)

	def paintEvent(self, *args):
		painter = QtGui.QPainter(self)
		style = self.parent.app.config.ruler_style
		if style:
			painter.fillRect(0, 0, self.width(), self.height(), self.brush)
			painter.setPen(self.line_color)
		else:
			painter.setPen(self.palette().text().color())
		painter.save()
		painter.drawLine(0, self.height() - 1,
						self.width() - 1, self.height() - 1)
		painter.drawLine(self.width() - 1, self.height() - 1,
						self.width() - 1, 0)

		coord = self.origin
		for job in SIGN[coord]:
			if job[0]:
				painter.setPen(Qt.Qt.SolidLine)
			else:
				painter.setPen(Qt.Qt.DotLine)
			painter.drawLine(job[1], job[2], job[3], job[4])
		painter.restore()


class Ruler(QtGui.QWidget):

	def __init__(self, app, parent, presenter, orientation=HORIZONTAL):

		QtGui.QWidget.__init__(self, parent)
		self.parent = parent
		self.orientation = orientation
		self.app = app
		self.presenter = presenter
		self.doc = presenter.model
		self.viewport = presenter.view
		self.setBackgroundRole(QtGui.QPalette.Base)
		self.setAutoFillBackground(True)

		self.origin = self.presenter.model.doc_origin
		self.positions = None
		self.set_range(0.0, 1.0)

		self.policy = QtGui.QSizePolicy()
		self.setMinimumSize(FIXED_SIZE, FIXED_SIZE)
		if self.orientation:
			self.line_color = qt_middle_color(self.palette().mid().color(),
											self.palette().background().color(),
											0.5)
			linearGradient = QtGui.QLinearGradient(0, 0, 20, 0)
			linearGradient.setColorAt(0.0, self.palette().background().color())
			linearGradient.setColorAt(0.3, self.palette().background().color())
			linearGradient.setColorAt(1.0, self.line_color)
			self.brush = QtGui.QBrush(linearGradient)

			self.policy.setVerticalPolicy(QtGui.QSizePolicy.Expanding)
			self.policy.setHorizontalPolicy(QtGui.QSizePolicy.Fixed)
			self.setSizePolicy(self.policy)
		else:
			self.line_color = qt_middle_color(self.palette().mid().color(),
											self.palette().background().color(),
											0.5)
			linearGradient = QtGui.QLinearGradient(0, 0, 0, 20)
			linearGradient.setColorAt(0.0, self.palette().background().color())
			linearGradient.setColorAt(0.3, self.palette().background().color())
			linearGradient.setColorAt(1.0, self.line_color)
			self.brush = QtGui.QBrush(linearGradient)

			self.policy.setVerticalPolicy(QtGui.QSizePolicy.Fixed)
			self.policy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
			self.setSizePolicy(self.policy)
		eventloop = self.presenter.eventloop
		eventloop.connect(eventloop.VIEW_CHANGED, self.update_ruler)
		eventloop.connect(eventloop.DOC_MODIFIED, self.check_config)
		events.connect(events.CONFIG_MODIFIED, self.check_config)

	def check_config(self, *args):
		if not self.origin == self.presenter.model.doc_origin:
			self.origin = self.presenter.model.doc_origin
			self.update()
			return
		if args[0][0] == 'ruler_coordinates' or args[0][0] == 'default_unit':
			self.update()

	def update_ruler(self, *args):
		self.update()

	def set_range(self, start, pixel_per_pt):
		self.start = start
		self.pixel_per_pt = pixel_per_pt
		self.positions = None

	def get_positions(self):
		self.viewport = self.presenter.view
		scale = 1.0
		x = y = 0
		if self.viewport:
			point = self.viewport.mapToScene(0, 0)
			x, y = [point.x(), point.y()]
			scale = self.viewport.get_factor()

		w, h = self.presenter.get_page_size()
		if self.origin == sk1doc.DOC_ORIGIN_LL:
			x += w / 2.0
			y += h / 2.0
		elif self.origin == sk1doc.DOC_ORIGIN_LU:
			x += w / 2.0
			y -= h / 2.0

		if self.orientation:
			self.set_range(y, scale)
		else:
			self.set_range(x, scale)

		config = self.app.config
		min_text_step = config.ruler_min_text_step
		max_text_step = config.ruler_max_text_step
		min_tick_step = config.ruler_min_tick_step
		if self.orientation == HORIZONTAL:
			length = self.width()
			origin = self.start
		else:
			length = self.height()
			origin = self.start - length / self.pixel_per_pt
		unit_name = config.default_unit
		pt_per_unit = unit_dict[unit_name]
		units_per_pixel = 1.0 / (pt_per_unit * self.pixel_per_pt)
		factor, subdivisions = tick_config[unit_name]
		subdivisions = (1,) + subdivisions

		factor = factor * pt_per_unit
		start_pos = floor(origin / factor) * factor
		main_tick_step = factor * self.pixel_per_pt
		num_ticks = floor(length / main_tick_step) + 2

		if main_tick_step < min_tick_step:
			tick_step = ceil(min_tick_step / main_tick_step) * main_tick_step
			subdivisions = (1,)
			ticks = 1
		else:
			tick_step = main_tick_step
			ticks = 1
			for depth in range(len(subdivisions)):
				tick_step = tick_step / subdivisions[depth]
				if tick_step < min_tick_step:
					tick_step = tick_step * subdivisions[depth]
					depth = depth - 1
					break
				ticks = ticks * subdivisions[depth]
			subdivisions = subdivisions[:depth + 1]

		positions = range(int(num_ticks * ticks))
		positions = map(operator.mul, [tick_step] * len(positions), positions)
		positions = map(operator.add, positions,
						[(start_pos - origin) * self.pixel_per_pt]
						* len(positions))

		stride = ticks
		marks = [None] * len(positions)
		for depth in range(len(subdivisions)):
			stride = stride / subdivisions[depth]
			if depth >= len(tick_lengths):
				height = tick_lengths[-1]
			else:
				height = tick_lengths[depth]
			for i in range(0, len(positions), stride):
				if marks[i] is None:
					marks[i] = (height, int(round(positions[i])))

		texts = []
		if main_tick_step < min_text_step:
			stride = int(ceil(min_text_step / main_tick_step))
			start_index = stride - (floor(origin / factor) % stride)
			start_index = int(start_index * ticks)
			stride = stride * ticks
		else:
			start_index = 0
			stride = ticks
			step = main_tick_step
			for div in subdivisions:
				step = step / div
				if step < min_text_step:
					break
				stride = stride / div
				if step < max_text_step:
					break

		for i in range(start_index, len(positions), stride):
			pos = positions[i] * units_per_pixel + origin / pt_per_unit
			pos = round(pos, 5)
			if self.origin == sk1doc.DOC_ORIGIN_LU and self.orientation == VERTICAL:
				pos *= -1
			if pos == 0.0:
				pos = 0.0
			texts.append(("%g" % pos, marks[i][-1]))

		self.positions = marks
		self.texts = texts
		return self.positions, self.texts

	def paintEvent(self, *args):
		style = self.app.config.ruler_style

		painter = QtGui.QPainter(self)
		painter.setPen(self.palette().text().color())
		painter.save()
		if style:
			painter.fillRect(0, 0, self.width(), self.height(), self.brush)
		if self.orientation:
			self.draw_vertical(painter)
			if style: painter.setPen(self.line_color)
			painter.drawLine(self.width() - 1, self.height() - 1,
							self.width() - 1, 0)
		else:
			self.draw_horizontal(painter)
			if style: painter.setPen(self.line_color)
			painter.drawLine(0, self.height() - 1,
							self.width() - 1, self.height() - 1)
		painter.restore()

	def draw_vertical(self, painter):
		height = self.height()
		width = self.width()

		ticks, texts = self.get_positions()
		for h, pos in ticks:
			pos = height - pos
			painter.drawLine(width - h - 1, pos, width, pos)
			pos += 1

		x = 8
		for text, pos in texts:
			pos = height - pos
			pos -= 1
			painter.drawLine(width - text_tick - 1, pos + 1, width, pos + 1)
			for character in str(text):
				data = VFONT[character]
				lines = data[1]
				for line in lines:
					painter.drawLine(x - line[0], pos - line[1],
									x - line[2], pos - line[3])
				pos -= data[0]

	def draw_horizontal(self, painter):
		height = self.height()

		ticks, texts = self.get_positions()
		for h, pos in ticks:
			painter.drawLine(pos, height,
							pos, height - h - 1)
			pos += 1

		y = 8
		for text, pos in texts:
			pos += 1
			painter.drawLine(pos - 1 , height,
							pos - 1, height - text_tick - 1)
			for character in str(text):
				data = HFONT[character]
				lines = data[1]
				for line in lines:
					painter.drawLine(line[0] + pos, y - line[1],
									line[2] + pos, y - line[3])
				pos += data[0]


