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

from PyQt4 import QtGui, Qt

from widgets import graphview
from sk1app.widgets import ruler

class DrawingArea(QtGui.QFrame):
	
	def __init__(self, parent, app, presenter):
		
		QtGui.QFrame.__init__(self, parent)
		
		self.app = app
		self.presenter = presenter
		
		self.build()
		self.setAutoFillBackground(True)		
		self.setMinimumSize(400, 300)
		
	def build(self):
		self.main_layout = QtGui.QGridLayout()

		self.canvas = graphview.GVCanvas(self, self.presenter)

		self.ruler_corner = ruler.RulerCorner(self, self.app, self.presenter)
		self.main_layout.addWidget(self.ruler_corner, 0, 0)
		
		self.h_ruler = ruler.Ruler(self.app, self, self.presenter, ruler.HORIZONTAL)
		self.main_layout.addWidget(self.h_ruler, 0, 1, 1, 1)
				
		self.v_ruler = ruler.Ruler(self.app, self, self.presenter, ruler.VERTICAL)
		self.main_layout.addWidget(self.v_ruler, 1, 0, 1, 1)
		self.main_layout.addWidget(self.canvas, 1, 1)

		self.main_layout.setContentsMargins(2, 1, 2, 2)	
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)
		
	def paintEvent(self, *args):		
		painter = QtGui.QPainter(self)
		painter.setPen(self.palette().mid().color())
		painter.save()
		painter.drawLine(0, 0, 0, self.height() - 1)
		painter.drawLine(0, self.height() - 1, self.width() - 1, self.height() - 1)		
		painter.drawLine(self.width() - 1, self.height() - 1, self.width() - 1, 0)
		painter.restore()

	def closeEvent(self, event):
		if self.app.close(self.presenter):
			event.accept()			
		else:
			event.ignore()
