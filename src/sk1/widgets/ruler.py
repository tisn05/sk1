# -*- coding: utf-8 -*-
#
#	Copyright (C) 2011-2012 by Igor E. Novikov
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
from math import floor

import gtk
import gobject
import cairo

from uc2.uc2const import unit_dict, HORIZONTAL, VERTICAL
from uc2.formats.sk1.sk1const import DOC_ORIGIN_CENTER, DOC_ORIGIN_LL, \
DOC_ORIGIN_LU, ORIGINS
from uc2.utils import system

from sk1 import config, events, modes
from sk1.appconst import RENDERING_DELAY

DEFAULT_CURSOR = -1
SIZE = 18

tick_lengths = (5, 4, 2, 2)
text_tick = 9

tick_config = {'in': (1.0, (2, 2, 2, 2)),
               'cm': (1.0, (2, 5)),
               'mm': (10.0, (2, 5)),
               'pt': (100.0, (2, 5, 2, 5)),
               }

FONT = {
	'.': (2, [(0, 1), (0, 0), (0, 1)]),
	',': (2, [(0, 1), (0, 0), (0, 1)]),
	'-': (4, [(0, 2), (2, 2), (0, 2), (), (1, 2), (0, 2), (1, 2)]),
	'0': (5, [(0, 0), (3, 0), (3, 4), (0, 4), (0, 0)]),
	'1': (3, [(1, 0), (1, 4), (0, 4), (1, 4)]),
	'2': (5, [(0, 0), (3, 0), (0, 0), (0, 2), (3, 2), (3, 4), (0, 4), (3, 4)]),
	'3': (5, [(3, 0), (0, 0), (3, 0), (3, 4), (3, 2), (1, 2), (3, 2), (3, 4), (0, 4), (3, 4)]),
	'4': (5, [(3, 0), (3, 4), (3, 0), (3, 1), (0, 1), (0, 4), (0, 1)]),
	'5': (5, [(3, 0), (0, 0), (3, 0), (3, 2), (0, 2), (0, 4), (3, 4), (0, 4)]),
	'6': (5, [(0, 4), (2, 4), (0, 4), (0, 0), (3, 0), (3, 2), (0, 2)]),
	'7': (5, [(3, 4), (0, 4), (3, 4), (3, 3), (), (1, 2), (1, 0), (1, 1), (), (2, 3), (2, 2), (2, 3)]),
	'8': (5, [(0, 0), (3, 0), (3, 4), (0, 4), (0, 0), (0, 2), (3, 2)]),
	'9': (5, [(3, 0), (1, 0), (3, 0), (3, 4), (0, 4), (0, 2), (3, 2)]),
}

SIGN = {
	0: ([1, 2, 9, 16, 9], [1, 14, 8, 14, 11], [1, 8, 2, 8, 16], [1, 7, 3, 10, 3], [0, 3, 15, 15, 3]),
	1: ([1, 3, 2, 3, 16], [1, 2, 3, 5, 3], [1, 1, 13, 16, 13], [1, 14, 12, 14, 15], [0, 4, 13, 15, 2]),
	2: ([1, 3, 2, 3, 16], [1, 2, 14, 5, 14], [1, 1, 4, 16, 4], [1, 14, 3, 14, 6], [0, 3, 4, 13, 14])
}

