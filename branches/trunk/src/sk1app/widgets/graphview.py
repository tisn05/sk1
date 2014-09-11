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

import math

from PyQt4 import QtCore, QtGui, Qt

from uc2.uc_conf import mm_to_pt
from uc2.sk1doc import model

from sk1app import events
from sk1app import modes
from viewitems import special

WORKSPACE_HEIGHT = 2000 * mm_to_pt
WORKSPACE_WIDTH = 4000 * mm_to_pt

PAGEFIT = 0.9
ZOOM_IN = 1.25
ZOOM_OUT = 0.8


class GVCanvas(QtGui.QGraphicsView):

	mode = None
	temporal = False
	stored_mode = None

	def __init__(self, parent, presenter):

		QtGui.QGraphicsView.__init__(self)
		self.parent = parent
		self.presenter = presenter
		self.eventloop = presenter.eventloop
		self.app = parent.app

		self.scene = QtGui.QGraphicsScene(self)
		self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
		self.scene.setSceneRect(-WORKSPACE_WIDTH / 2.0, -WORKSPACE_HEIGHT / 2.0,
						WORKSPACE_WIDTH, WORKSPACE_HEIGHT)
		self.scene.setSortCacheEnabled(True)
		self.setAutoFillBackground(True)
		self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
		self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
		self.setFrameStyle(self.Plain)
		self.setViewportMargins(0, 0, -2, -2)

		self.setScene(self.scene)
		self.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
		self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
		self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
		self.setMatrix(QtGui.QMatrix(1.0, 0.0, 0.0, -1.0, 0.0, 0.0))
		self.scale(0.8, 0.8)
		self.setRenderHint(QtGui.QPainter.Antialiasing, True)

		self.selframe = special.SelectFrame(self)
		self.scene.addItem(self.selframe)
		self.selection = presenter.selection
		self.sel_item = special.SelectionItem(self, self.selection)
		self.scene.addItem(self.sel_item)
		self.setMinimumSize(400, 300)
		self.wait_cursor = Qt.Qt.WaitCursor


	def set_mode(self, mode=modes.SELECT_MODE):
		if not self.mode == mode:
			self.mode = mode
			self.controller = self.controllers[self.mode]
			self.viewport().setCursor(self.app.canvas_cursors[self.mode])
			events.emit(events.MODE_CHANGED, mode)

	def set_temp_mode(self, mode):
		if not self.mode == mode:
			self.stored_mode = self.mode
			self.mode = mode
			self.controller = self.controllers[self.mode]
			self.viewport().setCursor(self.app.canvas_cursors[self.mode])

	def set_temp_cursor(self, cursor):
		self.viewport().setCursor(cursor)

	def restore_cursor(self):
		self.viewport().setCursor(self.app.canvas_cursors[self.mode])

	def restore_mode(self):
		if not self.stored_mode is None:
			self.mode = self.stored_mode
			self.stored_mode = None
			self.controller = self.controllers[self.mode]
			self.viewport().setCursor(self.app.canvas_cursors[self.mode])

	def set_controllers(self, controllers):
		self.controllers = controllers


