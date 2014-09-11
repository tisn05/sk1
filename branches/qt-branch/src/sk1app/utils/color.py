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

from PyQt4 import Qt

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
	r, g, b = tkcolor_to_rgb(str(qcolor.name()))
	delta = 255 - max(r, g, b)
	return Qt.QColor(rgb_to_tkcolor(r + delta, g + delta, b + delta))

def qt_middle_color(dark, light, factor=0.5):
	"""
	Calcs middle QColor value.
	
	dark, light - QColor instances
	factor - resulted color shift 
	"""
	dark = tkcolor_to_rgb(str(dark.name()))
	light = tkcolor_to_rgb(str(light.name()))
	r = dark[0] + (light[0] - dark[0]) * factor
	g = dark[1] + (light[1] - dark[1]) * factor
	b = dark[2] + (light[2] - dark[2]) * factor
	return Qt.QColor(rgb_to_tkcolor(r, g, b))

def qt_lighter_color(color, factor):
	"""
	Calcs lighted QColor value according factor.
	
	color - QColor instance
	factor - resulted color shift   
	"""
	return Qt.QColor(qt_middle_color(color, qt_saturated_color(color), factor))
