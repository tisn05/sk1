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

from controllers import AbstractController

class RectangleCreator(AbstractController):

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)
		self.flag = 1

	def mouse_down(self, event):
		self.start = self.end = event.pos()
		if event.button() == Qt.Qt.LeftButton:
			self.draw = True

	def mouse_move(self, event):
		self.end = event.pos()
		if self.draw and self.flag:
			self.flag = 0
			self.canvas.draw_frame(self.start, self.end)
		else:
			self.flag = 1

	def mouse_up(self, event):
		if event.button() == Qt.Qt.LeftButton:
			self.canvas.stop_draw_frame()
			self.end = event.pos()
			self.draw = False
			if self.start and self.end:
				change = self.end - self.start
				if abs(change.x()) < 5 and abs(change.y()) < 5:
					pass
				else:
					self.canvas.create_rectangle(self.start, self.end)
			self.end = []
			self.start = []
