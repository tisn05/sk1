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
from PyQt4 import Qt, QtGui
from xml.sax import handler

def gtk_to_tk_color(color):
	"""
	Converts gtk color representation to tk.
	For example: #0000ffff0000 will be converted to #00ff00
	"""
	return color[0] + color[1] + color[2] + color[5] + color[6] + color[9] + color[10]

def tkcolor_to_rgb(tkcolor):
	"""
	Converts tk color string as tuple of integer values.
	For example: #ff00ff => (255,0,255)
	"""
	return (int(tkcolor[1:3], 0x10), int(tkcolor[3:5], 0x10), int(tkcolor[5:], 0x10))

def rgb_to_tkcolor(r, g, b):
	"""
	Converts integer values as tk color string.
	For example: (255,0,255) => #ff00ff
	"""
	return '#%02X%02X%02X' % (r, g, b)

def saturated_color(color):
	"""
	Returns saturated color value. 
	"""
	r, g, b = tkcolor_to_rgb(color)
	delta = 255 - max(r, g, b)
	return rgb_to_tkcolor(r + delta, g + delta, b + delta)
				
def middle_color(dark, light, factor=0.5):
	"""
	Calcs middle color value.
	
	dark, light - tk color strings
	factor - resulted color shift 
	"""
	dark = tkcolor_to_rgb(dark)
	light = tkcolor_to_rgb(light)
	r = dark[0] + (light[0] - dark[0]) * factor
	g = dark[1] + (light[1] - dark[1]) * factor
	b = dark[2] + (light[2] - dark[2]) * factor
	return rgb_to_tkcolor(r, g, b)

def lighter_color(color, factor):
	"""
	Calcs lighted color value according factor.
	
	color - tk color strings
	factor - resulted color shift   
	"""
	return middle_color(color, saturated_color(color), factor)

def qt_saturated_color(qcolor):
	"""
	Returns saturated QColor value. 
	"""
	r, g, b = tkcolor_to_rgb(qcolor.name())
	delta = 255 - max(r, g, b)
	return Qt.QColor(rgb_to_tkcolor(r + delta, g + delta, b + delta))

def qt_middle_color(dark, light, factor=0.5):
	"""
	Calcs middle color value.
	
	dark, light - QColor instances
	factor - resulted color shift 
	"""
	dark = tkcolor_to_rgb(dark.name())
	light = tkcolor_to_rgb(light.name())
	r = dark[0] + (light[0] - dark[0]) * factor
	g = dark[1] + (light[1] - dark[1]) * factor
	b = dark[2] + (light[2] - dark[2]) * factor
	return Qt.QColor(rgb_to_tkcolor(r, g, b))

def qt_lighter_color(color, factor):
	"""
	Calcs lighted color value according factor.
	
	color - QColor instance
	factor - resulted color shift   
	"""
	color = color.name()
	return Qt.QColor(middle_color(color, saturated_color(color), factor))

class ColorPlate(QtGui.QWidget):
	
	def __init__(self, color=None, factor=1):
		QtGui.QWidget.__init__(self)
		self.color = color
		self.factor = factor

	def paintEvent(self, *args):		
		painter = QtGui.QPainter(self)
		painter.setPen(QtGui.QColor(0, 0, 0))
		painter.save()
		if self.color:
			painter.fillRect(0, 0, self.width()*self.factor - 1, self.height() - 1, self.color)
		painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
		painter.restore()
		
	def set_color(self, color):
		self.color = color
		self.update()
	
def draw_icon():
	colors = [
			QtGui.QColor(255, 0, 0), QtGui.QColor(0, 0, 255), QtGui.QColor(128, 128, 0),
			QtGui.QColor(128, 0, 128), QtGui.QColor(255, 128, 0), QtGui.QColor(128, 128, 255),
			QtGui.QColor(0, 128, 0), QtGui.QColor(128, 0, 0), QtGui.QColor(255, 255, 255),
			]
	icon = Qt.QPixmap(16, 16)
	painter = QtGui.QPainter(icon)
	painter.fillRect(0, 0, 15, 15, QtGui.QColor(255, 255, 255))
	painter.setPen(QtGui.QColor(0, 0, 0))
	line = 0;row = 0
	for color in colors:
		painter.fillRect(row * 5, line * 5, row * 5 + 5, line * 5 + 5, color)
		row += 1
		if row == 3:
			row = 0
			line += 1
	painter.drawRect(0, 0, 15, 15)
	painter.drawLine(0,5,15,5)
	painter.drawLine(0,10,15,10)
	painter.drawLine(5,0,5,15)
	painter.drawLine(10,0,10,15)
	return icon

