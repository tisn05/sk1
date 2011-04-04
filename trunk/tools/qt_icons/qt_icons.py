#! /usr/bin/python
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


import sys, os

from PyQt4 import Qt, QtGui, QtCore

ICON_LIST = [
QtGui.QStyle.SP_TitleBarMinButton, 
QtGui.QStyle.SP_TitleBarMenuButton, 
QtGui.QStyle.SP_TitleBarMaxButton, 
QtGui.QStyle.SP_TitleBarCloseButton, 
QtGui.QStyle.SP_TitleBarNormalButton, 
QtGui.QStyle.SP_TitleBarShadeButton, 
QtGui.QStyle.SP_TitleBarUnshadeButton, 
QtGui.QStyle.SP_TitleBarContextHelpButton, 
QtGui.QStyle.SP_MessageBoxInformation, 
QtGui.QStyle.SP_MessageBoxWarning, 
QtGui.QStyle.SP_MessageBoxCritical, 
QtGui.QStyle.SP_MessageBoxQuestion, 
QtGui.QStyle.SP_DesktopIcon, 
QtGui.QStyle.SP_TrashIcon, 
QtGui.QStyle.SP_ComputerIcon, 
QtGui.QStyle.SP_DriveFDIcon, 
QtGui.QStyle.SP_DriveHDIcon, 
QtGui.QStyle.SP_DriveCDIcon, 
QtGui.QStyle.SP_DriveDVDIcon, 
QtGui.QStyle.SP_DriveNetIcon, 
QtGui.QStyle.SP_DirHomeIcon, 
QtGui.QStyle.SP_DirOpenIcon, 
QtGui.QStyle.SP_DirClosedIcon, 
QtGui.QStyle.SP_DirIcon, 
QtGui.QStyle.SP_DirLinkIcon, 
QtGui.QStyle.SP_FileIcon, 
QtGui.QStyle.SP_FileLinkIcon, 
QtGui.QStyle.SP_FileDialogStart, 
QtGui.QStyle.SP_FileDialogEnd, 
QtGui.QStyle.SP_FileDialogToParent, 
QtGui.QStyle.SP_FileDialogNewFolder, 
QtGui.QStyle.SP_FileDialogDetailedView, 
QtGui.QStyle.SP_FileDialogInfoView, 
QtGui.QStyle.SP_FileDialogContentsView, 
QtGui.QStyle.SP_FileDialogListView, 
QtGui.QStyle.SP_FileDialogBack, 
QtGui.QStyle.SP_DockWidgetCloseButton, 
QtGui.QStyle.SP_ToolBarHorizontalExtensionButton, 
QtGui.QStyle.SP_ToolBarVerticalExtensionButton, 
QtGui.QStyle.SP_DialogOkButton, 
QtGui.QStyle.SP_DialogCancelButton, 
QtGui.QStyle.SP_DialogHelpButton, 
QtGui.QStyle.SP_DialogOpenButton, 
QtGui.QStyle.SP_DialogSaveButton, 
QtGui.QStyle.SP_DialogCloseButton, 
QtGui.QStyle.SP_DialogApplyButton, 
QtGui.QStyle.SP_DialogResetButton, 
QtGui.QStyle.SP_DialogDiscardButton, 
QtGui.QStyle.SP_DialogYesButton, 
QtGui.QStyle.SP_DialogNoButton, 
QtGui.QStyle.SP_ArrowUp, 
QtGui.QStyle.SP_ArrowDown, 
QtGui.QStyle.SP_ArrowLeft, 
QtGui.QStyle.SP_ArrowRight, 
QtGui.QStyle.SP_ArrowBack, 
QtGui.QStyle.SP_ArrowForward, 
QtGui.QStyle.SP_CommandLink, 
QtGui.QStyle.SP_VistaShield, 
QtGui.QStyle.SP_BrowserReload, 
QtGui.QStyle.SP_BrowserStop, 
QtGui.QStyle.SP_MediaPlay, 
QtGui.QStyle.SP_MediaStop, 
QtGui.QStyle.SP_MediaPause, 
QtGui.QStyle.SP_MediaSkipForward, 
QtGui.QStyle.SP_MediaSkipBackward, 
QtGui.QStyle.SP_MediaSeekForward, 
QtGui.QStyle.SP_MediaSeekBackward, 
QtGui.QStyle.SP_MediaVolume, 
QtGui.QStyle.SP_MediaVolumeMuted, 
QtGui.QStyle.SP_CustomBase, 
			]

