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

from PyQt4 import QtGui, Qt, QtCore

from uc2.formats import data
from uc2.utils.fs import expanduser_unicode

def _get_open_fiters():
	result = ''
	descr = data.FORMAT_DESCRIPTION
	ext = data.FORMAT_EXTENSION
	items = [] + data.LOADER_FORMATS
	for item in items:
		result += descr[item] + ' - *.' + ext[item] + ' (*.' + ext[item] + ');;'
	all = ' ('
	for item in items:
		all += ' *.' + ext[item]
	all += ');;' 
	result += descr[data.ALL_FORMATS] + all
	return result

def _get_save_fiters():
	result = ''
	descr = data.FORMAT_DESCRIPTION
	ext = data.FORMAT_EXTENSION
	items = [] + data.SAVER_FORMATS
	for item in items:
		result += descr[item] + ' - *.' + ext[item] + ' (*.' + ext[item] + ');;'
	result = result[0:-2]
	return result

def get_open_file_name(parent, app, directory='~'):
	caption = app.tr('Open file') + ' - ' + app.appdata.app_name
	filter = _get_open_fiters()
	filter += app.tr("All Files") + ' (*.*)'
	directory = expanduser_unicode(directory)
	return unicode(QtGui.QFileDialog.getOpenFileName(parent, caption, directory, filter))

def get_save_file_name(parent, app, directory='~'):
	caption = app.tr('Save file As...') + ' - ' + app.appdata.app_name
	filter = _get_save_fiters()
	directory = expanduser_unicode(directory)
	return unicode(QtGui.QFileDialog.getSaveFileName(parent, caption, directory, filter))

def show_about_dialog(parent):
	from dlg_about import Ui_Dialog
	dialog = QtGui.QDialog(parent)
	ui = Ui_Dialog()
	ui.setupUi(dialog)
	ui.buttonBox_2.rejected.connect(dialog.close)
	dialog.show()
