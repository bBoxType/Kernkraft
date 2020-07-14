# encoding: utf-8

###########################################################################################################
#
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import KernKraftModule as KKM

from Kernschmelze import KernschmelzeWindow
from GlyphsApp import Glyphs
from GlyphsApp.plugins import *

import traceback

class KernkraftPlugin(GeneralPlugin):
	@objc.python_method
	def settings(self):
		self.name = "Kernkraft"
	@objc.python_method
	def start(self):
		try:
			mainMenu = NSApplication.sharedApplication().mainMenu()
			glyphMenu = mainMenu.itemWithTag_(7).submenu()
			s = objc.selector(self.kernkraft_, signature=b'v@:@')
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Kernkraft", s, "")
			newMenuItem.setTarget_(self)
			glyphMenu.addItem_(newMenuItem)
			s = objc.selector(self.kernschmelze_, signature=b'v@:@')
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Kernschmelze", s, "")
			newMenuItem.setTarget_(self)
			glyphMenu.addItem_(newMenuItem)
		except:
			NSLog(traceback.format_exc())

	def kernkraft_(self, sender):
		try:
			thisFont = Glyphs.font
			mID = thisFont.selectedFontMaster.id
			kkk = KKM.KernKraft(Glyphs, thisFont, mID)
		except:
			NSLog(traceback.format_exc())

	def kernschmelze_(self, sender):
		try:
			thisFont = Glyphs.font
			KernschmelzeWindow(thisFont)
		except:
			NSLog(traceback.format_exc())
