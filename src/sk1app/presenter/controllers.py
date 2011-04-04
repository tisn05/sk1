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

from sk1app.widgets.graphview import ZOOM_IN, ZOOM_OUT
from sk1app import modes

class AbstractController:

	draw = False
	canvas = None
	start = []
	end = []

	def __init__(self, canvas, presenter):
		self.canvas = canvas
		self.app = canvas.app
		self.presenter = presenter
		self.eventloop = presenter.eventloop
		self.start = []
		self.end = []

	def mouse_down(self, event):
		pass

	def mouse_up(self, event):
		pass

	def mouse_move(self, event):
		pass

	def wheel(self, event):
		vb = self.canvas.verticalScrollBar()
		dy = vb.singleStep() * event.delta() / 120.0
		vb.setValue(vb.value() - dy)


class ZoomController(AbstractController):

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)

	def mouse_down(self, event):
		if event.button() == Qt.Qt.LeftButton:
			self.draw = True
			self.start = self.end = event.pos()
		elif event.button() == Qt.Qt.RightButton:
			self.start = event.pos()
			cursor = self.canvas.app.canvas_cursors[modes.ZOOM_OUT_MODE]
			self.canvas.set_temp_cursor(cursor)

	def mouse_move(self, event):
		if self.draw:
			self.end = event.pos()
			self.canvas.draw_frame(self.start, self.end)

	def mouse_up(self, event):
		if event.button() == Qt.Qt.LeftButton:
			self.canvas.stop_draw_frame()
			self.end = event.pos()
			self.draw = False
			if self.start and self.end:
				change = self.end - self.start
				if abs(change.x()) < 5 and abs(change.y()) < 5:
					self.canvas.zoom_at_point(self.start, ZOOM_IN)
				else:
					self.canvas.zoom_to_rectangle(self.start, self.end)
			self.end = []
			self.start = []
		elif event.button() == Qt.Qt.RightButton:
			if not self.draw:
				self.canvas.zoom_at_point(self.start, ZOOM_OUT)
				self.canvas.restore_cursor()


class FleurController(AbstractController):

	viewport = None

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)

	def mouse_down(self, event):
		self.start = [event.x(), event.y()]

	def mouse_up(self, event):
		self.start = []
		self.end = []

	def mouse_move(self, event):
		if self.start:
			self.end = [event.x(), event.y()]
			dx = self.end[0] - self.start[0]
			dy = self.end[1] - self.start[1]
			hb = self.canvas.horizontalScrollBar()
			vb = self.canvas.verticalScrollBar()
			hb.setValue(hb.value() - dx)
			vb.setValue(vb.value() - dy)
			self.start = self.end

class SelectController(AbstractController):

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)
		self.select = False

	def mouse_down(self, event):
		if event.button() == Qt.Qt.LeftButton:
			self.start = event.pos()
			self.select = True

	def mouse_up(self, event):
		if event.button() == Qt.Qt.LeftButton:
			self.canvas.stop_draw_frame()
			self.end = event.pos()
			self.select = False
			change = self.end - self.start
			if abs(change.x()) < 3 and abs(change.y()) < 3:
				self.canvas.select_at_point(self.start, event.modifiers())
				if self.canvas.mouse_over_selection(event.pos()):
					self.canvas.set_mode(modes.MOVE_MODE)
				return
			self.canvas.select_in_rect(self.start, self.end, event.modifiers())
			self.end = []
			self.start = []
		elif not self.select and event.button() == Qt.Qt.RightButton:
			self.canvas.selection.clear()

	def mouse_move(self, event):
		if self.canvas.selection.items:
			if not self.select and self.canvas.mouse_over_selection(event.pos()):
				self.canvas.set_mode(modes.MOVE_MODE)
		if self.select:
			self.end = event.pos()
			self.canvas.draw_frame(self.start, self.end)

class MoveController(AbstractController):
	start = None
	end = None

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)
		self.move = False
		self.moved = False
		self.copy = False

	def mouse_down(self, event):
		if event.button() == Qt.Qt.LeftButton:
			self.start = event.pos()
			self.move = True
			self.canvas.show_move_frame()

	def mouse_move(self, event):
		if self.move:
			self.moved = True
			self.end = event.pos()
			mod = event.modifiers()
			if int(mod & QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier:
				change = self.end - self.start
				if abs(change.x()) > abs(change.y()):
					change.setY(0)
				else:
					change.setX(0)
				self.end = change + self.start
			self.canvas.draw_move_frame(self.start, self.end)
		else:
			if not self.canvas.mouse_over_selection(event.pos()):
				self.canvas.set_mode()

	def mouse_up(self, event):
		if self.move and event.button() == Qt.Qt.LeftButton:
			self.canvas.hide_move_frame()
			self.move = False
			if self.moved:
				self.canvas.apply_move(self.start, self.end, self.copy)
				self.canvas.restore_cursor()
			else:
				self.canvas.sel_item.setVisible(True)
				self.canvas.sel_item.refresh()
			self.moved = False
			self.copy = False
		elif self.moved and event.button() == Qt.Qt.RightButton:
			self.copy = True
			cursor = self.app.canvas_cursors[modes.COPY_MODE]
			self.canvas.set_temp_cursor(cursor)

