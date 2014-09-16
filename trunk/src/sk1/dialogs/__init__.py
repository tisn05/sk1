# -*- coding: utf-8 -*-
#
#	Copyright (C) 2011-2012 by Igor E. Novikov
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

import os, sys
import gtk, gobject

from uc2 import uc2const
from uc2.formats import data
from uc2.utils.fs import expanduser_unicode
from uc2 import events

from sk1 import _, config
from sk1.resources.images import load_image, IMG_APP_ICON

def _get_open_fiters():
	result = []
	descr = uc2const.FORMAT_DESCRIPTION
	ext = uc2const.FORMAT_EXTENSION
	items = [] + data.LOADER_FORMATS

	file_filter = gtk.FileFilter()
	file_filter.set_name(_('All supported formats'))
	for item in items:
		for extension in ext[item]:
			file_filter.add_pattern('*.' + extension)
			file_filter.add_pattern('*.' + extension.upper())
	result.append(file_filter)

	file_filter = gtk.FileFilter()
	file_filter.set_name(_('All files'))
	file_filter.add_pattern('*')
	result.append(file_filter)

	for item in items:
		file_filter = gtk.FileFilter()
		file_filter.set_name(descr[item])
		for extension in ext[item]:
			file_filter.add_pattern('*.' + extension)
			file_filter.add_pattern('*.' + extension.upper())
		result.append(file_filter)

	return result

def _get_image_fiters():
	result = []
	descr = uc2const.FORMAT_DESCRIPTION
	ext = uc2const.FORMAT_EXTENSION
	items = [] + uc2const.IMAGE_FORMATS
	for item in items:
		file_filter = gtk.FileFilter()
		file_filter.set_name(descr[item])
		for extension in ext[item]:
			file_filter.add_pattern('*.' + extension)
			file_filter.add_pattern('*.' + extension.upper())
		result.append(file_filter)

	file_filter = gtk.FileFilter()
	file_filter.set_name(_('All supported image formats'))
	for item in items:
		for extension in ext[item]:
			file_filter.add_pattern('*.' + extension)
			file_filter.add_pattern('*.' + extension.upper())
	result.append(file_filter)

	file_filter = gtk.FileFilter()
	file_filter.set_name(_('All files'))
	file_filter.add_pattern('*')
	result.append(file_filter)

	return result

def get_open_file_name(parent, app, start_dir, image=False):
	result = ''
	caption = _('Open file')
	if image: caption = _('Import image file')
	dialog = gtk.FileChooserDialog(caption,
				parent,
				gtk.FILE_CHOOSER_ACTION_OPEN,
				(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
					gtk.STOCK_OPEN, gtk.RESPONSE_OK))

	dialog.set_default_response(gtk.RESPONSE_OK)
	start_dir = expanduser_unicode(start_dir)
	dialog.set_current_folder(start_dir)

	if image:
		for file_filter in _get_image_fiters():
			dialog.add_filter(file_filter)
	else:
		for file_filter in _get_open_fiters():
			dialog.add_filter(file_filter)

	ret = dialog.run()
	if not ret == gtk.RESPONSE_CANCEL:
		result = dialog.get_filename()
	dialog.destroy()
	if result is None: result = ''
	return result

def _get_save_fiters():
	result = []
	descr = uc2const.FORMAT_DESCRIPTION
	ext = uc2const.FORMAT_EXTENSION
	items = [] + data.SAVER_FORMATS
	for item in items:
		file_filter = gtk.FileFilter()
		file_filter.set_name(descr[item])
		for extension in ext[item]:
			file_filter.add_pattern('*.' + extension)
		result.append(file_filter)

	return result

def get_save_file_name(parent, app, path):
	result = ''
	dialog = gtk.FileChooserDialog(_('Save file As...'),
				parent,
				gtk.FILE_CHOOSER_ACTION_SAVE,
				(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
					gtk.STOCK_SAVE, gtk.RESPONSE_OK))
	dialog.set_do_overwrite_confirmation(True)

	dialog.set_default_response(gtk.RESPONSE_OK)
	path = expanduser_unicode(path)

	doc_folder = os.path.dirname(path)
	dialog.set_current_folder(doc_folder)

	doc_name = os.path.basename(path)
	dialog.set_current_name(doc_name)

	for file_filter in _get_save_fiters():
		dialog.add_filter(file_filter)

	ret = dialog.run()
	if not ret == gtk.RESPONSE_CANCEL:
		result = dialog.get_filename()
	dialog.destroy()
	if result is None: result = ''
	return result

