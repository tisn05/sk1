# -*- coding: utf-8 -*-
#
#	Copyright (C) 2011-2014 by Igor E. Novikov
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

import gtk, gconst

from boxes import VBox, HBox

class MainWindow(gtk.Window):

	def __init__(self, horizontal=False):
		gtk.Window.__init__(self)
		if horizontal:
			self.box = HBox()
		else:
			self.box = VBox()
		self.build()
		self.add(self.box)
		self.connect(gconst.EVENT_DELETE, self.exit)
		self.show_all()

	def build(self):pass

	def exit(self, *args):return True

	def pack(self, child, expand=False, fill=False, padding=0, end=False):
		self.box.pack(child, expand, fill, padding, end)

	def center(self):
		self.set_position(gtk.WIN_POS_CENTER)