ICON_DESRIPTION = {
QtGui.QStyle.SP_TitleBarMinButton: ('SP_TitleBarMinButton', 'Minimize button on title bars (e.g., in QMdiSubWindow).'),
QtGui.QStyle.SP_TitleBarMenuButton: ('SP_TitleBarMenuButton', 'Menu button on a title bar.'),
QtGui.QStyle.SP_TitleBarMaxButton: ('SP_TitleBarMaxButton', 'Maximize button on title bars.'),
QtGui.QStyle.SP_TitleBarCloseButton: ('SP_TitleBarCloseButton', 'Close button on title bars.'),
QtGui.QStyle.SP_TitleBarNormalButton: ('SP_TitleBarNormalButton', 'Normal (restore) button on title bars.'),
QtGui.QStyle.SP_TitleBarShadeButton: ('SP_TitleBarShadeButton', 'Shade button on title bars.'),
QtGui.QStyle.SP_TitleBarUnshadeButton: ('SP_TitleBarUnshadeButton', 'Unshade button on title bars.'),
QtGui.QStyle.SP_TitleBarContextHelpButton: ('SP_TitleBarContextHelpButton', 'The Context help button on title bars.'),
QtGui.QStyle.SP_MessageBoxInformation: ('SP_MessageBoxInformation', 'The "information" icon.'),
QtGui.QStyle.SP_MessageBoxWarning: ('SP_MessageBoxWarning', 'The "warning" icon.'),
QtGui.QStyle.SP_MessageBoxCritical: ('SP_MessageBoxCritical', 'The "critical" icon.'),
QtGui.QStyle.SP_MessageBoxQuestion: ('SP_MessageBoxQuestion', 'The "question" icon.'),
QtGui.QStyle.SP_DesktopIcon: ('SP_DesktopIcon', 'The "desktop" icon.'),
QtGui.QStyle.SP_TrashIcon: ('SP_TrashIcon', 'The "trash" icon.'),
QtGui.QStyle.SP_ComputerIcon: ('SP_ComputerIcon', 'The "My computer" icon.'),
QtGui.QStyle.SP_DriveFDIcon: ('SP_DriveFDIcon', 'The floppy icon.'),
QtGui.QStyle.SP_DriveHDIcon: ('SP_DriveHDIcon', 'The harddrive icon.'),
QtGui.QStyle.SP_DriveCDIcon: ('SP_DriveCDIcon', 'The CD icon.'),
QtGui.QStyle.SP_DriveDVDIcon: ('SP_DriveDVDIcon', 'The DVD icon.'),
QtGui.QStyle.SP_DriveNetIcon: ('SP_DriveNetIcon', 'The network icon.'),
QtGui.QStyle.SP_DirHomeIcon: ('SP_DirHomeIcon', 'The home directory icon.'),
QtGui.QStyle.SP_DirOpenIcon: ('SP_DirOpenIcon', 'The open directory icon.'),
QtGui.QStyle.SP_DirClosedIcon: ('SP_DirClosedIcon', 'The closed directory icon.'),
QtGui.QStyle.SP_DirIcon: ('SP_DirIcon', 'The directory icon.'),
QtGui.QStyle.SP_DirLinkIcon: ('SP_DirLinkIcon', 'The link to directory icon.'),
QtGui.QStyle.SP_FileIcon: ('SP_FileIcon', 'The file icon.'),
QtGui.QStyle.SP_FileLinkIcon: ('SP_FileLinkIcon', 'The link to file icon.'),
QtGui.QStyle.SP_FileDialogStart: ('SP_FileDialogStart', 'The "start" icon in a file dialog.'),
QtGui.QStyle.SP_FileDialogEnd: ('SP_FileDialogEnd', 'The "end" icon in a file dialog.'),
QtGui.QStyle.SP_FileDialogToParent: ('SP_FileDialogToParent', 'The "parent directory" icon in a file dialog.'),
QtGui.QStyle.SP_FileDialogNewFolder: ('SP_FileDialogNewFolder', 'The "create new folder" icon in a file dialog.'),
QtGui.QStyle.SP_FileDialogDetailedView: ('SP_FileDialogDetailedView', 'The detailed view icon in a file dialog.'),
QtGui.QStyle.SP_FileDialogInfoView: ('SP_FileDialogInfoView', 'The file info icon in a file dialog.'),
QtGui.QStyle.SP_FileDialogContentsView: ('SP_FileDialogContentsView', 'The contents view icon in a file dialog.'),
QtGui.QStyle.SP_FileDialogListView: ('SP_FileDialogListView', 'The list view icon in a file dialog.'),
QtGui.QStyle.SP_FileDialogBack: ('SP_FileDialogBack', 'The back arrow in a file dialog.'),
QtGui.QStyle.SP_DockWidgetCloseButton: ('SP_DockWidgetCloseButton', 'Close button on dock windows (see also QDockWidget).'),
QtGui.QStyle.SP_ToolBarHorizontalExtensionButton: ('SP_ToolBarHorizontalExtensionButton', 'Extension button for horizontal toolbars.'),
QtGui.QStyle.SP_ToolBarVerticalExtensionButton: ('SP_ToolBarVerticalExtensionButton', 'Extension button for vertical toolbars.'),
QtGui.QStyle.SP_DialogOkButton: ('SP_DialogOkButton', 'Icon for a standard OK button in a QDialogButtonBox.'),
QtGui.QStyle.SP_DialogCancelButton: ('SP_DialogCancelButton', 'Icon for a standard Cancel button in a QDialogButtonBox.'),
QtGui.QStyle.SP_DialogHelpButton: ('SP_DialogHelpButton', 'Icon for a standard Help button in a QDialogButtonBox.'),
QtGui.QStyle.SP_DialogOpenButton: ('SP_DialogOpenButton', 'Icon for a standard Open button in a QDialogButtonBox.'),
QtGui.QStyle.SP_DialogSaveButton: ('SP_DialogSaveButton', 'Icon for a standard Save button in a QDialogButtonBox.'),
QtGui.QStyle.SP_DialogCloseButton: ('SP_DialogCloseButton', 'Icon for a standard Close button in a QDialogButtonBox.'),
QtGui.QStyle.SP_DialogApplyButton: ('SP_DialogApplyButton', 'Icon for a standard Apply button in a QDialogButtonBox.'),
QtGui.QStyle.SP_DialogResetButton: ('SP_DialogResetButton', 'Icon for a standard Reset button in a QDialogButtonBox.'),
QtGui.QStyle.SP_DialogDiscardButton: ('SP_DialogDiscardButton', 'Icon for a standard Discard button in a QDialogButtonBox.'),
QtGui.QStyle.SP_DialogYesButton: ('SP_DialogYesButton', 'Icon for a standard Yes button in a QDialogButtonBox.'),
QtGui.QStyle.SP_DialogNoButton: ('SP_DialogNoButton', 'Icon for a standard No button in a QDialogButtonBox.'),
QtGui.QStyle.SP_ArrowUp: ('SP_ArrowUp', 'Icon arrow pointing up.'),
QtGui.QStyle.SP_ArrowDown: ('SP_ArrowDown', 'Icon arrow pointing down.'),
QtGui.QStyle.SP_ArrowLeft: ('SP_ArrowLeft', 'Icon arrow pointing left.'),
QtGui.QStyle.SP_ArrowRight: ('SP_ArrowRight', 'Icon arrow pointing right.'),
QtGui.QStyle.SP_ArrowBack: ('SP_ArrowBack', 'Equivalent to SP_ArrowLeft when the current layout direction is Qt.LeftToRight, otherwise SP_ArrowRight.'),
QtGui.QStyle.SP_ArrowForward: ('SP_ArrowForward', 'Equivalent to SP_ArrowRight when the current layout direction is Qt.LeftToRight, otherwise SP_ArrowLeft.'),
QtGui.QStyle.SP_CommandLink: ('SP_CommandLink', 'Icon used to indicate a Vista style command link glyph.'),
QtGui.QStyle.SP_VistaShield: ('SP_VistaShield', 'Icon used to indicate UAC prompts on Windows Vista. This will return a null pixmap or icon on all other platforms.'),
QtGui.QStyle.SP_BrowserReload: ('SP_BrowserReload', 'Icon indicating that the current page should be reloaded.'),
QtGui.QStyle.SP_BrowserStop: ('SP_BrowserStop', 'Icon indicating that the page loading should stop.'),
QtGui.QStyle.SP_MediaPlay: ('SP_MediaPlay', 'Icon indicating that media should begin playback.'),
QtGui.QStyle.SP_MediaStop: ('SP_MediaStop', 'Icon indicating that media should stop playback.'),
QtGui.QStyle.SP_MediaPause: ('SP_MediaPause', 'Icon indicating that media should pause playback.'),
QtGui.QStyle.SP_MediaSkipForward: ('SP_MediaSkipForward', 'Icon indicating that media should skip forward.'),
QtGui.QStyle.SP_MediaSkipBackward: ('SP_MediaSkipBackward', 'Icon indicating that media should skip backward.'),
QtGui.QStyle.SP_MediaSeekForward: ('SP_MediaSeekForward', 'Icon indicating that media should seek forward.'),
QtGui.QStyle.SP_MediaSeekBackward: ('SP_MediaSeekBackward', 'Icon indicating that media should seek backward.'),
QtGui.QStyle.SP_MediaVolume: ('SP_MediaVolume', 'Icon indicating a volume control.'),
QtGui.QStyle.SP_MediaVolumeMuted: ('SP_MediaVolumeMuted', 'Icon indicating a muted volume control.'),
QtGui.QStyle.SP_CustomBase: ('SP_CustomBase', 'Base value for custom standard pixmaps; custom values must be greater than this value.'),
				}

