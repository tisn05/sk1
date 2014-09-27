# -*- coding: utf-8 -*-
#
#	Copyright (C) 2013-2014 by Igor E. Novikov
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

import gtk

from sk1 import const, rc
from sk1.widgets import PangoLabel

class GenericPrefsPlugin(gtk.VBox):

	app = None
	name = ''
	title = ''
	short_title = ''
	icon_stock = gtk.STOCK_FILE
	image_id = ''
	icon = None
	cid = const.PREFS_APP_PLUGIN
	childs = []
	built = False
	leaf = True

	def __init__(self, app, dlg, fmt_config):
		gtk.VBox.__init__(self)
		self.fmt_config = fmt_config
		self.app = app
		self.dlg = dlg
		if self.image_id:
			self.icon = rc.get_pixbuf(self.image_id)
		else:
			self.icon = rc.get_stock_pixbuf(self.icon_stock, gtk.ICON_SIZE_MENU)

	def build(self):
		title = PangoLabel(self.title, const.TXT_LARGE, True)
		self.pack_start(title, False, False, 0)
		self.pack_start(gtk.HSeparator(), False, False, 5)
		self.built = True
		self.set_border_width(5)
		self.set_size_request(400, -1)

	def apply_changes(self):pass
	def restore_defaults(self):pass