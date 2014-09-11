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


from PyQt4 import Qt, QtGui

def set_app_icon(config):
	
	from resources import app_icon_rc
	
	config.app_icon = QtGui.QIcon()
	config.app_icon.addFile(':/icon_sk1_16.png', Qt.QSize(16, 16))
	config.app_icon.addFile(':/icon_sk1_22.png', Qt.QSize(22, 22))
	config.app_icon.addFile(':/icon_sk1_24.png', Qt.QSize(24, 24))
	config.app_icon.addFile(':/icon_sk1_32.png', Qt.QSize(32, 32))
	config.app_icon.addFile(':/icon_sk1_48.png', Qt.QSize(48, 48))
	config.app_icon.addFile(':/icon_sk1_64.png', Qt.QSize(64, 64))
	
def set_doc_icon(config, flag):
	config.doc_icon = QtGui.QIcon()
	if flag:
		config.doc_icon.addFile(':/16x16/document-icon.png',
							Qt.QSize(16, 16))
	
def get_generic_icons():
	icons = get_oxygen_icons()
	return icons

def get_oxygen_icons():	
	icons_data = {
				'NEW': 'document-new.png',
				
				'OPEN': 'document-open.png',
				'OPEN_RECENT': 'document-open-recent.png',
				'SAVE': 'document-save.png',
				'SAVE_AS': 'document-save-as.png',
				'SAVE_ALL': 'document-save-all.png',
				'PRINT': 'document-print.png',
				'PRINT_PREVIEW': 'document-print-preview.png',
				'CLOSE': 'document-close.png',
				
				'UNDO': 'edit-undo.png',
				'REDO': 'edit-redo.png',
				'DELETE': 'edit-delete.png',
				'CUT': 'edit-cut.png',
				'COPY': 'edit-copy.png',
				'PASTE': 'edit-paste.png',
								
				'ZOOM_IN': 'zoom-in.png',
				'ZOOM_OUT': 'zoom-out.png',
				'ZOOM_100': 'zoom-original.png',
				'ZOOM_SELECT': 'zoom-select.png',
				'ZOOM_PAGE': 'zoom-page.png',
								
				'REFRESH': 'view-refresh.png',
				
				'CONFIGURE': 'configure.png',
				'QUIT': 'application-exit.png',
				'HELP': 'help-contents.png',
				'HOME': 'go-home.png',
				'ABOUT': 'help-about.png',
				'EXIT': 'application-exit.png',
				}
	
	from resources import oxygen_icons_rc
	icons = {}
	
	for key in icons_data.keys():
		icon = QtGui.QIcon()
		icon.addFile(':/16x16/'+ icons_data[key], Qt.QSize(16, 16))
		icon.addFile(':/22x22/'+ icons_data[key], Qt.QSize(22, 22))
		icons[key]=icon
		
		
	return icons


#import gtk, os
#
#def get_gtk_icons():	
#	
#	icons_data = {
#				'NEW': gtk.STOCK_NEW,
#				'OPEN': gtk.STOCK_OPEN,
#				'SAVE': gtk.STOCK_SAVE,
#				'SAVE_AS': gtk.STOCK_SAVE_AS,
#				'PRINT': gtk.STOCK_PRINT,
#				'PRINT_PREVIEW': gtk.STOCK_PRINT_PREVIEW,
#				'CLOSE': gtk.STOCK_CLOSE,
#				'UNDO': gtk.STOCK_UNDO,
#				'REDO': gtk.STOCK_REDO,
#				'DELETE': gtk.STOCK_DELETE,
#				'CUT': gtk.STOCK_CUT,
#				'COPY': gtk.STOCK_COPY,
#				'PASTE': gtk.STOCK_PASTE, 				
#				'ZOOM_IN': gtk.STOCK_PASTE,
#				'ZOOM_OUT': gtk.STOCK_PASTE,
#				'ZOOM_100': gtk.STOCK_PASTE,
#				'ZOOM_FIT': gtk.STOCK_PASTE, 				
#				'REFRESH': gtk.STOCK_REFRESH,
#				'PREFERENCES': gtk.STOCK_PREFERENCES,
#				'QUIT': gtk.STOCK_QUIT,
#				'HELP': gtk.STOCK_HELP,
#				'HOME': gtk.STOCK_HOME,
#				'ABOUT': gtk.STOCK_ABOUT,
#				'QUIT': gtk.STOCK_QUIT,
#				}
#	
#	icons = {}
#	iconTheme = gtk.icon_theme_get_default()
#	warning = False
#	
#	for key in icons_data.keys():	
#		icon = QtGui.QIcon()
#		try:
#			icon.addFile(iconTheme.lookup_icon(icons_data[key], 16, 0).get_filename(), Qt.QSize(16, 16))
#			icon.addFile(iconTheme.lookup_icon(icons_data[key], 22, 0).get_filename(), Qt.QSize(22, 22))
#			icon.addFile(iconTheme.lookup_icon(icons_data[key], 32, 0).get_filename(), Qt.QSize(32, 32))
#		except:
#			icon = None
#			warning = True
#		icons[key] = icon
#	
#	theme_data = []
#	
#	if warning:
#		warning = False
#		for key in icons.keys():
#			if icons[key] is not None:
#				for size in [16, 22, 32]:
#					path = iconTheme.lookup_icon(icons_data[key], size, 0).get_filename()
#					path_dir = os.path.dirname(path)
#					head, path_ext = os.path.splitext(path)
#					theme_data.append([size, path_dir, path_ext])
#				break
#		
#		if len(theme_data):
#			problem_icons = []
#			for key in icons.keys():
#				if icons[key] is None:
#					problem_icons.append(key)
#			
#			for key in problem_icons:
#				icon = QtGui.QIcon()
#				counter = 3
#				for item in theme_data:
#					size = item[0]
#					path = os.path.join(item[1], ('stock_' + key + item[2]).lower())
#					if os.path.exists(path):
#						icon.addFile(path, Qt.QSize(size, size))
#					else:
#						counter -= 1
#				if not counter:
#					warning = True
#					icon = None
#				icons[key] = icon
#				
#	return icons, warning
