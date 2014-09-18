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

import gtk

from sk1 import config, events, rc
from sk1.ui.menubar import AppMenubar
from sk1.ui.toolbar import AppToolbar
from sk1.ui.tools import AppTools
from sk1.ui.palette import HPalette
from sk1.ui.statusbar import AppStatusbar
from sk1.context import ContextPanel
from sk1.plugins import PluginPanel
from sk1.widgets import HidableArea

class MainWindow(gtk.Window):

	canvas = None
	doc_index = 1

	def __init__(self, app):

		gtk.Window.__init__(self)
		self.app = app

		vbox = gtk.VBox(False, 0)

		self.mb = AppMenubar(self)
		vbox.pack_start(self.mb, False, False, 0)

		self.toolbar = AppToolbar(self)
		vbox.pack_start(self.toolbar, False, False, 0)

		#---CENTRAL PART
		self.workarea = HidableArea()

		self.workarea.box.pack_start(gtk.HSeparator(), False, False, 0)
		self.ctx_bar = ContextPanel(self)
		self.workarea.box.pack_start(self.ctx_bar, False, False, 0)
		self.workarea.box.pack_start(gtk.HSeparator(), False, False, 0)

		hbox = gtk.HBox(False, 0)
		self.tools = AppTools(self)
		hbox.pack_start(self.tools, False, False, 1)
		self.inner_hpaned = gtk.HPaned()
		self.nb = gtk.Notebook()
		self.nb.connect('switch-page', self.change_doc)
		self.nb.set_property('scrollable', True)
		self.inner_hpaned.pack1(self.nb, 1, 0)

		self.plugin_panel = PluginPanel(self)

		hbox.pack_start(self.inner_hpaned, True, True, 1)
		self.workarea.box.pack_start(hbox , True, True, 0)
		vbox.pack_start(self.workarea , True, True, 0)

		#---SPLASH
		self.nb_splash = SplashArea(self)
		self.workarea.box2.pack_start(self.nb_splash , True, True, 0)
		#---CENTRAL PART END

		self.hpalette = HPalette(self)
		self.workarea.box.pack_start(self.hpalette, False, False, 2)

		self.statusbar = AppStatusbar(self)
		vbox.pack_end(self.statusbar, False, False, 0)

		vbox.pack_end(gtk.HSeparator(), False, False, 0)

		self.add(vbox)
		self.set_win_title()
		self.set_size_request(config.mw_min_width, config.mw_min_height)
		if config.mw_store_size:
			self.set_default_size(config.mw_width, config.mw_height)
		self.set_position(gtk.WIN_POS_CENTER)
		self.connect("delete-event", self.exit)
		self.add_accel_group(self.app.accelgroup)
		self.set_icon_from_file(rc.get_image_path(rc.IMG_APP_ICON))

		self.show_all()
		if config.mw_maximized:
			self.window.maximize()

	def exit(self, *args):
		if self.app.exit():
			return False
		else:
			return True

	def set_win_title(self, docname=''):
		if docname:
			title = '[%s] - %s' % (docname, self.app.appdata.app_name)
			self.set_title(title)
		else:
			self.set_title(self.app.appdata.app_name)

	def add_tab(self, da):
		if not self.nb.get_n_pages():
			self.workarea.set_visible(True)
		index = self.nb.append_page(da, da.tab_caption)
		da.show_all()
		self.nb.show_all()
		self.nb.set_current_page(index)
		self.set_win_title(da.presenter.doc_name)

	def remove_tab(self, tab):
		self.nb.remove_page(self.nb.page_num(tab))
		if not self.nb.get_n_pages():
			self.set_win_title()
			self.app.current_doc = None
			self.workarea.set_visible(False)

	def change_doc(self, *args):
		da = self.nb.get_nth_page(args[2])
		self.app.current_doc = da.presenter
		self.set_win_title(da.caption)
		events.emit(events.DOC_CHANGED, self)

	def set_tab_title(self, tab, title):
		tab.set_caption(title)
		if self.nb.page_num(tab) == self.nb.get_current_page():
			self.set_win_title(title)

	def set_active_tab(self, tab):
		self.nb.set_current_page(self.nb.page_num(tab))


class SplashArea(gtk.DrawingArea):

	def __init__(self, mw):
		gtk.DrawingArea.__init__(self)
		self.mw = mw
		self.nodocs_color = self.mw.get_style().fg[gtk.STATE_INSENSITIVE]
		self.modify_bg(gtk.STATE_NORMAL, self.nodocs_color)

		r = self.nodocs_color.red / 0xff
		g = self.nodocs_color.green / 0xff
		b = self.nodocs_color.blue / 0xff
		self.pixel = r * 256 * 256 * 256 + g * 65536 + b * 256 + 255

		self.banner = rc.get_pixbuf(rc.IMG_CAIRO_BANNER)
		self.connect('expose_event', self.repaint)

	def repaint(self, *args):
		if config.show_cairo_splash:
			h = self.allocation[3]
			self.composite(self.banner, 5, h - self.banner.get_height() - 5)

	def composite(self, banner, x, y):
		frame = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8,
            banner.get_width(),
            banner.get_height())

		frame.fill(self.pixel)
		banner.composite(
			frame,
			0, 0,
            banner.get_width(),
            banner.get_height(),
            0, 0, 1, 1, gtk.gdk.INTERP_NEAREST, 255)

		self.window.draw_rgb_image(
            self.style.black_gc,
            x, y,
            frame.get_width(),
            frame.get_height(),
            gtk.gdk.RGB_DITHER_NORMAL,
            frame.get_pixels(),
            frame.get_rowstride())