def msg_dialog(parent, title, text, seconary_text='', details='',
			dlg_type=gtk.MESSAGE_ERROR):
	dialog = gtk.MessageDialog(parent,
					flags=gtk.DIALOG_MODAL,
					type=dlg_type,
					buttons=gtk.BUTTONS_OK,
					message_format=text)
	if seconary_text:
		dialog.format_secondary_text(seconary_text)

	if details:
		expander = gtk.expander_new_with_mnemonic("_Additional details")

		text_buffer = gtk.TextBuffer()
		text_buffer.set_text(details)
		editor = gtk.TextView(text_buffer);
		editor.set_editable(False)
		editor.set_wrap_mode(True)

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.add(editor)

		expander.add(sw)
		dialog.vbox.pack_start(expander, True)
		expander.show_all()

	dialog.set_title(title)
	dialog.run()
	dialog.destroy()

def warning_dialog(parent, title, text, seconary_text='',
				buttons=[(gtk.STOCK_OK, gtk.RESPONSE_OK)],
				dlg_type=gtk.MESSAGE_WARNING):
	dialog = gtk.MessageDialog(parent,
					flags=gtk.DIALOG_MODAL,
					type=dlg_type,
					message_format=text)
	if seconary_text:
		dialog.format_secondary_text(seconary_text)
	for button in buttons:
		dialog.add_button(button[0], button[1])
	dialog.set_title(title)
	dialog.set_default_response(buttons[-1][1])
	ret = dialog.run()
	dialog.destroy()
	return ret


def about_dialog(parent):
	from sk1.dialogs.credits import CREDITS
	from sk1.dialogs.license import LICENSE
	authors = [
		"\nIgor E. Novikov (sK1, Gtk+ version; sK1, Tk version)\n\
		<igor.e.novikov@gmail.com>\n\n\
------------------------------",
		"Bernhard Herzog (Skencil, Tk version)\n\
		<bernhard@users.sourceforge.net>\n",
		]

	about = gtk.AboutDialog()
	about.set_property('window-position', gtk.WIN_POS_CENTER)
	about.set_icon(parent.get_icon())

	about.set_program_name(parent.app.appdata.app_name)
	about.set_version(parent.app.appdata.version)
	about.set_copyright("Copyright (C) 2011-2014 by Igor E. Novikov\n")
	about.set_comments(_("Vector graphics editor based on sK1 0.9.x") + "\n" + \
						  _("and Skencil 0.6.x experience."))
	about.set_website('http://www.sk1project.org')

	about.set_logo(load_image(IMG_APP_ICON))
	about.set_authors(authors + [CREDITS])
	about.set_license(LICENSE)
	about.run()
	about.destroy()

def text_edit_dialog(parent, text="", caption=_("Enter text")):
	result = "" + text
	dialog = gtk.Dialog(caption, parent,
						gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
						(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
						gtk.STOCK_OK, gtk.RESPONSE_OK))
	dialog.set_icon(parent.get_icon())
	dialog.set_default_size(570, 350)

	#------------------------

	text_buffer = gtk.TextBuffer()
	text_buffer.set_text(text)
	editor = gtk.TextView(text_buffer);

	sw = gtk.ScrolledWindow()
	sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
	sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	sw.add(editor)

	vbox = gtk.VBox(False, 0)
	vbox.pack_start(sw, True, True, 0)

	#------------------------

	dialog.vbox.pack_start(vbox)

	dialog.show_all()
	ret = dialog.run()

	if ret == gtk.RESPONSE_OK:
		result = text_buffer.get_text(text_buffer.get_start_iter(),
									text_buffer.get_end_iter())

	dialog.destroy()
	return result

def delete_page_dialog(parent, doc, caption=_("Delete page")):
	result = -1
	dialog = gtk.Dialog(caption, parent,
						gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
						(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
						gtk.STOCK_OK, gtk.RESPONSE_OK))
	dialog.set_icon(parent.get_icon())
	dialog.set_resizable(False)

	#------------------------
	pages = doc.get_pages()
	hbox = gtk.HBox(False, 10)
	hbox.set_border_width(10)
	label = gtk.Label(_('Delete page No.:'))
	hbox.pack_start(label, True, True, 0)

	index = pages.index(doc.active_page)

	adj = gtk.Adjustment(index + 1, 1, len(pages), 1, 1, 0)
	spinner = gtk.SpinButton(adj, 0, 0)
	spinner.set_numeric(True)
	hbox.pack_end(spinner, False, False, 0)

	#------------------------

	dialog.vbox.pack_start(hbox)
	dialog.show_all()
	ret = dialog.run()

	if ret == gtk.RESPONSE_OK:
		result = int(adj.get_value()) - 1
	dialog.destroy()
	return result

