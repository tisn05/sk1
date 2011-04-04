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

from sk1app import events

class Selection:

	objs = []
	items = []
	view_item = None
	cid = 3

	def __init__(self, presenter):
		self.presenter = presenter
		self.app = presenter.app
		self.objs = []
		self.items = []

	def update(self):
		self.view_item.refresh()
		eventloop = self.presenter.eventloop
		eventloop.emit(eventloop.SELECTION_CHANGED)
		msg = self.app.tr('object(s) in selection')
		msg = '%i %s'%(len(self.objs), msg)
		events.emit(events.APP_STATUS, msg)
		
	def object_remove(self, obj):
		self.quiet_object_remove(obj)
		self.update()
	
	def quiet_object_remove(self, obj):
		self.objs.remove(obj)
		self.items.remove(self.presenter.view_items[obj])
		
	def objects_remove(self, objs):
		self.quiet_object_remove(objs)
		self.update()
	
	def quiet_objects_remove(self, objs):
		for obj in objs:
			self.quiet_object_remove(obj)
		
	def item_remove(self, item):
		self.quiet_item_remove(item)
		self.update()
	
	def quiet_item_remove(self, item):
		self.items.remove(item)
		self.objs.remove(item.obj)	

	def object_insert(self, obj, index):
		self.quiet_object_insert(obj, index)
		self.update()
	
	def quiet_object_insert(self, obj, index):
		self.objs.insert(index, obj)
		self.items.insert(index, self.presenter.view_items[obj])
		
	def item_insert(self, item, index):
		self.quiet_item_insert(item, index)
		self.update()
	
	def quiet_item_insert(self, item, index):
		self.objs.insert(index, item.obj)
		self.items.insert(index, item)

	def set_selection(self, objs):
		pass

	def add_to_selection(self, objs):
		pass

	def set_items_to_selection(self, items):
		if len(items)==1 and items[0] in self.items:
			return
		self.items = items
		self.objs = []
		for item in items:
			self.objs.append(item.obj)
		self.update()

	def add_items_to_selection(self, items):
		for item in items:
			if item in self.items:
				self.items.remove(item)
				self.objs.remove(item.obj)
			else:
				self.items.append(item)
				self.objs.append(item.obj)
		self.update()
		
	def clear(self):
		self.objs = []
		self.items = []
		self.update()
