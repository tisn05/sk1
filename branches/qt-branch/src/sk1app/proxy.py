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

from sk1app import modes 
from sk1app import events

class AppProxy:
	
	app = None
	
	def __init__(self, app):
		self.app = app
		
	def do_undo(self):
		self.app.current_doc.api.do_undo()
		
	def do_redo(self):
		self.app.current_doc.api.do_redo()
		
	def clear_history(self):		
		self.app.current_doc.api.clear_history()
		
	def delete_selection(self):
		self.app.current_doc.api.delete_selection()
		
	def copy_selection(self):
		self.app.current_doc.api.copy_selection()
		events.emit(events.CLIPBOARD)
		
	def cut_selection(self):
		self.app.current_doc.api.cut_selection()
		events.emit(events.CLIPBOARD)
		
	def paste_from_clipboard(self):
		self.app.current_doc.api.paste_from_clipboard()
		
	def select_all(self):
		self.app.current_doc.view.select_all()
		
	def deselect(self):
		self.app.current_doc.view.deselect()
		
	def zoom_in(self):
		self.app.current_doc.view.zoom_in()

	def zoom_out(self):
		self.app.current_doc.view.zoom_out()

	def zoom_area(self):
		if self.app.current_doc.view.stored_mode is None:
			self.app.current_doc.view.set_temp_mode(modes.ZOOM_MODE)

	def zoom_100(self):
		self.app.current_doc.view.zoom_100()

	def fit_to_page(self):
		self.app.current_doc.view.fit_to_page()

	def zoom_selected(self):
		self.app.current_doc.view.zoom_selected()

	def zoom_previous(self):
		self.app.current_doc.view.zoom_previous()
