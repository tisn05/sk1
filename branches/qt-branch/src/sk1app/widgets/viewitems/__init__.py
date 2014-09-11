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

from uc2.sk1doc import model

import structural
import primitives

CID_TO_ITEM = {
	model.DOCUMENT: structural.DocumentItem,

	model.METAINFO: None, model.STYLES: None, model.STYLE: None,
	model.PROFILES: None, model.PROFILE: None, model.FONTS: None,
	model.FONT: None, model.IMAGES: None, model.IMAGE: None,

	model.PAGES: structural.PagesItem,
	model.PAGE: structural.PageItem,
	model.LAYER_GROUP: structural.LayerGroupItem,
	model.MASTER_LAYERS: structural.MasterLayersItem,
	model.LAYER: structural.LayerItem,
	model.GRID_LAYER: structural.GridLayerItem,
	model.GUIDE_LAYER: structural.GuideLayerItem,

	model.GROUP: None, model.CLIP_GROUP: None,
	model.TEXT_BLOCK: None, model.TEXT_COLUMN: None,

	model.RECTANGLE: primitives.RectangleItem,
	model.CIRCLE: None,
	model.POLYGON: None, model.CURVE: None,
	model.CHAR: None, model.PIXMAP: None,
	}
