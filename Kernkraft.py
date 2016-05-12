#MenuTitle: Kernkraft beta 1.8 Launcher
# -*- coding: utf-8 -*-
__doc__ = """
Kerning the Carrois Way
"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# --> Code written by
#	>> Mark Froemberg << aka `mark2mark` @ GitHub
#	>> www.markfromberg.com <<
#
# --> Based on the kerning procedure in Glyphsapp by
#	>> Ralph Du Carrois <<
#	>> type.carrois.com <<
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import KernkraftLib.KernKraftModule as KKM
reload(KKM)

thisFont = Glyphs.font
mID = thisFont.selectedFontMaster.id

kkk = KKM.KernKraft(Glyphs, thisFont, mID)
