#MenuTitle: Kernkraft (beta)
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
#	>> www.carrois.com <<
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import KernkraftLib.KernKraftModule as KKM
reload(KKM)

version = "1.8"

thisFont = Glyphs.font
mID = thisFont.selectedFontMaster.id

kkk = KKM.KernKraft(Glyphs, thisFont, mID)
