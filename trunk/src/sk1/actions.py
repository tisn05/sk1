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

import gtk

from sk1 import _, events, icons
from sk1.events import CLIPBOARD, DOC_CHANGED, PAGE_CHANGED, \
DOC_CLOSED, DOC_MODIFIED, DOC_SAVED, NO_DOCS, SELECTION_CHANGED



class AppAction(gtk.Action):

	def __init__(self, name, label, tooltip, icon, shortcut,
				 callable, channels, validator, args=[]):

		gtk.Action.__init__(self, name, label, tooltip, icon)
		self.menuitem = None
		self.tooltip = tooltip
		self.shortcut = shortcut
		self.callable = callable
		self.events = events
		self.validator = validator
		self.args = args
		self.icon = icon

		self.connect('activate', self.callable)

		self.channels = channels
		self.validator = validator

		if channels:
			for channel in channels:
				events.connect(channel, self.receiver)

	def receiver(self, *args):
		self.set_sensitive(self.validator())

class AppToggleAction(gtk.ToggleAction):

	def __init__(self, name, label, tooltip, icon, shortcut,
				 callable, channels, validator, checker, args=[]):

		gtk.Action.__init__(self, name, label, tooltip, icon)
		self.menuitem = None
		self.tooltip = tooltip
		self.shortcut = shortcut
		self.callable = callable
		self.events = events
		self.validator = validator
		self.checker = checker
		self.args = args
		self.icon = icon

		self.connect('activate', self.callable)

		self.channels = channels
		self.validator = validator

		if channels:
			for channel in channels:
				events.connect(channel, self.receiver)

	def receiver(self, *args):
		self.set_sensitive(self.validator())
		self.set_active(self.checker())

