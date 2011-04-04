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

from PyQt4 import QtGui, QtCore

from sk1app import events

class AppAction(QtGui.QAction):
	
	mode = None
	
	def __init__(self, icon, text, obj, method, shortcut='', 
				channels=[], validator=None):
		
		QtGui.QAction.__init__(self, icon, text, obj)

		if shortcut:
			self.setShortcut(shortcut)
			
		self.method = method		
		obj.connect(self, QtCore.SIGNAL('triggered()'), method)
		
		self.channels = channels
		self.validator = validator
		
		if channels:
			for channel in channels:
				events.connect(channel, self.receiver)	
				
	def receiver(self, *args):
		self.setEnabled(self.validator())

def create_actions(app):
	
	actions = {}
	
	actions['NEW'] = AppAction(app.generic_icons['NEW'], 
							app.tr('New'), 
							app, app.new, 
							'Ctrl+N')
	actions['OPEN'] = AppAction(app.generic_icons['OPEN'], 
							app.tr('Open...'), 
							app, app.open, 
							'Ctrl+O')
	actions['SAVE'] = AppAction(app.generic_icons['SAVE'], 
							app.tr('Save'), 
							app, app.save, 
							'Ctrl+S',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED, 
									events.DOC_MODIFIED, 
									events.DOC_SAVED], 
							validator=app.inspector.is_doc_not_saved)
	actions['SAVE_AS'] = AppAction(app.generic_icons['SAVE_AS'], 
							app.tr('Save As...'), 
							app, app.save_as,
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED], 
							validator=app.inspector.is_doc)
	actions['SAVE_ALL'] = AppAction(QtGui.QIcon(), 
							app.tr('Save All'), 
							app, app.save_all,
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED, 
									events.DOC_MODIFIED, 
									events.DOC_SAVED],
							validator=app.inspector.is_any_doc_not_saved)
	
	actions['PRINT'] = AppAction(app.generic_icons['PRINT'], 
							app.tr('Print...'), 
							app, app.stub, 
							'Ctrl+P',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED, 
									events.DOC_CLOSED],
							validator=app.inspector.is_doc)
	
	actions['CLOSE'] = AppAction(app.generic_icons['CLOSE'], 
							app.tr('Close'), 
							app, app.close, 
							'Ctrl+F4',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED, 
									events.DOC_CLOSED],
							validator=app.inspector.is_doc)
	actions['CLOSE_ALL'] = AppAction(QtGui.QIcon(), 
							app.tr('Close All'), 
							app, app.close_all,
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED, 
									events.DOC_CLOSED],
							validator=app.inspector.is_doc)
	
	actions['UNDO'] = AppAction(app.generic_icons['UNDO'], 
							app.tr('Undo'), 
							app, app.proxy.do_undo, 
							'Ctrl+Z',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED,
									events.DOC_MODIFIED, 
									events.DOC_CLOSED],
							validator=app.inspector.is_undo)
	actions['REDO'] = AppAction(app.generic_icons['REDO'], 
							app.tr('Redo'), 
							app, app.proxy.do_redo, 
							'Ctrl+Shift+Z',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED,
									events.DOC_MODIFIED,  
									events.DOC_CLOSED],
							validator=app.inspector.is_redo)
	actions['CLEAR_HISTORY'] = AppAction(QtGui.QIcon(), 
							app.tr('Clear undo history'), 
							app, app.proxy.clear_history, 
							'',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED,
									events.DOC_MODIFIED, 
									events.DOC_CLOSED],
							validator=app.inspector.is_history)	
	
	actions['DELETE'] = AppAction(app.generic_icons['DELETE'], 
							app.tr('Delete'), 
							app, app.proxy.delete_selection, 
							'Delete',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED,
									events.SELECTION_CHANGED,
									events.DOC_CLOSED],
							validator=app.inspector.is_selection)
	actions['CUT'] = AppAction(app.generic_icons['CUT'], 
							app.tr('Cut'), 
							app, app.proxy.cut_selection, 
							'Ctrl+X',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED,
									events.SELECTION_CHANGED,
									events.DOC_CLOSED],
							validator=app.inspector.is_selection)
	actions['COPY'] = AppAction(app.generic_icons['COPY'], 
							app.tr('Copy'), 
							app, app.proxy.copy_selection, 
							'Ctrl+C',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED,
									events.SELECTION_CHANGED, 
									events.DOC_CLOSED],
							validator=app.inspector.is_selection)
	actions['PASTE'] = AppAction(app.generic_icons['PASTE'], 
							app.tr('Paste'), 
							app, app.proxy.paste_from_clipboard, 
							'Ctrl+V',
							channels=[events.NO_DOCS, 
									events.CLIPBOARD],
							validator=app.inspector.is_clipboard)
	actions['SELECT_ALL'] = AppAction(QtGui.QIcon(), 
							app.tr('Select All'), 
							app, app.proxy.select_all, 
							'Ctrl+A',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED,
									events.DOC_CLOSED],
							validator=app.inspector.is_doc)
	actions['DESELECT'] = AppAction(QtGui.QIcon(), 
							app.tr('Deselect'), 
							app, app.proxy.deselect, 
							'Ctrl+Shift+A',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED,
									events.SELECTION_CHANGED,
									events.DOC_CLOSED],
							validator=app.inspector.is_selection)
	
	actions['ZOOM_IN'] = AppAction(app.generic_icons['ZOOM_IN'], 
							app.tr('Zoom in'), 
							app, app.proxy.zoom_in, 
							'+',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED], 
							validator=app.inspector.is_doc)
	actions['ZOOM_IN'].setAutoRepeat(True)
	
	actions['ZOOM_OUT'] = AppAction(app.generic_icons['ZOOM_OUT'], 
							app.tr('Zoom out'), 
							app, app.proxy.zoom_out, 
							'-',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED], 
							validator=app.inspector.is_doc)
	actions['ZOOM_OUT'].setAutoRepeat(True)	
	
	actions['ZOOM_AREA'] = AppAction(app.generic_icons['ZOOM_IN'], 
							app.tr('Zoom Area'), 
							app, app.proxy.zoom_area, 
							'F2',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED], 
							validator=app.inspector.is_doc)
		
	actions['ZOOM_100'] = AppAction(app.generic_icons['ZOOM_100'], 
							app.tr('Zoom 100%'), 
							app, app.proxy.zoom_100, 
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED], 
							validator=app.inspector.is_doc)
	actions['ZOOM_PAGE'] = AppAction(app.generic_icons['ZOOM_PAGE'], 
							app.tr('Fit zoom to page'), 
							app, app.proxy.fit_to_page, 
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED], 
							validator=app.inspector.is_doc)
	actions['ZOOM_SELECT'] = AppAction(app.generic_icons['ZOOM_SELECT'], 
							app.tr('Fit zoom to selection'), 
							app, app.proxy.zoom_selected, 
							'F4', 
							channels=[events.NO_DOCS, 
									events.SELECTION_CHANGED,
									events.DOC_CHANGED], 
							validator=app.inspector.is_selection)
	actions['ZOOM_PREVIOUS'] = AppAction(QtGui.QIcon(), 
							app.tr('Restore previous view'), 
							app, app.proxy.zoom_previous, 
							'F3',
							channels=[events.NO_DOCS, 
									events.DOC_CHANGED],
							validator=app.inspector.is_doc)
	
	actions['CONFIGURE'] = AppAction(app.generic_icons['CONFIGURE'], 
							app.tr('Configure editor...'), 
							app, app.stub)
	
	actions['EXIT'] = AppAction(app.generic_icons['QUIT'], 
							app.tr('Exit'), 
							app, app.app_exit, 
							'Ctrl+Q')
	
	return actions
