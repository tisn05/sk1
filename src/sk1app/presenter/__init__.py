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

import os
import sys

from PyQt4 import Qt, QtGui
from uc2.presenter import UCDocPresenter

from sk1app import events
from sk1app.drawingarea import DrawingArea
from sk1app import modes
from sk1app.widgets import viewitems

import controllers
import creators

from api import PresenterAPI
from eventloop import EventLoop
from selection import Selection



class DocumentPresenter(UCDocPresenter):

	selection = None
	view = None
	view_items = {}
	view_root = None
	eventloop = None

	drawingarea = None
	subwindow = None
	doc_file = ''
	doc_name = ''
	cms = None

	saved = True
	tabbed_flag = False

	def __init__(self, app, doc_file=''):

		UCDocPresenter.__init__(self, app.config, app.appdata)
		self.app = app
		self.eventloop = EventLoop(self)


		if doc_file:
			self.load(doc_file)
			self.doc_name = os.path.basename(self.doc_file)
		else:
			self.new()
			self.doc_name = self.app.get_new_docname()

		self.cms = self.app.default_cms

		self.view_items = {}
		self.api = PresenterAPI(self)
		self.selection = Selection(self)
		self.drawingarea = DrawingArea(self.app.mw.mdiArea, self.app, self)
		self.subwindow = self.app.mw.mdiArea.addSubWindow(self.drawingarea)

		self.view = self.drawingarea.canvas
		self.api.view = self.view
		self.view.set_controllers(self.init_controllers())
		self.view.set_mode()
		self.init_view()

		self.set_title()

		if self.app.inspector.is_not_doc():
			if not self.app.config.interface_type:
				self.app.mw.set_windowed_interface()
				self.tabbed_flag = True

		self.subwindow.setWindowIcon(self.app.appdata.doc_icon)
		self.subwindow.resize(500, 400)
		self.subwindow.setMinimumSize(500, 400)
		self.subwindow.showMaximized()
		self.subwindow.show()

		if self.tabbed_flag:
			self.app.mw.set_tab_interface()
			self.tabbed_flag = False

		self.view.fit_to_page()
		self.eventloop.connect(self.eventloop.DOC_MODIFIED, self.modified)
		self.eventloop.connect(self.eventloop.SELECTION_CHANGED, self.sel_changed)

	def modified(self, *args):
		self.saved = False
		self.set_title()
		self.app.events.emit(self.app.events.DOC_MODIFIED, self)
		
	def sel_changed(self, *args):
		self.app.events.emit(self.app.events.SELECTION_CHANGED, self)

	def save(self):
		try:
			if self.app.config.make_backup:
				if os.path.lexists(self.doc_file):
					if os.path.lexists(self.doc_file + '~'):
						os.remove(self.doc_file + '~')
					os.rename(self.doc_file, self.doc_file + '~')
			UCDocPresenter.save(self, self.doc_file)
		except IOError:
			errtype, value, traceback = sys.exc_info()
			raise IOError(errtype, value, traceback)
		self.reflect_saving()

	def reflect_saving(self):
		self.saved = True
		self.set_title()
		self.api.save_mark()
		self.app.events.emit(self.app.events.DOC_SAVED, self)

	def close(self):
		if self.subwindow:
			self.app.mw.mdiArea.removeSubWindow(self.subwindow)
		UCDocPresenter.close(self)

	def set_doc_file(self, doc_file, doc_name=''):
		self.doc_file = doc_file
		if doc_name:
			self.doc_name = doc_name
		else:
			self.doc_name = os.path.basename(self.doc_file)
		self.set_title()

	def set_title(self):
		if self.saved:
			self.subwindow.setWindowTitle(self.doc_name)
		else:
			self.subwindow.setWindowTitle(self.doc_name + '*')
		self.app.mw.set_title()

	def init_controllers(self):
		dummy = controllers.AbstractController(self.view, self)
		ctrls = {
			modes.SELECT_MODE: controllers.SelectController(self.view, self),
			modes.SHARPER_MODE: dummy,
			modes.ZOOM_MODE: controllers.ZoomController(self.view, self),
			modes.FLEUR_MODE: controllers.FleurController(self.view, self),
			modes.LINE_MODE: dummy,
			modes.CURVE_MODE: dummy,
			modes.RECT_MODE: creators.RectangleCreator(self.view, self),
			modes.ELLIPSE_MODE: dummy,
			modes.TEXT_MODE: dummy,
			modes.POLYGON_MODE: dummy,
			modes.MOVE_MODE: controllers.MoveController(self.view, self)
		}
		return ctrls

	def init_view(self):
		dict = viewitems.CID_TO_ITEM
		self.view_root = dict[self.model.cid](self.view, self.model)
		self.view_items[self.model] = self.view_root
		self.build_viewtree(self.view_root, dict)
		self.view.scene.addItem(self.view_root)		

	def build_viewtree(self, parent, dict):
		if parent.obj.childs:
			for child in parent.obj.childs:
				item = dict[child.cid](self.view, child)
				self.view_items[child] = item
				item.setParentItem(parent)
				self.build_viewtree(item, dict)
				item.setZValue(parent.obj.childs.index(child))

