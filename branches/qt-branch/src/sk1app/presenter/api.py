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

from PyQt4 import QtCore, Qt

from sk1app import events
from uc2.sk1doc import model
from sk1app.widgets.viewitems import CID_TO_ITEM

class PresenterAPI:

	presenter = None
	view = None
	methods = None
	model = None
	app = None
	eventloop = None
	undo = []
	redo = []
	undo_marked = False
	view_items = {}

	def __init__(self, presenter):
		self.presenter = presenter
		self.methods = self.presenter.methods
		self.model = presenter.model
		self.view = presenter.view

		self.view_items = presenter.view_items
		self.eventloop = presenter.eventloop
		self.app = presenter.app
		self.undo = []
		self.redo = []

	def do_undo(self):
		canvas = self.presenter.view
		canvas.set_temp_cursor(canvas.wait_cursor)
		transaction_list = self.undo[-1][0]
		for transaction in transaction_list:
			self._do_action(transaction)
		tr = self.undo[-1]
		self.undo.remove(tr)
		self.redo.append(tr)
		self.eventloop.emit(self.eventloop.DOC_MODIFIED)
		if self.undo and self.undo[-1][2]:
			self.presenter.reflect_saving()
		if not self.undo and not self.undo_marked:
			self.presenter.reflect_saving()
		if self.presenter.selection.items:
			self.view.sel_item.refresh()
		canvas.restore_cursor()	

	def do_redo(self):
		canvas = self.presenter.view
		canvas.set_temp_cursor(canvas.wait_cursor)
		transaction_list = self.redo[-1][1]
		for transaction in transaction_list:
			self._do_action(transaction)
		tr = self.redo[-1]
		self.redo.remove(tr)
		self.undo.append(tr)
		self.eventloop.emit(self.eventloop.DOC_MODIFIED)
		if not self.undo or self.undo[-1][2]:
			self.presenter.reflect_saving()
		if self.presenter.selection.items:
			self.view.sel_item.refresh()
		canvas.restore_cursor()	

	def _do_action(self, action):
		if not action: return
		if len(action) == 1:
			action[0]()
		elif len(action) == 2:
			action[0](action[1])
		elif len(action) == 3:
			action[0](action[1], action[2])
		elif len(action) == 4:
			action[0](action[1], action[2], action[3])
		elif len(action) == 5:
			action[0](action[1], action[2], action[3], action[4])
		elif len(action) == 6:
			action[0](action[1], action[2], action[3], action[4], action[5])

	def add_undo(self, transaction):
		self.redo = []
		self.undo.append(transaction)
		self.eventloop.emit(self.eventloop.DOC_MODIFIED)

	def save_mark(self):
		for item in self.undo:
			item[2] = False
		for item in self.redo:
			item[2] = False

		if self.undo:
			self.undo[-1][2] = True
			self.undo_marked = True

	def clear_history(self):
		self.undo = []
		self.redo = []
		events.emit(events.DOC_CHANGED, self.presenter)

	def set_doc_origin(self, origin):
		cur_origin = self.model.doc_origin
		transaction = [
			[[self.methods.set_doc_origin, cur_origin]],
			[[self.methods.set_doc_origin, origin]],
			False]
		self.methods.set_doc_origin(origin)
		self.add_undo(transaction)

	def update_zvalue(self, parent, index=0):
		for object in parent.childs[index:]:
			item = self.view_items[object]
			item.setZValue(parent.childs.index(object))

	def _delete_object(self, obj):
		parent = obj.parent
		obj_item = self.view_items[obj]

		self.methods.delete_object(obj)
		self.view.scene.removeItem(obj_item)
		self.view_items[obj] = None

		if obj_item in self.presenter.selection.items:
			self.presenter.selection.item_remove(obj_item)
		self.update_zvalue(parent)

	def delete_object(self, obj):
		parent = obj.parent
		index = parent.childs.index(obj)
		self._delete_object(obj)
		transaction = [
			[[self._insert_object, obj, parent, index]],
			[[self._delete_object, obj]],
			False]
		self.add_undo(transaction)

	def _delete_objects(self, objs):
		objs_data = []
		parents = []
		for obj in objs:
			parent = obj.parent
			index = parent.childs.index(obj)
			obj_item = self.view_items[obj]
			objs_data.append([obj, obj_item, parent, index])
		for obj, obj_item, parent, index in objs_data:
			self.methods.delete_object(obj)
			if obj_item in self.presenter.selection.items:
				self.presenter.selection.quiet_item_remove(obj_item)
			self.view.scene.removeItem(obj_item)
			self.view_items[obj] = None
			if not parent in parents:
				parents.append(parent)
		for parent in parents:
			self.update_zvalue(parent)
		self.presenter.selection.update()
		objs_data.reverse()
		return objs_data

	def insert_object(self, obj, obj_item, parent, index):
		self._insert_object(obj, obj_item, parent, index)
		obj_item = self.view_items[obj]
		transaction = [
			[[self._delete_object, obj]],
			[[self._insert_object, obj, obj_item, parent, index]],
			False]
		self.add_undo(transaction)

	def _insert_object(self, obj, obj_item, parent, index):
		self.methods.insert_object(obj, parent, index)
		if obj_item is None:
			obj_item = CID_TO_ITEM[obj.cid](self.view, obj)
		parent_item = self.view_items[parent]
		obj_item.setParentItem(parent_item)
		self.view_items[obj] = obj_item
		self.update_zvalue(obj.parent)
		self.presenter.selection.set_items_to_selection([obj_item])

	def _insert_objects(self, objs_data):
		items = []
		parents = []
		for obj, obj_item, parent, index in objs_data:
			self.methods.insert_object(obj, parent, index)
			if obj_item is None:
				obj_item = CID_TO_ITEM[obj.cid](self.view, obj)
			parent_item = self.view_items[parent]
			obj_item.setParentItem(parent_item)
			self.view_items[obj] = obj_item
			if not parent in parents:
				parents.append(parent)
		for parent in parents:
			self.update_zvalue(parent)
		data_objs = [] + objs_data
		data_objs.reverse()
		for obj, obj_item, parent, index in data_objs:
			items.append(self.view_items[obj])
		self.presenter.selection.set_items_to_selection(items)

	def _append_objects(self, objs_data):
		items = []
		for obj, obj_item, parent, index in objs_data:
			self.methods.insert_object(obj, parent, index)
			if obj_item is None:
				obj_item = CID_TO_ITEM[obj.cid](self.view, obj)
			parent_item = self.view_items[parent]
			obj_item.setParentItem(parent_item)
			self.view_items[obj] = obj_item
		data_objs = [] + objs_data
		data_objs.reverse()
		for obj, obj_item, parent, index in data_objs:
			items.append(self.view_items[obj])
			self.view_items[obj].setZValue(parent.childs.index(obj))
		self.presenter.selection.set_items_to_selection(items)

	def delete_selection(self):
		canvas = self.presenter.view
		canvas.set_temp_cursor(canvas.wait_cursor)
		objs = [] + self.presenter.selection.objs
		objs_data = self._delete_objects(objs)
		transaction = [
			[[self._insert_objects, objs_data]],
			[[self._delete_objects, objs]],
			False]
		self.add_undo(transaction)
		canvas.restore_cursor()

	def copy_selection(self):
		objs = [] + self.presenter.selection.objs
		result = []
		for obj in objs:
			result.append(obj.copy())
		self.app.clipboard = result

	def cut_selection(self):
		self.copy_selection()
		self.delete_selection()

	def paste_from_clipboard(self):
		canvas = self.presenter.view
		canvas.set_temp_cursor(canvas.wait_cursor)
		objs = []
		objs_data = []
		parent = self.presenter.active_layer
		index = len(parent.childs)
		for obj in self.app.clipboard:
			obj_copy = obj.copy()
			objs_data.append([obj_copy, None, parent, index])
			objs.append(obj_copy)
		objs_data.reverse()
		objs.reverse()
		self._append_objects(objs_data)
		transaction = [
			[[self._delete_objects, objs]],
			[[self._insert_objects, objs_data]],
			False]
		self.add_undo(transaction)
		canvas.restore_cursor()

	def _apply_trafo(self, items, matrix):
		for item in items:
			item.apply_trafo(matrix)

	def transform_selection(self, matrix, copy=False):
		canvas = self.presenter.view
		canvas.set_temp_cursor(canvas.wait_cursor)
		if copy:
			objs = []
			objs_data = []
			parent = self.presenter.active_layer
			index = len(parent.childs)
			for obj in self.presenter.selection.objs:
				obj_copy = obj.copy()
				objs_data.append([obj_copy, None, parent, index])
				objs.append(obj_copy)
			objs_data.reverse()
			objs.reverse()
			self._append_objects(objs_data)
			items = [] + self.presenter.selection.items
			self._apply_trafo(items, matrix)
			objs = []
			objs_data = []
			for obj in self.presenter.selection.objs:
				parent = obj.parent
				index = parent.childs.index(obj)
				item = self.view_items[obj]
				objs_data.append([obj, item, parent, index])
				objs.append(obj)				
			transaction = [
				[[self._delete_objects, objs]],
				[[self._insert_objects, objs_data]],
				False]
			self.add_undo(transaction)	
		else:
			redo_matrix = Qt.QMatrix(1.0 / matrix.m11(), -matrix.m12(),
									- matrix.m21(), 1.0 / matrix.m22(),
									- matrix.dx(), -matrix.dy())
			items = [] + self.presenter.selection.items
			self._apply_trafo(items, matrix)
			transaction = [
				[[self._apply_trafo, items, redo_matrix]],
				[[self._apply_trafo, items, matrix]],
				False]
			self.add_undo(transaction)
		canvas.restore_cursor()	


	def create_rectangle(self, rect):
		rect = [rect.x(), rect.y(), rect.width(), rect.height()]
		config = self.app.config
		parent = self.presenter.active_layer
		obj = model.Rectangle(config, parent, rect)
		index = len(parent.childs)
		self.insert_object(obj, None, parent, index)


