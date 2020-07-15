'''
https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/CocoaViewsGuide/SubclassingNSView/SubclassingNSView.html
'''
from Foundation import NSLog
from AppKit import NSView, NSColor, NSAffineTransform, NSMutableParagraphStyle, NSAttributedString, NSFont, NSFontAttributeName, NSForegroundColorAttributeName, NSParagraphStyleAttributeName, NSRectFill #, NSBezierPath, NSRect
import traceback
from vanilla.vanillaBase import VanillaBaseObject


class MFGlyphView(NSView):

	def drawRect_(self, rect):
		# self._layer.drawInFrame_(bounds)  # used in Georgs GlyphView
		try:
			print("__test__")
			bounds = self.bounds()
			NSColor.textBackgroundColor().set()
			NSRectFill(bounds)
			scaleFactor = self._scaleFactor

			thisGlyph = self._layer.parent
			layerWidth = self._layer.width * scaleFactor
			descender = self._layer.glyphMetrics()[3] * scaleFactor
			ascender = self._layer.glyphMetrics()[1] * scaleFactor

			## This order is important! Wont work the other way around.
			bezierPathOnly = self._layer.bezierPath # Path Only
			if bezierPathOnly is not None:
				bezierPathOnly = bezierPathOnly.copy()
			bezierPathWithComponents = self._layer.completeBezierPath  # Path & Components
			bezierPathOpenWithComponents = self._layer.completeOpenBezierPath  # Path & Components
			
			# Set the scale
			#--------------
			scale = NSAffineTransform.transform()
			scale.translateXBy_yBy_((bounds.size.width - layerWidth) / 2.0, (bounds.size.height - ascender + descender) / 2.0 - descender)
			scale.scaleBy_(scaleFactor)
			
			
			# Draw only path in black
			#------------------------
			if thisGlyph.export:
				pathColor = NSColor.textColor()
				componentColor = NSColor.secondaryLabelColor()
			else:
				pathColor = NSColor.orangeColor()
				componentColor = NSColor.orangeColor()
				
			if bezierPathWithComponents:
				bezierPathWithComponents.transformUsingAffineTransform_(scale)
				componentColor.set() # Draw components in gray
				bezierPathWithComponents.fill()
			if bezierPathOnly:
				pathColor.set()
				bezierPathOnly.transformUsingAffineTransform_(scale)
				bezierPathOnly.fill()
			if bezierPathOpenWithComponents:
				pathColor.set()
				bezierPathOpenWithComponents.transformUsingAffineTransform_(scale)
				bezierPathOpenWithComponents.stroke()
			# Draw non-exported glyphs in orange
			#-----------------------------------
			else:
				NSColor.orangeColor().set()
				bezierPathWithComponents.transformUsingAffineTransform_(scale)
				bezierPathWithComponents.fill()
			
			attributes = {}
			attributes[NSFontAttributeName] = NSFont.systemFontOfSize_(14)
			
			thisLKG = thisGlyph.leftKerningGroup
			thisRKG = thisGlyph.rightKerningGroup
			if thisLKG is not None:
				String = NSAttributedString.alloc().initWithString_attributes_(thisLKG, attributes)
				String.drawAtPoint_alignment_((12, 5), 0)
			if thisRKG is not None:
				String = NSAttributedString.alloc().initWithString_attributes_(thisRKG, attributes)
				String.drawAtPoint_alignment_((bounds.size.width - 12, 5), 2)

			# AUTO-WIDTH LABEL
			#-----------------
			if self._layer.hasAlignedWidth():
				attributes[NSForegroundColorAttributeName] = NSColor.lightGrayColor()
				attributes[NSFontAttributeName] = NSFont.systemFontOfSize_(11)
				String = NSAttributedString.alloc().initWithString_attributes_("Auto-Width", attributes)
				String.drawAtPoint_alignment_((bounds.size.width / 2.0, 5), 1)
		except:
			print(traceback.format_exc())
			
class GlyphView(VanillaBaseObject):

	nsGlyphPreviewClass = MFGlyphView

	def __init__(self, posSize, layer=None):
		self._setupView(self.nsGlyphPreviewClass, posSize)
		# self._scaleFactor = 1;
		self.layer = layer
	@property
	def layer(self):
		return self._nsObject._layer
	@layer.setter
	def layer(self, value):
		self._nsObject._layer = value
		self._nsObject.setNeedsDisplay_(True)
