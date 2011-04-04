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


#pyuic4 converts GUIs created using Qt Designer to Python code.
#pyrcc4 embeds arbitrary resources (eg. icons, images, translation files) 
#in a Python module.
#pylupdate4 updates translation files

import sys
import os

from PyQt4 import QtGui, Qt

import uc2
from uc2.utils import system
from uc2 import sk1doc
from uc2 import cms

import dialogs
import mw
import iconfactory
import modes
from sk1app import events, app_conf
from sk1app.presenter import DocumentPresenter
from sk1app.inspector import DocumentInspector
from proxy import AppProxy


class Application(QtGui.QApplication):

	"""Provides main sK1 application instance."""

	inspector = None
	proxy = None
	config = None
	appdata = None
	mw = None
	pkgdir = None

	generic_icons = {}
	canvas_cursors = {}
	default_cms = None
	current_doc = None
	docs = []
	actions = {}

	doc_counter = 0
	clipboard = []

	def __init__(self, packagedir):
		"""
		Constructs an instance. 
		
		packagedir - sk1 package location. 
		The value is needed for correct resource uploading.
		"""

		QtGui.QApplication.__init__(self, sys.argv)

		self.events = events
		self.proxy = AppProxy(self)
		self.appdata = app_conf.AppData()

		setattr(uc2, "appdata", self.appdata)

		self.setOrganizationName(self.appdata.app_org)
		self.setOrganizationDomain(self.appdata.app_domain)
		self.setApplicationName(self.appdata.app_proc)

		#FIXME: Here should be locale init.

		setattr(uc2, "_", self.tr)

		self.inspector = DocumentInspector(self)
		self.config = app_conf.get_app_config()
		self.config.load(self.appdata.app_config)

		setattr(uc2, "config", self.config)

		iconfactory.set_app_icon(self.appdata)
		self.generic_icons = iconfactory.get_generic_icons()
		iconfactory.set_doc_icon(self.appdata, self.config.set_doc_icon)

		from resources import cursor_icons_rc
		self.canvas_cursors = modes.get_cursors()

		self.pkgdir = packagedir

		import actions
		self.actions = actions.create_actions(self)
		self.default_cms = cms.ColorManager(self.qcolor_creator)
		self.mw = mw.MainWindow(self)

	def run(self):
		events.emit(events.NO_DOCS)
		msg = self.tr('To start create new or open existing document')
		events.emit(events.APP_STATUS, msg)
		self.mw.show()
		self.exec_()

	def get_new_docname(self):
		self.doc_counter += 1
		return unicode(self.tr('Untitled')) + ' ' + str(self.doc_counter)

	def set_current_doc(self, doc):
		self.current_doc = doc
		events.emit(events.DOC_CHANGED, doc)

	def update_config(self):
		if self.mw.windowState() == Qt.Qt.WindowMaximized:
			if self.config.os != system.MACOSX:
				self.config.mw_maximized = 1
		else:
			self.config.mw_maximized = 0

			self.config.mw_width = self.mw.width()
			self.config.mw_height = self.mw.height()

	def stub(self):
		print 'Works!'


	def new(self):
		doc = DocumentPresenter(self)
		self.docs.append(doc)
		self.set_current_doc(doc)
		self.mw.menubar.rebuild_window_menu()
		self.mw.set_title()
		events.emit(events.APP_STATUS, self.tr('New document created'))

	def open(self):
		doc_file = dialogs.get_open_file_name(self.mw, self,
											self.config.open_dir)
		if os.path.lexists(doc_file):
			try:
				doc = DocumentPresenter(self, doc_file)
			except:
				msg = self.tr('Cannot open file')
				msg = "<b>%s '%s'</b><br><br>" % (msg, doc_file)
				s = self.tr('The file may be corrupted or not supported format')
				QtGui.QMessageBox.warning(self.mw, self.appdata.app_name,
												msg + s, QtGui.QMessageBox.Ok)
				return
			self.docs.append(doc)
			self.set_current_doc(doc)
			self.mw.menubar.rebuild_window_menu()
			self.mw.set_title()
			self.config.open_dir = os.path.dirname(doc_file)
			events.emit(events.APP_STATUS, self.tr('Document opened'))

	def save(self, doc=''):
		if not doc:
			doc = self.current_doc
		if not doc.doc_file:
			return self.save_as()
		ext = os.path.splitext(self.current_doc.doc_file)[1]
		if not ext == sk1doc.DOC_EXTENSION:
			return self.save_as()
		if not os.path.lexists(os.path.dirname(self.current_doc.doc_file)):
			return self.save_as()

		try:
			doc.save()
			events.emit(events.DOC_SAVED, doc)
		except:
			return False
		events.emit(events.APP_STATUS, self.tr('Document saved'))
		return True

	def save_as(self):
		doc_file = '' + self.current_doc.doc_file
		if not doc_file:
			doc_file = '' + self.current_doc.doc_name
		if not os.path.splitext(doc_file)[1] == sk1doc.DOC_EXTENSION:
			doc_file = os.path.splitext(doc_file)[0] + sk1doc.DOC_EXTENSION
		if not os.path.lexists(os.path.dirname(doc_file)):
			doc_file = os.path.join(self.config.save_dir,
								os.path.basename(doc_file))
		doc_file = dialogs.get_save_file_name(self.mw, self, doc_file)
		if doc_file:
			old_file = self.current_doc.doc_file
			old_name = self.current_doc.doc_name
			self.current_doc.set_doc_file(doc_file)
			try:
				self.current_doc.save()
			except IOError:
				self.current_doc.set_doc_file(old_file, old_name)

				errtype, value, traceback = sys.exc_info()
				print errtype, value, traceback

				first = self.tr('Cannot save document')
				second = self.tr('Please check file name and write permissions')
				msg = ("<b>%s '%s'.</b><br><br>%s.<br>") % (first,
										self.current_doc.doc_name, second)

				QtGui.QMessageBox.warning(self.mw, self.appdata.app_name,
												msg, QtGui.QMessageBox.Ok)
				return False
			self.config.save_dir = os.path.dirname(doc_file)
			events.emit(events.APP_STATUS, self.tr('Document saved'))
			return True
		else:
			return False

	def save_all(self):
		for doc in [] + self.docs:
			self.save(doc)

	def close(self, doc=''):
		if not doc:
			doc = self.current_doc
		if doc is None:
			return
		if not doc.subwindow == self.mw.active_child():
			self.mw.mdiArea.setActiveSubWindow(doc.subwindow)

		if self.inspector.is_doc_not_saved(doc):
			first = self.tr("Document '%1' has been modified.").arg(doc.doc_name)
			second = self.tr('Do you want to save your changes?')
			ret = QtGui.QMessageBox.warning(self.mw, self.appdata.app_name,
					("<b>%s</b><br><br>%s<br>") % (first, second),
					QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
					QtGui.QMessageBox.Cancel)

			if ret == QtGui.QMessageBox.Save:
				if not self.save(): return False
			if ret == QtGui.QMessageBox.Cancel: return False

		if doc in self.docs:
			self.docs.remove(doc)
			self.mw.mdiArea.activatePreviousSubWindow()
			doc.close()
			events.emit(events.DOC_CLOSED)
			if not len(self.docs):
				self.current_doc = None
				events.emit(events.NO_DOCS)
				msg = self.tr('To start create new or open existing document')
				events.emit(events.APP_STATUS, msg)
				self.mw.set_title()
		self.mw.menubar.rebuild_window_menu()
		return True

	def close_all(self):
		ret = True
		for doc in [] + self.docs:
			if not self.close(doc):
				ret = False
				break
		return ret

	def app_exit(self):
		self.update_config()
		self.config.save(self.appdata.app_config)
		self.close_all()
		if not len(self.docs):
			sys.exit(self.exit())

	def qcolor_creator(self, hexcolor):
		return Qt.QColor(hexcolor)