#==============APPLICATION LEVEL METHODS==========================
	def get_factor(self):
		return self.matrix().m11()

	def drawBackground(self, painter, rect):
		pass

	def drawForeground(self, painter, rect):
		pass

	def scaleView(self, scaleFactor):
		f = self.matrix().scale(scaleFactor, scaleFactor)
		factor = f.mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

		if factor < 0.07 or factor > 100:
			return

		self.scale(scaleFactor, scaleFactor)

	def viewportEvent(self, event):
		self.eventloop.emit(self.eventloop.VIEW_CHANGED)
		return QtGui.QGraphicsView.viewportEvent(self, event)


	def zoom_in(self):
		self.scaleView(ZOOM_IN)

	def zoom_out(self):
		self.scaleView(ZOOM_OUT)

	def zoom_area(self):
		pass

	def zoom_100(self):
		self.scaleView(1 / self.get_factor())

	def fit_to_page(self):
		self.zoom_100()
		vp = self.viewport()
		width, height = [vp.width(), vp.height()]
		w, h = self.presenter.get_page_size()
		scale = min(PAGEFIT * width / w, PAGEFIT * height / h)
		self.scaleView(scale)
		self.centerOn(0.0, 0.0)

	def zoom_at_point(self, point, zoom):
		point = self.mapToScene(point)
		self.scaleView(zoom)
		self.centerOn(point)

	def zoom_selected(self):
		rect = self.sel_item.boundingRect()
		center = rect.center()
		self.zoom_100()
		vp = self.viewport()
		width, height = [vp.width(), vp.height()]
		w, h = [rect.width(), rect.height()]
		scale = min(width / w, height / h)
		self.scaleView(PAGEFIT * scale)
		self.centerOn(center)

	def zoom_previous(self):
		self.scaleView(ZOOM_OUT / 1.5)

	def zoom_to_rectangle(self, p0, p1):
		rect = QtCore.QRect(p0, p1).normalized()
		center = self.mapToScene(rect.center())
		view = self.rect()
		coef = min(float(view.width())/float(rect.width()),
				float(view.height())/float(rect.height()))
		self.scaleView(coef)
		self.centerOn(center)
		
	def create_rectangle(self, p0, p1):	
		p0 = self.mapToScene(p0)
		p1 = self.mapToScene(p1)
		rect = QtCore.QRectF(p0, p1).normalized()
		self.presenter.api.create_rectangle(rect)

	def draw_frame(self, p0, p1):
		self.selframe.set_rect(p0, p1)
		self.selframe.setVisible(True)

	def stop_draw_frame(self):
		self.selframe.setVisible(False)

	def select_at_point(self, point, modifiers):
		result = []
		items = self.items(point)
		for item in items:
			if item.obj.cid > model.SELECTABLE_CLASS:
				result.append(item)
				break
		if int(modifiers & QtCore.Qt.ShiftModifier) == QtCore.Qt.ShiftModifier:
			self.selection.add_items_to_selection(result)
		else:
			self.selection.set_items_to_selection(result)

	def select_in_rect(self, p0, p1, modifiers):
		result = []
		rect = QtCore.QRect(p0, p1).normalized()
		items = self.items(rect, Qt.Qt.ContainsItemShape)
		for item in items:
			if item.obj.cid > model.SELECTABLE_CLASS:
				result.append(item)
		result.reverse()
		if int(modifiers & QtCore.Qt.ShiftModifier) == QtCore.Qt.ShiftModifier:
			self.selection.add_items_to_selection(result)
		else:
			self.selection.set_items_to_selection(result)

	def select_all(self):
		result = []
		items = self.items()
		for item in items:
			if item.type() > model.SELECTABLE_CLASS + QtGui.QGraphicsItem.UserType:
				result.append(item)
		result.reverse()
		self.selection.set_items_to_selection(result)

	def deselect(self):
		self.selection.clear()

	def mouse_over_selection(self, point):
		result = False
		point = self.mapToScene(point)
		if self.sel_item.contains(point):
			for item in self.selection.items:
				if item.contains(point):
					result = True
					break
		return result

	def show_move_frame(self):
		self.sel_item.setVisible(False)
		self.selframe.set_rect_by_rect(self.sel_item.bbox())
		self.selframe.setVisible(True)

	def draw_move_frame(self, start, end):
		start = self.mapToScene(start)
		end = self.mapToScene(end)
		self.selframe.setPos(self.selframe.position + end - start)

	def hide_move_frame(self):
		self.selframe.setVisible(False)
		self.selframe.setPos(QtCore.QPointF(0, 0))

	def apply_move(self, start, end, flag):
		start = self.mapToScene(start)
		end = self.mapToScene(end)
		change = end - start
		matrix = Qt.QMatrix(1.0, 0.0, 0.0, 1.0, change.x(), change.y())
		self.presenter.api.transform_selection(matrix, flag)
		self.sel_item.setVisible(True)
		self.sel_item.refresh()

#==============EVENT CONTROLLING==========================
	def mouseDoubleClickEvent(self, event):
		QtGui.QGraphicsView.mouseDoubleClickEvent(self, event)

	def mouseMoveEvent(self, event):
		self.controller.mouse_move(event)

	def mousePressEvent(self, event):
		if event.button() == Qt.Qt.MidButton and \
			not self.mode == modes.FLEUR_MODE:
			if self.stored_mode is None:
				self.set_temp_mode(modes.FLEUR_MODE)
		self.controller.mouse_down(event)

	def mouseReleaseEvent(self, event):
		self.controller.mouse_up(event)
		if not self.stored_mode is None:
			self.restore_mode()

	def wheelEvent(self, event):
		self.controller.wheel(event)

	def keyPressEvent(self, event):
		QtGui.QGraphicsView.keyPressEvent(self, event)

	def keyReleaseEvent(self, event):
		QtGui.QGraphicsView.keyReleaseEvent(self, event)