class RulerCorner(gtk.DrawingArea):

	def __init__(self, docarea):
		gtk.DrawingArea.__init__(self)
		self.docarea = docarea
		self.presenter = docarea.presenter
		self.eventloop = self.presenter.eventloop
		self.origin = self.presenter.model.doc_origin

		self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
					gtk.gdk.BUTTON_RELEASE_MASK)

		self.set_size_request(SIZE, SIZE)
		self.connect('expose_event', self.repaint)
		self.connect('button-release-event', self.click_event)
		self.eventloop.connect(self.eventloop.DOC_MODIFIED, self.check_coords)

	def check_coords(self, *args):
		if not self.origin == self.presenter.model.doc_origin:
			self.origin = self.presenter.model.doc_origin
			self.repaint()

	def click_event(self, *args):
		origin = self.presenter.model.doc_origin
		if origin < ORIGINS[-1]:
			origin += 1
		else:
			origin = ORIGINS[0]
		self.presenter.api.set_doc_origin(origin)

	def repaint(self, *args):
		if config.ruler_style:
			color = self.get_style().bg[gtk.STATE_ACTIVE]
			r = color.red / 65535.0
			g = color.green / 65535.0
			b = color.blue / 65535.0
		else:
			r = g = b = 0

		if system.get_os_family() == system.WINDOWS:
			bgcolor = self.get_style().base[gtk.STATE_NORMAL]
		else:
			bgcolor = self.get_style().bg[gtk.STATE_NORMAL]
		r0 = bgcolor.red / 65535.0
		g0 = bgcolor.green / 65535.0
		b0 = bgcolor.blue / 65535.0

		painter = self.window.cairo_create()
		painter.set_matrix(cairo.Matrix())
		painter.set_antialias(cairo.ANTIALIAS_NONE)
		painter.set_source_rgb(r0, g0, b0)
		painter.paint()
		painter.set_source_rgb(r, g, b)
		painter.set_line_width(1.0)
		painter.rectangle(0, 0, SIZE, SIZE)
		painter.stroke()

		coord = self.origin
		painter.set_source_rgb(0, 0, 0)
		painter.set_line_width(1.0)
		for job in SIGN[coord]:
			if job[0]:
				painter.set_dash([], 0)
			else:
				painter.set_dash([0.2], 0)
			painter.move_to(job[1], job[2])
			painter.line_to(job[3], job[4])
			painter.stroke()