def goto_page_dialog(parent, doc, caption=_("Go to page")):
	result = -1
	dialog = gtk.Dialog(caption, parent,
						gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
						(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
						gtk.STOCK_OK, gtk.RESPONSE_OK))
	dialog.set_icon(parent.get_icon())
	dialog.set_resizable(False)

	#------------------------
	pages = doc.get_pages()
	hbox = gtk.HBox(False, 10)
	hbox.set_border_width(10)
	label = gtk.Label(_('Go to page No.:'))
	hbox.pack_start(label, True, True, 0)

	index = pages.index(doc.active_page)

	adj = gtk.Adjustment(index + 1, 1, len(pages), 1, 1, 0)
	spinner = gtk.SpinButton(adj, 0, 0)
	spinner.set_numeric(True)
	hbox.pack_end(spinner, False, False, 0)

	#------------------------

	dialog.vbox.pack_start(hbox)
	dialog.show_all()
	ret = dialog.run()

	if ret == gtk.RESPONSE_OK:
		result = int(adj.get_value()) - 1
	dialog.destroy()
	return result

def insert_page_dialog(parent, doc, caption=_("Insert page")):
	result = []
	dialog = gtk.Dialog(caption, parent,
						gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
						(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
						gtk.STOCK_OK, gtk.RESPONSE_OK))
	dialog.set_icon(parent.get_icon())
	dialog.set_resizable(False)

	#------------------------
	pages = doc.get_pages()
	index = pages.index(doc.active_page)

	hbox = gtk.HBox(False, 10)
	hbox.set_border_width(10)

	label = gtk.Label(_('Insert:'))
	hbox.pack_start(label, False, False, 0)


	adj = gtk.Adjustment(1, 1, 1000, 1, 1, 0)
	spinner = gtk.SpinButton(adj, 0, 0)
	spinner.set_numeric(True)
	hbox.pack_start(spinner, False, False, 0)

	label = gtk.Label(_('page(s)'))
	hbox.pack_start(label, False, False, 0)

	hbox2 = gtk.HBox(False, 10)
	hbox2.set_border_width(10)

	adj2 = gtk.Adjustment(index + 1, 1, len(pages), 1, 1, 0)
	spinner2 = gtk.SpinButton(adj2, 0, 0)
	spinner2.set_numeric(True)
	hbox2.pack_end(spinner2, False, False, 0)

	label = gtk.Label(_('page No.:'))
	hbox2.pack_end(label, False, False, 0)

	vbox = gtk.VBox(False, 0)
	radiobut1 = gtk.RadioButton(None, _("Before"))
	radiobut2 = gtk.RadioButton(radiobut1, _("After"))
	vbox.pack_start(radiobut1)
	vbox.pack_start(radiobut2)
	radiobut2.set_active(True)
	hbox2.pack_start(vbox, False, False, 0)
	#------------------------

	dialog.vbox.pack_start(hbox)
	dialog.vbox.pack_start(hbox2)
	dialog.show_all()
	ret = dialog.run()

	if ret == gtk.RESPONSE_OK:
		number = int(adj.get_value())
		target = int(adj2.get_value()) - 1
		if radiobut2.get_active():
			position = uc2const.AFTER
		else:
			position = uc2const.BEFORE
		result = [number, target, position]

	dialog.destroy()
	return result


class ProgressDialog(gtk.Dialog):

	error_info = None

	def __init__(self, caption, parent):
		self.caption = caption

		gtk.Dialog.__init__(self, caption,
                   parent,
                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                   (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
		self.set_resizable(True)
		self.set_size_request(350, -1)
		self.set_resizable(False)

		self.vbox.set_border_width(10)

		self.label = gtk.Label('')
		self.vbox.pack_start(self.label, True, False, 5)
		self.progress_bar = gtk.ProgressBar()
		self.vbox.pack_start(self.progress_bar, False, False, 10)

		self.vbox.show_all()

		self.timer = gobject.timeout_add(100, self.progress_timeout)
		self.flag = False
		self.result = None

	def progress_timeout(self):
		if not self.flag:
			self.flag = True
			try:
				self.result = self.executable(*self.args)
			except:
				self.result = None
				self.error_info = sys.exc_info()

			self.progress_bar.set_text('100 %')
			self.progress_bar.set_fraction(1.0)
			while gtk.events_pending():
				gtk.main_iteration()

			self.response(gtk.RESPONSE_OK)

	def listener(self, *args):
		val = round(args[0][1], 2)
		info = args[0][0]
		self.label.set_label(info)
		self.progress_bar.set_text('%d %%' % (val * 100.0))
		if val > 1.0:val = 1.0
		if val < 0.0:val = 0.0
		self.progress_bar.set_fraction(val)
		while gtk.events_pending():
			gtk.main_iteration()

	def run(self, executable, args):
		events.connect(events.FILTER_INFO, self.listener)
		self.progress_bar.set_text('0 %')
		self.progress_bar.set_fraction(0.0)
		while gtk.events_pending():
			gtk.main_iteration()
		self.executable = executable
		self.args = args
		return gtk.Dialog.run(self)


	def destroy(self):
		events.disconnect(events.FILTER_INFO, self.listener)
		gobject.source_remove(self.timer)
		self.timer = 0
		gtk.Dialog.destroy(self)
