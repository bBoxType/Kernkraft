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
			
			## This order is important! Wont work the other way around.
			try: # pre Glyphs 2.3
				bezierPathOnly = self._layer.copy().bezierPath()  # Path Only
				bezierPathWithComponents = self._layer.copyDecomposedLayer().bezierPath() # Path & Components				
			except: # Glyphs 2.3
				bezierPathOnly = self._layer.copy().bezierPath  # Path Only
				bezierPathWithComponents = self._layer.copyDecomposedLayer().bezierPath  # Path & Components			


			# Set the scale
			#--------------
			scale = NSAffineTransform.transform()
			scale.translateXBy_yBy_( rectWidth/2 - (layerWidth / 2.0) + self._margin/2, -descender + self._margin/2 )
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
			
			# AUTO-WIDTH LABEL
			#-----------------
			if self._layer.hasAlignedWidth():
				paragraphStyle = NSMutableParagraphStyle.alloc().init()
				paragraphStyle.setAlignment_(2) ## 0=L, 1=R, 2=C, 3=justified
				attributes = {}
				attributes[NSFontAttributeName] = NSFont.systemFontOfSize_(10)
				attributes[NSForegroundColorAttributeName] = NSColor.lightGrayColor()
				attributes[NSParagraphStyleAttributeName] = paragraphStyle
				String = NSAttributedString.alloc().initWithString_attributes_("Auto-Width", attributes)
				# String.drawAtPoint_((rectWidth, 0))
				NSColor.redColor().set()
				# NSRectFill(((0, 0), (self.rect.size.width, 15)))
				String.drawInRect_(((0, 0), (self.rect.size.width, 15)))
		except:
			pass # print traceback.format_exc()
			

