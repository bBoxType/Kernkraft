'''
https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/CocoaViewsGuide/SubclassingNSView/SubclassingNSView.html
'''
from AppKit import NSView, NSColor, NSAffineTransform, NSMutableParagraphStyle, NSAttributedString, NSFont, NSFontAttributeName, NSForegroundColorAttributeName, NSParagraphStyleAttributeName # NSRectFill, NSBezierPath, NSRect
import traceback

class GlyphView(NSView):

	def drawRect_(self, rect): ## must be `drawRect_` - nothing else

		bounds = self.bounds()
		scaleFactor = self._scaleFactor
		thisUPM = self._upm * scaleFactor # = self._layer.parent.parent.upm
		rectX, rectY, rectWidth, rectHeight = 0, 0, thisUPM, thisUPM
		self.rect = rect

		# self._layer.drawInFrame_(bounds)  # used in Georgs GlyphView

		try:
			thisGlyph = self._layer.parent
			layerWidth = self._layer.width * scaleFactor
			descender = self._layer.glyphMetrics()[3] * scaleFactor
			ascender = self._layer.glyphMetrics()[1] * scaleFactor

			## This order is important! Wont work the other way around.
			try: # Glyphs 2.3
				bezierPathOnly = self._layer.bezierPath.copy()  # Path Only
				bezierPathWithComponents = self._layer.copyDecomposedLayer().bezierPath  # Path & Components
			except: # Glyphs 2.4
				bezierPathOnly = self._layer.bezierPath.copy()  # Path Only
				bezierPathWithComponents = self._layer.completeBezierPath  # Path & Components


			# Set the scale
			#--------------
			scale = NSAffineTransform.transform()
			scale.translateXBy_yBy_((bounds.size.width - layerWidth) / 2.0, (bounds.size.height - ascender + descender) / 2.0 - descender)
			scale.scaleBy_( scaleFactor )

			if bezierPathWithComponents:
				bezierPathWithComponents.transformUsingAffineTransform_( scale )
			if bezierPathOnly:
				bezierPathOnly.transformUsingAffineTransform_( scale )

			# Draw components in gray
			#------------------------
			NSColor.darkGrayColor().set() # lightGrayColor
			bezierPathWithComponents.fill()
			
			
			# Draw only path in black
			#------------------------
			if thisGlyph.export:
				NSColor.blackColor().set()
				if bezierPathOnly:
					bezierPathOnly.fill()
			# Draw non-exported glyphs in orange
			#-----------------------------------
			else:
				NSColor.orangeColor().set()
				bezierPathWithComponents.fill()
			
			attributes = {}
			attributes[NSFontAttributeName] = NSFont.systemFontOfSize_(14)
			
			thisLKG = thisGlyph.leftKerningGroup
			thisRKG = thisGlyph.rightKerningGroup
			if thisLKG != None:
				String = NSAttributedString.alloc().initWithString_attributes_(thisLKG, attributes)
				String.drawAtPoint_alignment_((12, 5), 0)
			if thisRKG != "None":
				String = NSAttributedString.alloc().initWithString_attributes_(thisRKG, attributes)
				String.drawAtPoint_alignment_((self.rect.size.width - 12, 5), 2)

			# AUTO-WIDTH LABEL
			#-----------------
			if self._layer.hasAlignedWidth():
				attributes[NSForegroundColorAttributeName] = NSColor.lightGrayColor()
				attributes[NSFontAttributeName] = NSFont.systemFontOfSize_(11)
				String = NSAttributedString.alloc().initWithString_attributes_("Auto-Width", attributes)
				String.drawAtPoint_alignment_((self.rect.size.width / 2.0, 5), 1)
		except:
			print(traceback.format_exc())
			

