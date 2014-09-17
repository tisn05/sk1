# -*- coding: utf-8 -*-
#
#	Copyright (C) 2013 by Igor E. Novikov
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

import gtk

from sk1 import appconst
from sk1.widgets import PangoLabel
from sk1.resources.images import get_pixbuf, get_stock_pixbuf

class GenericPrefsPlugin(gtk.VBox):

	app = None
	name = ''
	title = ''
	short_title = ''
	icon_stock = gtk.STOCK_FILE
	icon_file = ''
	icon = None
	cid = appconst.PREFS_APP_PLUGIN
	childs = []
	built = False
	leaf = True

	def __init__(self, app, dlg, pdxf_config):
		gtk.VBox.__init__(self)
		self.pdxf_config = pdxf_config
		self.app = app
		self.dlg = dlg
		if self.icon_file:
			self.icon = get_pixbuf(self.icon_file)
		else:
			self.icon = get_stock_pixbuf(self.icon_stock, gtk.ICON_SIZE_MENU)

	def build(self):
		title = PangoLabel(self.title, appconst.TXT_LARGE, True)
		self.pack_start(title, False, False, 0)
		self.pack_start(gtk.HSeparator(), False, False, 5)
		self.built = True
		self.set_border_width(5)
		self.set_size_request(400, -1)

	def apply_changes(self):pass
	def restore_defaults(self):pass