class Ruler(gtk.DrawingArea):

	exposed = False

	def __init__(self, docarea, orient):
		gtk.DrawingArea.__init__(self)
		self.docarea = docarea
		self.app = docarea.app
		self.mw = docarea.app.mw
		self.orient = orient
		self.presenter = docarea.presenter
		self.eventloop = self.presenter.eventloop
		self.doc = self.presenter.model

		self.origin = self.presenter.model.doc_origin
		self.positions = None
		self.set_range(0.0, 1.0)

		if self.orient:
			self.set_size_request(SIZE, -1)
		else:
			self.set_size_request(-1, SIZE)

		self.default_cursor = gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)
		if self.orient == HORIZONTAL:
			self.guide_cursor = self.app.cursors[modes.HGUIDE_MODE]
		else:
			self.guide_cursor = self.app.cursors[modes.VGUIDE_MODE]

		self.set_property("can-focus", True)

		self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
					gtk.gdk.POINTER_MOTION_MASK |
					gtk.gdk.BUTTON_RELEASE_MASK)

		self.pointer = []
		self.draw_guide = False

		self.connect('expose_event', self.repaint)
		self.connect('button_press_event', self.mouse_down)
		self.connect('motion_notify_event', self.mouse_move)
		self.connect('button_release_event', self.mouse_up)
		self.eventloop.connect(self.eventloop.VIEW_CHANGED, self.repaint)
		self.eventloop.connect(self.eventloop.DOC_MODIFIED, self.check_config)
		events.connect(events.CONFIG_MODIFIED, self.check_config)

	#------ Guides creation
	def set_cursor(self, mode=0):
		if mode == DEFAULT_CURSOR:
			self.window.set_cursor(self.default_cursor)
		else:
			self.window.set_cursor(self.guide_cursor)

	def mouse_down(self, widget, event):
		x, y, w, h = self.allocation
		w = float(w)
		h = float(h)
		self.width = w
		self.height = h
		self.draw_guide = True
		self.set_cursor()
		self.timer = gobject.timeout_add(RENDERING_DELAY, self.repaint_guide)

	def mouse_up(self, widget, event):
		self.pointer = [event.x, event.y]
		if self.orient == HORIZONTAL:
			y_win = self.pointer[1] - self.height
			if y_win > 0.0:
				p = [self.pointer[0], y_win]
				p, p_doc = self.presenter.snap.snap_point(p, snap_x=False)[1:]
				self.presenter.api.create_guides([[p_doc[1], HORIZONTAL], ])
		else:
			x_win = self.pointer[0] - self.width
			if x_win > 0.0:
				p = [x_win, self.pointer[1]]
				p, p_doc = self.presenter.snap.snap_point(p, snap_y=False)[1:]
				self.presenter.api.create_guides([[p_doc[0], VERTICAL], ])

		self.set_cursor(DEFAULT_CURSOR)
		if not  self.timer is None:
			gobject.source_remove(self.timer)
		self.draw_guide = False
		self.pointer = []
		self.repaint_guide()
		self.canvas.selection_repaint()

	def mouse_move(self, widget, event):
		if self.draw_guide:
			self.pointer = [event.x, event.y]

	def repaint_guide(self, *args):
		p_doc = []
		orient = HORIZONTAL
		if self.draw_guide and self.pointer:
			if self.orient == HORIZONTAL:
				y_win = self.pointer[1] - self.height
				p = [self.pointer[0], y_win]
				p, p_doc = self.presenter.snap.snap_point(p, snap_x=False)[1:]
			else:
				x_win = self.pointer[0] - self.width
				p = [x_win, self.pointer[1]]
				p, p_doc = self.presenter.snap.snap_point(p, snap_y=False)[1:]
				orient = VERTICAL
		self.canvas.renderer.paint_guide_dragging(p_doc, orient)
		return True

	#------ Guides creation

	def check_config(self, *args):
		if not self.origin == self.presenter.model.doc_origin:
			self.origin = self.presenter.model.doc_origin
			self.queue_draw()
			return
		if args[0][0] == 'ruler_coordinates' or args[0][0] == 'default_unit':
			self.queue_draw()

	def update_ruler(self, *args):
		self.queue_draw()

	def set_range(self, start, pixel_per_pt):
		self.start = start
		self.pixel_per_pt = pixel_per_pt
		self.positions = None

	def get_positions(self):
		self.canvas = self.presenter.canvas
		scale = 1.0
		x = y = 0
		if not self.canvas is None:
			x, y = self.canvas.win_to_doc([0, 0])
			scale = self.canvas.zoom

		w, h = self.presenter.get_page_size()
		if self.origin == DOC_ORIGIN_LU:
			y -= h
		elif self.origin == DOC_ORIGIN_CENTER:
			x -= w / 2.0
			y -= h / 2.0

		if self.orient:
			self.set_range(y, scale)
		else:
			self.set_range(x, scale)

		min_text_step = config.ruler_min_text_step
		max_text_step = config.ruler_max_text_step
		min_tick_step = config.ruler_min_tick_step
		x, y, w, h = self.allocation
		if self.orient == HORIZONTAL:
			length = w
			origin = self.start
		else:
			length = h
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
#			tick_step = ceil(min_tick_step / main_tick_step) * main_tick_step
			tick_step = floor(min_tick_step / main_tick_step) * main_tick_step
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
#			stride = int(ceil(min_text_step / main_tick_step))
			stride = int(floor(min_text_step / main_tick_step))
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
			if self.origin == DOC_ORIGIN_LU and self.orient == VERTICAL:
				pos *= -1
			if pos == 0.0:
				pos = 0.0
			texts.append(("%g" % pos, marks[i][-1]))

		self.positions = marks
		self.texts = texts
		return self.positions, self.texts

	def update_colors(self):
		color = self.mw.get_style().bg[gtk.STATE_ACTIVE]
		self.border_color = [color.red / 65535.0,
						color.green / 65535.0,
						color.blue / 65535.0]

		r, g, b = self.border_color

		if system.get_os_family() == system.WINDOWS:
			color = self.get_style().base[gtk.STATE_NORMAL]
		else:
			color = self.get_style().bg[gtk.STATE_NORMAL]
		self.bg_color = [color.red / 65535.0,
					color.green / 65535.0,
					color.blue / 65535.0]

		r0, g0, b0 = self.bg_color

		if self.orient:
			self.grad = cairo.LinearGradient(0, 0, SIZE, 0)
			self.grad.add_color_stop_rgb(0, r0, g0, b0)
			self.grad.add_color_stop_rgb(1, r, g, b)
		else:
			self.grad = cairo.LinearGradient(0, 0, 0, SIZE)
			self.grad.add_color_stop_rgb(0, r0, g0, b0)
			self.grad.add_color_stop_rgb(1, r, g, b)

		if not config.ruler_style:
			self.border_color = [0, 0, 0]

	def repaint(self, *args):
		if not self.exposed:
			self.update_colors()
			self.exposed = True
			self.set_cursor(DEFAULT_CURSOR)

		r, g, b = self.border_color
		r0, g0, b0 = self.bg_color
		x, y, w, h = self.allocation

		win_ctx = self.window.cairo_create()
		buffer = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
		buffer.set_device_offset(0, 0)
		painter = cairo.Context(buffer)

		painter.set_antialias(cairo.ANTIALIAS_NONE)
		painter.set_source_rgb(r0, g0, b0)
		painter.paint()

		painter.set_line_width(1)
		if self.orient:
			if config.ruler_style:
				painter.set_source(self.grad)
				painter.rectangle(0, 0, SIZE, h + 1)
				painter.fill ()

			painter.set_source_rgb(r, g, b)
			painter.rectangle(0, 0, SIZE, h + 1)
			painter.stroke()

			painter.set_source_rgb(0, 0, 0)
			self.draw_vertical(painter)
		else:
			if config.ruler_style:
				painter.set_source(self.grad)
				painter.rectangle(0, 0, w + 1, SIZE)
				painter.fill ()

			painter.set_source_rgb(r, g, b)
			painter.rectangle(0, 0, w + 1 , SIZE)
			painter.stroke()

			painter.set_source_rgb(0, 0, 0)
			self.draw_horizontal(painter)

		win_ctx.set_source_surface(buffer)
		win_ctx.paint()

	def draw_vertical(self, painter):
		x, y, width, height = self.allocation

		ticks, texts = self.get_positions()

		for h, pos in ticks:
			pos = height - pos
			painter.move_to(width - h - 1, pos)
			painter.line_to(width, pos)
			painter.stroke()
			pos += 1

		x = 6
		for text, pos in texts:
			pos = height - pos
			pos -= 1
			painter.move_to(width - text_tick - 1, pos + 1)
			painter.line_to(width, pos + 1)
			painter.stroke()

			for character in str(text):
				data = FONT[character]
				points = data[1]
				for point in points:
					if not point:
						painter.stroke()
						continue
					painter.line_to(x - point[1], pos - point[0])
				painter.stroke()
				pos -= data[0]

	def draw_horizontal(self, painter):
		x, y, width, height = self.allocation

		ticks, texts = self.get_positions()

		for h, pos in ticks:
			painter.move_to(pos, height)
			painter.line_to(pos, height - h - 1)
			painter.stroke()
			pos += 1

		y = 6
		for text, pos in texts:
			pos += 1
			painter.move_to(pos - 1 , height)
			painter.line_to(pos - 1, height - text_tick - 1)
			painter.stroke()

			for character in str(text):
				data = FONT[character]
				points = data[1]
				for point in points:
					if not point:
						painter.stroke()
						continue
					painter.line_to(point[0] + pos, y - point[1])
				painter.stroke()
				pos += data[0]
