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

from PyQt4 import QtGui, Qt, QtCore

DOCK_WIDTH = 200

class AbstractDock(QtGui.QDockWidget):
	
	def __init__(self, title, mw):
		
		QtGui.QDockWidget.__init__(self, ' ' + title, mw)
		self.mw = mw
		self.app = mw.app
		self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		self.policy = QtGui.QSizePolicy()
		self.policy.setVerticalPolicy(QtGui.QSizePolicy.Fixed)
		self.policy.setHorizontalPolicy(QtGui.QSizePolicy.Fixed)
		self.line_color = self.palette().shadow().color()
		self.bg_color = Qt.QColor('#ffffff')
		self.black_color = Qt.QColor('#000000')
		self.top_color = Qt.QColor('#6B6864')
		
		
		self.setMinimumWidth(DOCK_WIDTH)
		
	def paintEvent(self, arg):	
		painter = QtGui.QPainter(self)
		painter.save()
		painter.setPen(self.line_color)
		painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
		painter.restore()
		painter.end()
		QtGui.QDockWidget.paintEvent(self, arg)
		