def create_actions(app):
	insp = app.inspector
	proxy = app.proxy
	accelgroup = app.accelgroup
	actiongroup = app.actiongroup
	actions = {}
	entries = [

#	name, label, tooltip, icon, shortcut, callable, [channels], validator, args 
#gtk.accelerator_name(ord('+'),gtk.gdk.CONTROL_MASK)

#SELECT_MODE = 0
#SHAPER_MODE = 1
#ZOOM_MODE = 2
#FLEUR_MODE = 3
#LINE_MODE = 10
#CURVE_MODE = 11
#RECT_MODE = 12
#ELLIPSE_MODE = 13
#TEXT_MODE = 14
#POLYGON_MODE = 15
#ZOOM_OUT_MODE = 16
#MOVE_MODE = 17
#COPY_MODE = 18

	['SELECT_MODE', _('Selection mode'), _('Selection mode'), None, None,
	 proxy.set_select_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['SHAPER_MODE', _('Edit mode'), _('Edit mode'), None, None,
	 proxy.set_shaper_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['ZOOM_MODE', _('Zoom mode'), _('Zoom mode'), None, None,
	 proxy.set_zoom_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['FLEUR_MODE', _('Fleur mode'), _('Fleur mode'), None, None,
	 proxy.set_fleur_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['LINE_MODE', _('Create polyline'), _('Create polyline'), None, None,
	 proxy.set_line_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['CURVE_MODE', _('Create paths'), _('Create paths'), None, None,
	 proxy.set_curve_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['RECT_MODE', _('Create rectangle'), _('Create rectangle'), None, None,
	 proxy.set_rect_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['ELLIPSE_MODE', _('Create ellipse'), _('Create ellipse'), None, None,
	 proxy.set_ellipse_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['TEXT_MODE', _('Create text'), _('Create text'), None, None,
	 proxy.set_text_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['POLYGON_MODE', _('Create polygon'), _('Create polygon'), None, None,
	 proxy.set_polygon_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['ZOOM_OUT_MODE', _('Zoom out mode'), _('Zoom out mode'), None, None,
	 proxy.set_zoom_out_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['MOVE_MODE', _('Move mode'), _('Move mode'), None, None,
	 proxy.set_move_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['COPY_MODE', _('Copy mode'), _('Copy mode'), None, None,
	 proxy.set_copy_mode, [NO_DOCS, DOC_CHANGED], insp.is_doc],

	#------ File -------
	['NEW', _('_New'), _('New'), gtk.STOCK_NEW, '<Control>N',
	 proxy.new, None, None],
	['OPEN', _('_Open'), _('Open'), gtk.STOCK_OPEN, '<Control>O',
	 proxy.open, None, None],
	['IMPORT_IMAGE', _('_Import image'), _('Import image'), None, None,
	 proxy.import_image, None, None],
	['SAVE', _('_Save'), _('Save'), gtk.STOCK_SAVE, '<Control>S',
	 proxy.save, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED, DOC_SAVED],
	 insp.is_doc_not_saved],
	['SAVE_AS', _('Save _As...'), _('Save As...'), gtk.STOCK_SAVE_AS, None,
	 proxy.save_as, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['SAVE_ALL', _('Save All'), _('Save All'), None, None,
	 proxy.save_all, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED, DOC_SAVED],
	 insp.is_any_doc_not_saved],
	['CLOSE', _('_Close'), _('Close'), gtk.STOCK_CLOSE, '<Control>W',
	 proxy.close, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['CLOSE_ALL', _('_Close All'), _('Close All'), None, None,
	 proxy.close_all, [NO_DOCS, DOC_CHANGED], insp.is_doc],

	['PRINT', _('_Print...'), _('Print'), gtk.STOCK_PRINT, '<Control>P',
	 proxy.do_print, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['PRINT_SETUP', _('Print Setup...'), _('Print Setup'), gtk.STOCK_PRINT_PREVIEW, None,
	 proxy.do_print_setup, [NO_DOCS, DOC_CHANGED], insp.is_doc],

	['QUIT', _('_Exit'), _('Exit'), gtk.STOCK_QUIT, '<Alt>F4',
	 proxy.exit, None, None],

	#------ Edit -------
	['UNDO', _('_Undo'), _('Undo'), gtk.STOCK_UNDO, '<Control>Z',
	 proxy.undo, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED, DOC_CLOSED], insp.is_undo],
	['REDO', _('_Redo'), _('Redo'), gtk.STOCK_REDO, '<Control><Shift>Z',
	 proxy.redo, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED, DOC_CLOSED], insp.is_redo],
	['CLEAR_HISTORY', _('Clear undo history'), _('Clear undo history'),
	None, None, proxy.clear_history, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED,
	DOC_CLOSED], insp.is_history],


	['CUT', _('Cu_t'), _('Cut'), gtk.STOCK_CUT, '<Control>X',
	 proxy.cut, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_selection],
	['CUT2', 'Cut', 'Cut', gtk.STOCK_CUT, '<Shift>Delete',
	 proxy.cut, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_selection],
	['CUT3', 'Cut', 'Cut', gtk.STOCK_CUT, '<Shift>KP_Decimal',
	 proxy.cut, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_selection],
	['COPY', _('_Copy'), _('Copy'), gtk.STOCK_COPY, '<Control>C',
	 proxy.copy, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_selection],
	['PASTE', _('_Paste'), _('Paste'), gtk.STOCK_PASTE, '<Control>V',
	 proxy.paste, [NO_DOCS, CLIPBOARD], insp.is_clipboard],
	['PASTE2', '_Paste', 'Paste', None, '<Shift>Insert',
	 proxy.paste, [NO_DOCS, CLIPBOARD], insp.is_clipboard],
	['PASTE3', '_Paste', 'Paste', None, '<Shift>KP_0',
	 proxy.paste, [NO_DOCS, CLIPBOARD], insp.is_clipboard],
	['DELETE', _('_Delete'), _('Delete'), gtk.STOCK_DELETE, 'Delete',
	 proxy.delete, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_selection],
	['DELETE2', '_Delete', 'Delete', None, 'KP_Delete',
	 proxy.delete, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_selection],

	['SELECT_ALL', _('_Select All'), _('Select All'), gtk.STOCK_SELECT_ALL, '<Control>A',
	 proxy.select_all, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['DESELECT', _('_Deselect'), _('Deselect'), None, '<Control><Shift>A',
	 proxy.deselect, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_selection],

	#------ View -------

	['ZOOM_IN', _('Zoom in'), _('Zoom in'), gtk.STOCK_ZOOM_IN, '<Control>equal',
	 proxy.zoom_in, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['ZOOM_OUT', _('Zoom out'), _('Zoom out'), gtk.STOCK_ZOOM_OUT, '<Control>minus',
	 proxy.zoom_out, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['ZOOM_PAGE', _('Fit zoom to page'), _('Fit zoom to page'), gtk.STOCK_FILE, '<Shift>F4',
	 proxy.fit_zoom_to_page, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['ZOOM_100', _('Zoom 100%'), _('Zoom 100%'), gtk.STOCK_ZOOM_100, None,
	 proxy.zoom_100, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['ZOOM_SELECTED', _('Zoom selected'), _('Zoom selected'), gtk.STOCK_ZOOM_FIT, 'F4',
	 proxy.zoom_selected, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_selection],
	['FORCE_REDRAW', _('Redraw document'), _('Redraw document'),
	gtk.STOCK_REFRESH, '<Alt>R', proxy.force_redraw,
	[NO_DOCS, DOC_CHANGED], insp.is_doc],

	['PAGE_FRAME', _('Create page frame'), _('Create page frame'), icons.STOCK_PAGE_FRAME, None,
	 proxy.create_page_border, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['PAGE_GUIDE_FRAME', _('Guides along page border'), _('Guides along page border'),
	icons.STOCK_PAGE_GUIDE_FRAME, None, proxy.create_guide_border, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['REMOVE_ALL_GUIDES', _('Remove all guides'), _('Remove all guides'), icons.STOCK_REMOVE_ALL_GUIDES, None,
	 proxy.remove_all_guides, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['GUIDES_AT_CENTER', _('Guides at page center'), _('Guides at page center'), icons.STOCK_GUIDES_AT_CENTER, None,
	 proxy.create_guides_at_center, [NO_DOCS, DOC_CHANGED], insp.is_doc],

	#------ Layout -------
	['INSERT_PG', _('Insert page...'), _('Insert page'), None, None,
	 proxy.insert_page, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['DELETE_PG', _('Delete page...'), _('Delete page'), None, None,
	 proxy.delete_page, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED], insp.can_delete_page],
	['GOTO_PG', _('Go to page...'), _('Go to page'), None, None,
	 proxy.goto_page, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED], insp.can_goto_page],
	['NEXT_PG', _('Next page'), _('Next page'), None, 'Page_Down',
	 proxy.next_page, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED, PAGE_CHANGED], insp.can_be_next_page],
	['NEXT_PG_KP', 'Next page', 'Next page', None, 'KP_Page_Down',
	 proxy.next_page, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED, PAGE_CHANGED], insp.can_be_next_page],
	['PREV_PG', _('Previous page'), _('Previous page'), None, 'Page_Up',
	 proxy.previous_page, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED, PAGE_CHANGED], insp.can_be_previous_page],
	['PREV_PG_KP', 'Previous page', 'Previous page', None, 'KP_Page_Up',
	 proxy.previous_page, [NO_DOCS, DOC_CHANGED, DOC_MODIFIED, PAGE_CHANGED], insp.can_be_previous_page],

	#------ Arrange -------
	['COMBINE', _('_Combine'), _('Combine'), None, '<Control>L',
	 proxy.combine_selected, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.can_be_combined],
	['BREAK_APART', _('_Break apart'), _('Break apart'), None, '<Control>K',
	 proxy.break_apart_selected, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.can_be_breaked],

	['GROUP', _('_Group'), _('Group'), None, '<Control>G',
	 proxy.group, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.can_be_grouped],
	['UNGROUP', _('_Ungroup'), _('Ungroup'), None, '<Control>U',
	 proxy.ungroup, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.can_be_ungrouped],
	['UNGROUP_ALL', _('U_ngroup all'), _('Ungroup all'), None, None,
	 proxy.ungroup_all, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.can_be_ungrouped_all],
	['CONVERT_TO_CURVES', _('Con_vert to curves'), _('Convert to curves'), icons.STOCK_TO_CURVE, '<Control>Q',
	 proxy.convert_to_curve, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.can_be_curve],

	['EDIT_TEXT', _('_Edit text...'), _('Edit text'), None, 'F8',
	 proxy.edit_text, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_text_selected],

	#------ Effects -------
	['SET_CONTAINER', _('_Place into container'), _('Place into container'), None, None,
	 proxy.set_container, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_selection],

	['UNPACK_CONTAINER', _('_Extract from container'), _('Extract from container'), None, None,
	 proxy.unpack_container, [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED], insp.is_container_selected],

	#------ Tools -------
	['PAGES', _('_Pages'), _('Pages'), icons.STOCK_PLUGIN_PAGES, '<Control>F7',
	 proxy.load_pages_plg, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['LAYERS', _('_Layers'), _('Close'), icons.STOCK_PLUGIN_LAYERS, 'F7',
	 proxy.load_layers_plg, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['DOM_VIEWER', _('_Object browser'), _('Object browser'), icons.STOCK_PLUGIN_DOM_VIEWER, None,
	 proxy.load_dom_plg, [NO_DOCS, DOC_CHANGED], insp.is_doc],


	['PROPERTIES', _('Document Properties...'), _('Document Properties...'), gtk.STOCK_PROPERTIES, None,
	 proxy.properties, [NO_DOCS, DOC_CHANGED], insp.is_doc],
	['PREFERENCES', _('Preferences...'), _('Preferences...'), gtk.STOCK_PREFERENCES, None,
	 proxy.preferences, None, None],

	['REPORT_BUG', _('_Report bug'), _('Report bug'), gtk.STOCK_DIALOG_WARNING, None,
	 proxy.report_bug, None, None],
	['PROJECT_WEBSITE', _('Project _web site'), _('Project web site'), None, None,
	 proxy.project_website, None, None],
	['PROJECT_FORUM', _('Project _forum'), _('Project forum'), None, None,
	 proxy.project_forum, None, None],
	['ABOUT', _('_About sK1'), _('About sK1'), gtk.STOCK_ABOUT, None,
	 proxy.about, None, None],

	['ROTATE_LEFT', _('Rotate _Left'), _('Rotate Left'), icons.STOCK_ROTATE_LEFT, None,
	 proxy.rotate_left, [events.NO_DOCS, events.DOC_CHANGED,
	events.SELECTION_CHANGED], insp.is_selection],
	['ROTATE_RIGHT', _('Rotate _Right'), _('Rotate Right'), icons.STOCK_ROTATE_RIGHT, None,
	 proxy.rotate_right, [events.NO_DOCS, events.DOC_CHANGED,
	events.SELECTION_CHANGED], insp.is_selection],
	['VERT_MIRROR', _('Flip _vertically'), _('Flip vertically'), icons.STOCK_VERT_MIRROR, None,
	 proxy.vertical_mirror, [events.NO_DOCS, events.DOC_CHANGED,
	events.SELECTION_CHANGED], insp.is_selection],
	['HOR_MIRROR', _('Flip _horizontally'), _('Flip horizontally'), icons.STOCK_HOR_MIRROR, None,
	 proxy.horizontal_mirror, [events.NO_DOCS, events.DOC_CHANGED,
	events.SELECTION_CHANGED], insp.is_selection],
	]

	toggle_entries = [
	['STROKE_VIEW', _('Stroke View'), _('Stroke View'), None, '<Shift>F9',
	 proxy.stroke_view, [NO_DOCS, DOC_CHANGED], insp.is_doc, insp.is_stroke_view],
	['DRAFT_VIEW', _('Draft View'), _('Draft View'), None, None,
	 proxy.draft_view, [NO_DOCS, DOC_CHANGED], insp.is_doc, insp.is_draft_view],

	['SHOW_GRID', _('Show grid'), _('Show grid'), None, None,
	 proxy.show_grid, [NO_DOCS, DOC_CHANGED], insp.is_doc, insp.is_grid_visible],
	['SHOW_GUIDES', _('Show guides'), _('Show guides'), None, None,
	 proxy.show_guides, [NO_DOCS, DOC_CHANGED], insp.is_doc, insp.is_guides_visible],
	['SHOW_SNAP', _('Show active snapping'), _('Show active snapping'), None, None,
	 proxy.show_snapping, [NO_DOCS, DOC_CHANGED], insp.is_doc, insp.is_show_snapping],
	['SHOW_PAGE', _('Show page border'), _('Show page border'), None, None,
	 proxy.draw_page_border, [NO_DOCS, DOC_CHANGED], insp.is_doc, insp.is_draw_page_border],


	['SNAP_TO_GRID', _('Snap to grid'), _('Snap to grid'), icons.STOCK_SNAP_TO_GRID, '<Control>Y',
	 proxy.snap_to_grid, [NO_DOCS, DOC_CHANGED], insp.is_doc, insp.is_snap_to_grid],
	['SNAP_TO_GUIDES', _('Snap to guides'), _('Snap to guides'), icons.STOCK_SNAP_TO_GUIDES, '<Control>I',
	 proxy.snap_to_guides, [NO_DOCS, DOC_CHANGED], insp.is_doc, insp.is_snap_to_guides],
	['SNAP_TO_OBJECTS', _('Snap to objects'), _('Snap to objects'), icons.STOCK_SNAP_TO_OBJECTS, None,
	 proxy.snap_to_objects, [NO_DOCS, DOC_CHANGED], insp.is_doc, insp.is_snap_to_objects],
	['SNAP_TO_PAGE', _('Snap to page'), _('Snap to page'), icons.STOCK_SNAP_TO_PAGE, None,
	 proxy.snap_to_page, [NO_DOCS, DOC_CHANGED], insp.is_doc, insp.is_snap_to_page],

	]

	for entry in entries:
		action = AppAction(entry[0], entry[1], entry[2], entry[3],
						   entry[4], entry[5], entry[6], entry[7])

		actions[entry[0]] = action
		if not action.shortcut is None:
			actiongroup.add_action_with_accel(action, action.shortcut)
			action.set_accel_group(accelgroup)
		else:
			actiongroup.add_action(action)

	for entry in toggle_entries:
		action = AppToggleAction(entry[0], entry[1], entry[2], entry[3],
						   entry[4], entry[5], entry[6], entry[7], entry[8])

		actions[entry[0]] = action
		if not action.shortcut is None:
			actiongroup.add_action_with_accel(action, action.shortcut)
			action.set_accel_group(accelgroup)
		else:
			actiongroup.add_action(action)

	return actions