class Window(QtGui.QWidget):
	
	colors = {}
	widgets = {}
	qt_color_list = [
				'alternateBase',
				'background',
				'base',
				'button',
				'buttonText',
				'dark',
				'foreground',
				'highlight',
				'highlightedText',
				'light',
				'link',
				'linkVisited',
				'mid',
				'midlight',
				'shadow',
				'text',
				'toolTipBase',
				'toolTipText',
				'window',
				'windowText',
				]
	
	def __init__(self):
		QtGui.QWidget.__init__(self)
		
		self.setWindowTitle('QtPalette')
		self.setWindowIcon(Qt.QIcon(draw_icon()))
		
		self.mainLayout = QtGui.QGridLayout()
		self.create_menu()
		self.mainLayout.setMenuBar(self.menuBar)
		self.setLayout(self.mainLayout)
		self.build_widgets()		
		
		self.resize(400, 500)
		screen = QtGui.QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 3)

		self.set_palette(self.get_qt_palette())
		
	
	def build_widgets(self,):
		colors = self.qt_color_list		
		i = 0
		brush = self.palette().background()
		for item in colors:
			label = QtGui.QLabel(item + ":")
								
			colorPlate = ColorPlate(brush)
			colorPlate.resize(250, 35)
			self.widgets[item] = colorPlate
			
			self.mainLayout.addWidget(label, i + 1, 0)
			self.mainLayout.addWidget(colorPlate, i + 1, 1)
			i += 1
		
	def get_qt_palette(self):
		qt_colors = {
					'alternateBase' : self.palette().alternateBase(),
					'background' : self.palette().background(),
					'base' : self.palette().base(),
					'button' : self.palette().button(),
					'buttonText' : self.palette().buttonText(),
					'dark' : self.palette().dark(),
					'foreground' : self.palette().foreground(),
					'highlight' : self.palette().highlight(),
					'highlightedText' : self.palette().highlightedText(),
					'light' : self.palette().light(),
					'link' : self.palette().link(),
					'linkVisited' : self.palette().linkVisited(),
					'mid' : self.palette().mid(),
					'midlight' : self.palette().midlight(),
					'shadow' : self.palette().shadow(),
					'text' : self.palette().text(),
					'toolTipBase' : self.palette().toolTipBase(),
					'toolTipText' : self.palette().toolTipText(),
					'window' : self.palette().window(),
					'windowText' : self.palette().windowText(),
					}
		return qt_colors

			
	def set_palette(self, palette):
		self.colors = palette
		for item in self.qt_color_list:
			self.widgets[item].set_color(palette[item])
			
	def create_menu(self):
		self.menuBar = QtGui.QMenuBar()

		self.fileMenu = QtGui.QMenu("&File", self)
		
		self.fileMenu.addAction("&New", self.file_new, 'Ctrl+N')
		self.fileMenu.addSeparator()
		self.fileMenu.addAction("&Open", self.file_open, 'Ctrl+O')
		self.fileMenu.addAction("&Save", self.file_save, 'Ctrl+S')
		self.fileMenu.addSeparator()
		self.fileMenu.addAction("E&xit", self.app_exit, 'Alt+F4')
		
		self.menuBar.addMenu(self.fileMenu)

	def app_exit(self, *args):
		sys.exit(0)
		
	def file_new(self):
		self.set_palette(self.get_qt_palette())
		self.setWindowTitle('QtPalette')
			
	def file_open(self):
		filter = 'QtPalette files - *.qtpal' + ' (*.qtpal)' + ';;'
		filter += "All Files" + ' (*.*)'
		filename = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open File - QtPalette',
															os.path.expanduser('~'), filter))
		if os.path.isfile(filename):
			self.palette_load(filename)
	
	def file_save(self):
		filter = 'QtPalette files - *.qtpal' + ' (*.qtpal)' + ';;'
		filter += "All Files" + ' (*.*)'
		filename = unicode(QtGui.QFileDialog.getSaveFileName(self, 'Save As - QtPalette',
															os.path.expanduser('~/unnamed palette.qtpal'), filter))
		self.palette_save(filename)
	
	def palette_save(self, filename):
		if not filename:
			return
		from xml.sax.saxutils import XMLGenerator

		try:
			file = open(filename, 'w')
		except (IOError, os.error), value:
			sys.stderr('cannot write palette into %s: %s' % (`filename`, value[1]))
			return
	
		writer = XMLGenerator(out=file, encoding='utf-8')
		writer.startDocument()
		items = self.colors.items()
		items.sort()
		writer.startElement('palette', {})
		writer.characters('\n')
		for key, value in items:
			value = value.color().name()
			writer.characters('\t')
			writer.startElement('%s' % key, {})
			writer.characters('%s' % value)				
			writer.endElement('%s' % key)
			writer.characters('\n')
		writer.endElement('palette')
		writer.endDocument()
		file.close
	
	def palette_load(self, filename):
		import xml.sax
		from xml.sax.xmlreader import InputSource
		palette = {}
		content_handler = XMLPrefReader(palette)
		error_handler = ErrorHandler()
		entity_resolver = EntityResolver()
		dtd_handler = DTDHandler()
		try:
			input = open(filename, "r")
			input_source = InputSource()
			input_source.setByteStream(input)
			xml_reader = xml.sax.make_parser()
			xml_reader.setContentHandler(content_handler)
			xml_reader.setErrorHandler(error_handler)
			xml_reader.setEntityResolver(entity_resolver)
			xml_reader.setDTDHandler(dtd_handler)
			xml_reader.parse(input_source)
			input.close
		except:
			pass
		if palette:
			self.set_palette(palette)			
			self.setWindowTitle('QtPalette - ' + os.path.basename(filename))
		
		
class XMLPrefReader(handler.ContentHandler):
	"""Handler for xml file reading"""
	def __init__(self, palette=None):
		self.key = None
		self.value = None
		self.palette = palette

	def startElement(self, name, attrs):
		self.key = name

	def endElement(self, name):
		if name != 'palette':
			self.palette[self.key] = Qt.QColor(self.value)

	def characters(self, data):
		self.value = data

class ErrorHandler(handler.ErrorHandler): pass
class EntityResolver(handler.EntityResolver): pass
class DTDHandler(handler.DTDHandler): pass


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	mw = Window()
	mw.show()
	sys.exit(app.exec_())