class Window(QtGui.QWidget):
	
	def __init__(self):
		QtGui.QWidget.__init__(self)
		
		self.setWindowTitle('Qt Standard Icons')
		
		self.mainLayout = QtGui.QGridLayout()
		self.create_menu()
		self.mainLayout.setMenuBar(self.menuBar)
		self.setLayout(self.mainLayout)
		self.build_widgets()		
		
		self.resize(400, 500)
		screen = QtGui.QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 3)
		
	def create_menu(self):
		self.menuBar = QtGui.QMenuBar()

		self.fileMenu = QtGui.QMenu("&File", self)
		self.fileMenu.addAction("E&xit", self.app_exit, 'Alt+F4')
		
		self.menuBar.addMenu(self.fileMenu)

	def app_exit(self, *args):
		sys.exit(0)
		
	def build_widgets(self):
		self.model=QtGui.QStandardItemModel(0, 3, self)
		self.set_model()
		self.view = QtGui.QTreeView(self)	
		self.view.setRootIsDecorated(False)
		self.view.setAlternatingRowColors(True)	
		self.setContentsMargins(0, 0, 0, 0)
		self.mainLayout.addWidget(self.view)
		self.view.setModel(self.model)
		
	def set_model(self):		
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Icon")
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Name")
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Description")
		for item in ICON_LIST:
			icon =self.style().standardIcon(item)
			point = QtGui.QStandardItem(icon, QtCore.QString(''))
			text1 = QtGui.QStandardItem()
			text1.setData(ICON_DESRIPTION[item][0], QtCore.Qt.DisplayRole)
			text2 = QtGui.QStandardItem()
			text2.setData(ICON_DESRIPTION[item][1], QtCore.Qt.DisplayRole)
			
			self.model.appendRow([point, text1, text2])

		
		
	
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	mw = Window()
	mw.show()
	sys.exit(app.exec_())			
		
		