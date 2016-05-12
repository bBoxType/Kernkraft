#MenuTitle: Kernschmelze (beta)
# -*- coding: utf-8 -*-
__doc__ = """
• Interpolate Kerning from 2 Source Masters
• Or copy Kerning from one of the Source Masters
• Equalize number Kerning Pairs, fill empty ones with 0
"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#	_NOTES:
#		- 
#
#	_TODO:
#		- include Width & Custom Values, HUH??
#		- `Scale` is currently based on masters weight value, do we need to incorporate other values?
#
#	>> Mark Froemberg << aka `Mark2Mark` @ GitHub
#	>> www.markfromberg.com <<
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


'''
--> Interpolate Kerning to Target Masters from 2 Source Masters
--> Copy Kerning from one of the Source Masters to Target Master
--> Equalize Kerning (match num of Kerning Pairs, fill empty ones with value 0)
	a) only for the 2 Source Masters (when no Target Masters are chosen)
	b) for the 2 Source Masters (when Target Masters get Kerning)
	= Always applied on run
'''


from vanilla import *
import traceback
from GlyphsApp import *
Glyphs.clearLog()
# Glyphs.showMacroWindow()

# font = Glyphs.font
# thisMasterID = font.selectedFontMaster.id


version = "0.7"
class KernschmelzeWindow(object):

	def __init__(self, font):

		self.font = font

		#------------------------------------------------------
		### MONKEY PATCH
		### Create custom functions to [Vanilla] Objects:
		def __setID(self, customTitle):
			'''
			SET ACCESSIBILITY TITLE OR IDENTIFIER TO CALL OBJECT BY IT
			'''			
			self._nsObject.setIdentifier_(customTitle)
			###### print help(self._nsObject)

		def __getID(self):
			'''
			GET ACCESSIBILITY TITLE OR IDENTIFIER TO CALL OBJECT BY IT
			'''			
			return self._nsObject.identifier()

		def __enable(self, onOff):
			'''
			REDUCING THE ALPHA FOR DEACTIVATED OBJECTS
			*UC* Not disabling a PopUpButton
			'''
			alpha = onOff + 0.3
			try: self._checkBox.enable(onOff)
			except:	pass
			try: self._nsObject.setAlphaValue_(alpha)
			except:	pass

			try: self._textButton.enable(onOff)
			except: pass
			try: self._nsObject.setAlphaValue_(alpha)
			except: pass

			# try:
			# 	self._nsObject.enable(onOff)
			# except:
			# 	pass
			# try:
			# 	self._nsObject.setAlphaValue_(alpha)
			# except:
			# 	pass

		### Add custom functions to [PopUpButton, CheckBox]:
		PopUpButton.setID = __setID
		PopUpButton.getID = __getID
		# PopUpButton.enable = __enable # Monkey Patch, override given enable()
		CheckBox.setID = __setID
		CheckBox.getID = __getID
		# CheckBox.enable = __enable # Monkey Patch, override given enable()
		#------------------------------------------------------






		tab1 = 40
		tab2 = 245
		y = 10

		source_Options = []
		for i, m in enumerate(self.font.masters):
			## Keep index in there, so same titled masters won’t be swallowed by unique checkbox requirement
			source_Options.append(u"%s)  \"%s\"  [%s Pairs]" % (i+1, m.name, str( len( self.getKerningFromMaster(m) ) ) ) )

		self.UI_sourceMasterA = None
		self.UI_sourceMasterB = None

		# init dictionary master options with index 0
		self.masterOptions = {}
		for mi, m in enumerate(self.font.masters):
			self.masterOptions[mi] = 0

		self.UI_SelectedTargetMasters = []

		self.w = Window((0, 0), "Kernschmelze (beta)")
		self.w.SourceMastersLabel = TextBox((10, y, -10, 20), "Source Masters:", alignment="center" )
		y += 25
		self.w.SourceMasterALabel = TextBox((10, y, -10, 20), u"🅐 =" )
		self.w.SourceMasterA = PopUpButton((tab1, y, -10, 20), source_Options, callback=self.getSourceMasterA, sizeStyle="small")
		y += 25
		self.w.SourceMasterBLabel = TextBox((10, y, -10, 20), u"🅑 =" )
		self.w.SourceMasterB = PopUpButton((tab1, y, -10, 20), source_Options, callback=self.getSourceMasterB, sizeStyle="small" )
		y += 50
		self.w.CopyMastersLabel = TextBox((10, y, -10, 20), "Apply Kerning to:", alignment="center" )
		y += 25
		for i, master in enumerate(self.font.masters):
			
			attrNameLine = "Line_%s" % str(i)
			line = HorizontalLine((10, y, -10, 1))
			setattr(self.w, attrNameLine, line)
			y += 8
			attrNameTargetMaster = "CopyMasters_%s" % str(i)
			checkBoxTargetMaster = CheckBox((10, y, tab2, 20), "", sizeStyle="small", callback=self.makeTargetMasters) # str(master.name)
			checkBoxTargetMaster.setID(str(i)) # MONKEY PATCH
			setattr(self.w, attrNameTargetMaster, checkBoxTargetMaster)
			exec("self.w.CopyMasters_" + str(i) + ".setTitle('\"%s\"  [%s Pairs]" % (str(master.name), str(len(self.getKerningFromMaster( master )))) + "')")

			attrNameSourceMaster = "FromMaster_%s" % str(i)
			radioGroupSourceMaster = PopUpButton((tab2, y, -10, 20), ["Interpolate", u"Copy from 🅐", u"Copy from 🅑"], sizeStyle="small", callback=self.targetMastersOptions )
			radioGroupSourceMaster.setID(str(i)) # MONKEY PATCH
			setattr(self.w, attrNameSourceMaster, radioGroupSourceMaster)
			exec("self.w.FromMaster_" + str(i) + ".set(0)")
			y += 28
		
		y += 10
		self.w.button = Button((10, y, -10, 20), "Select Source Masters first", callback=self.buttonCallback)
		self.w.button.enable(0)
		y += 30

		self.w.resize(390, y)
		self.w.center()
		self.w.open()

	def makeTargetMasters(self, sender):
		masterID = int(sender.getID())
		master = self.font.masters[masterID]
		status = sender.get()
		if status == 1:
			if master not in self.UI_SelectedTargetMasters:
				self.UI_SelectedTargetMasters.append(master)
		if status == 0:
			if master in self.UI_SelectedTargetMasters:
				self.UI_SelectedTargetMasters.remove(master)
		# print self.UI_SelectedTargetMasters


	def targetMastersOptions(self, sender):
		masterID = int(sender.getID())
		status = sender.get()
		self.masterOptions[masterID] = status
		print self.masterOptions

	def getSourceMasterA(self, sender):
		self.UI_sourceMasterA = [self.font.masters[sender.get()], sender.get()]
		self.toggleAvailability()


	def getSourceMasterB(self, sender):
		self.UI_sourceMasterB = [self.font.masters[sender.get()], sender.get()]
		self.toggleAvailability()


	def toggleAvailability(self):

		for i, master in enumerate(self.font.masters):
			# exec("thisMaster = self.w.CopyMasters_" + str(i) + ".getTitle()")
			thisMasterIndex = i
			# if thisMaster == self.w.SourceMasterA.getTitle() or thisMaster == self.w.SourceMasterB.getTitle():  # tile
			if thisMasterIndex == self.w.SourceMasterA.get() or thisMasterIndex == self.w.SourceMasterB.get():  # index
				exec("thisMaster = self.w.CopyMasters_" + str(i) + ".enable(0)")
				exec("thisMaster = self.w.CopyMasters_" + str(i) + ".set(0)")
				exec("thisMaster = self.w.FromMaster_" + str(i) + ".enable(0)")

			else:
				exec("thisMaster = self.w.CopyMasters_" + str(i) + ".enable(1)")
				exec("thisMaster = self.w.FromMaster_" + str(i) + ".enable(1)")
				

		if self.UI_sourceMasterA != None and self.UI_sourceMasterB != None:
			self.w.button.enable(1)
			self.w.button.setTitle("Schmelz!")


	def getKerningFromMaster(self, fontMaster):
		# print "__sourceMaster:", fontMaster.name ## sourceMasterA or sourceMasterB
		try:
			thisKerning = self.font.kerning[fontMaster.id]
		except:
			# if no kerning in fontMaster:
			thisKerning = {}

		thisKerningCollection = []
		for leftSide, rightSide in thisKerning.iteritems():
			if leftSide[:5] != "@MMK_":  # if single glyph (exception to Kerning Group)
				leftSide = self.font.glyphForId_( leftSide ).name

			for item in rightSide.viewitems():
				value = item[1]
				if item[0][:5] != "@MMK_":  # if single glyph (exception to Kerning Group)
					#print "----> %s" % font.glyphForId_( item[0] ).name
					rightSide = self.font.glyphForId_( item[0] ).name
				else:
					rightSide = item[0]

				# print item
				thisKerningCollection.append([leftSide, rightSide, value ])

		### DEBUG
		# print "__thisKerningCollection:"
		# print "  %s Pairs:" % len(thisKerningCollection)
		# for x in thisKerningCollection:
		# 	print x
		# print

		return thisKerningCollection



	def EQKerningPairs(self, KerningM1, KerningM2, fillValue=None):
		kernDict = {}
		self.separator = " -- "
		## iterate over M1 to render dict
		for A in KerningM1:
			pair = "%s%s%s" % (A[0], self.separator, A[1])
			valueA = A[2]
			kernDict[pair] = [valueA]

		## iterate over M2 to fill up given pairs and append non existing ones
		for B in KerningM2:
			pair = "%s%s%s" % (B[0], self.separator, B[1])
			valueB = B[2]
			try:
				kernDict[pair].append(valueB)
			except:
				kernDict[pair] = [fillValue, valueB] # case: 1st M has no entry for this pair, set it to 0

		## iterate over M1 afain to fill up newly added pairs from M2
		for A in KerningM1:
			pair = "%s%s%s" % (A[0], self.separator, A[1])
			valueA = A[2]
			if len (kernDict[pair]) == 1:
				kernDict[pair] = [valueA, fillValue] # case: 2nd M has no entry for this pair, set it to 0


		# for key, val in kernDict.iteritems():
		# 	print key.split(self.separator), val
		return kernDict



	def interpolate(self, a, b, location):
		''' location = interpolation factor '''
		interpolatedValue = a + location * (b - a)
		return int(interpolatedValue)


	def copyKerning(self, choice):
		''' COPY KERNING '''
		if choice == 1:
			copiedKernValue = self.KernValue_A
		if choice == 2:
			copiedKernValue = self.KernValue_B
		print choice
		try:
			self.font.setKerningForPair(self.master.id, '%s'  % self.leftSide_K, '%s'  % self.rightSide_K, copiedKernValue)
		except:
			print traceback.format_exc()



	def buttonCallback(self, sender):
		self.w.close()

		try:

			'''
			Define the master IDs
			'''
			UI_SelectedMasterA_IDX = self.UI_sourceMasterA[1]
			UI_SelectedMasterAValue = self.UI_sourceMasterA[0].weightValue

			UI_SelectedMasterB_IDX = self.UI_sourceMasterB[1]
			UI_SelectedMasterBValue = self.UI_sourceMasterB[0].weightValue


			'''
			EQ KERNING
			'''
			### EQUALIZE BOTH SOURCE MASTERS, FILL UP NON MATCHING PAIRS WITH VALUE 0
			kerningACollection = self.getKerningFromMaster(self.UI_sourceMasterA[0])
			kerningBCollection = self.getKerningFromMaster(self.UI_sourceMasterB[0])		
			for key, values in self.EQKerningPairs(kerningACollection, kerningBCollection).iteritems():
				pair = key.split(self.separator)
				self.leftSide_K, self.rightSide_K = pair
				self.KernValue_A, self.KernValue_B = values
				# print self.leftSide_K, self.rightSide_K, self.KernValue_A, self.KernValue_B
				if self.KernValue_A == None:
					self.font.setKerningForPair(self.UI_sourceMasterA[0].id, '%s' % self.leftSide_K, '%s' % self.rightSide_K, 0)
					# print "set %s (%s %s) to ZERO" % (self.UI_sourceMasterA[0].name, self.leftSide_K, self.rightSide_K)
				if self.KernValue_B == None:
					self.font.setKerningForPair(self.UI_sourceMasterB[0].id, '%s' % self.leftSide_K, '%s' % self.rightSide_K, 0)
					# print "set %s (%s %s) to ZERO" % (self.UI_sourceMasterB[0].name, self.leftSide_K, self.rightSide_K)





			'''
			APPLY KERNING TO TARGET MASTERS
			'''
			for i, master in enumerate(self.font.masters):
				## include only selected Target Masters:	
				self.master = master

				## exclude Source Masters:
				if i != UI_SelectedMasterA_IDX and i != UI_SelectedMasterB_IDX:  # by index
					print "Master: %s - Option: %s" % (i, self.masterOptions[i])
					
					if master in self.UI_SelectedTargetMasters:

						### same iteration as above in the Master-EQing, but this time for EACH TARGET MASTER
						### I(!): reset kerning_Collection, to get the equalized(!) Kerning (masters with added zero-values):
						kerningACollection = self.getKerningFromMaster(self.UI_sourceMasterA[0])
						kerningBCollection = self.getKerningFromMaster(self.UI_sourceMasterB[0])
						for key, values in self.EQKerningPairs(kerningACollection, kerningBCollection).iteritems():
							pair = key.split(self.separator)
							print pair
							self.leftSide_K, self.rightSide_K = pair
							self.KernValue_A, self.KernValue_B = values

							### copy kerning
							if self.masterOptions[i] != 0:
								self.copyKerning(self.masterOptions[i])
				

							if self.masterOptions[i] == 0:
								### interpolate kerning
								scale = UI_SelectedMasterAValue + UI_SelectedMasterBValue # weight values of Master_A + Master_B
								location = master.weightValue / scale # return factor 0…1 for interpolation, exceeding for extrapolation
								try:
									self.font.setKerningForPair(master.id, '%s' % self.leftSide_K, '%s' % self.rightSide_K, self.interpolate(self.KernValue_A, self.KernValue_B, location))
								except:
									print traceback.format_exc()


		except:
			print traceback.format_exc()

