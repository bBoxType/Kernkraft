# -*- coding: utf-8 -*-

# Code written by Mark Frömberg ( @Mark2Mark, markfromberg.com )
# Kerning procedure by Ralph du Carrois ( @Carrois, www.carrois.com )

# TODO:
# 	+ BUG: when kerning SC `a.sc` it opens way too many tabs (29 in fira instad of 3 like with `A`)
# 	+ rewrite variables, better names
# 	+ sort functions by UI and Tool functionality
#	+ Kerning strings for CamelCase (e.g: »drawAtPoint« etc), maybe as an option?

# Changelog:
# 	1.9
#		+ Use Glyph with Group-Name if given (instead of first Group Member) [only if BOTH sides KG are the same]
# 	1.9.2
#		+ New Function: Include all occurrences of the Input Glyph in other scripts (Option in UI)
#		  (Showing only the Category `Letter`)
# 	1.9.3
#		+ Add `Private Use` to the UI as an option to skip.
# 	1.9.4
#		+ Fix crash caused by function introduced in 1.9.2 with Glyphs builds below 911 (bypassing, thanks Botio)
# 	1.9.6
#		+ Add editable Kering Group Text Boxes (commented out, not working here (just in the stand alone snippet))
# 	1.9.7
#		+ updated deprecated Method layer.drawBezierPath w/ layer.completeBezierPath
#	1.9.8
#		+ Add Thai to kernKit
#	1.9.9
#		+ New "Done" List, which automatically adds items with each Glyph to Tab(s).
#		+ Drawer remembers status now.
#	2.0.0
#		+ Fix CheckBox bug (Same as in Reporter Toggler)



import os
from vanilla import *
import traceback
import preview as preview
import kernKit as KK
import Customizables
from GlyphsApp import Glyphs
from Foundation import NSColor, NSUserDefaults, NSMakeRange
from AppKit import NSScreen, NSNoBorder


# # # # # # # # #
debugMode = False
# Glyphs.clearLog()
# # # # # # # # #

try:
	reload(Customizables)
except: pass
excludedSubCategories = Customizables.excludedSubCategories


screenHeight = NSScreen.mainScreen().frame().size.height
noTransform = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0) # components that are not transformed in any way.


##########################################################################
##########################################################################
##########################################################################
##########################################################################



class KernKraft(object):

	version = "2.0.0"
	# excludeCategories = []

	def __init__(self, Glyphs, thisFont, mID):

		self.Glyphs = Glyphs
		self.thisFont = thisFont
		self.mID = mID

		self.allGlyphsInFont = [g.name for g in self.thisFont.glyphs] ## genuinely all glyphs
		self.firstGlyphInFont = self.allGlyphsInFont[0]

		# User Interface
		#---------------
		self.prefwindow = PreferenceWindow(self)

		# Kerning Strings
		#----------------
		self.kenringStrings = KK.KerningStrings().customKenringStrings

		# Defaults
		#---------
		# Reset on submitButtonCallback via UI Selections or certain function calls
		self.skippedCategories = None
		self.writingDirection = 0 # LTR
		# self.firstGlyphInFont = self.allGlyphsInFont[0]  # using global var
		self.errorCollector = []

		self.allowedCategories = [
			"Letter",
			"Number",
			"Punctuation",
			"Symbol",
			"Math",
			"Private Use",
		] ## for the glyphs put downwards step by step between the to-be-kerned glyph
		self.prohibitedCategories = [ "Mark", "Separator" ]

		self.kerningRelations = ["noGroupToNoGroup", "groupToGroup", "groupToNoGroup", "noGroupToGroup"  ]

		self.showAllScripts = [] # mutable collector for all occurrences of the input glyph in other scripts.



	#==============
	# H E L P E R S
	#==============

	def debugPrint(self, s):
		if debugMode:
			print s


	def escName(self, glyphName):
		''' MAKE GLYPH NAME ESCAPED (e.g. `/alpha`) '''
		return "/" + glyphName


	def caseOfLigature(self, glyphName):
		cases = []
		for i in glyphName.split("_"):
			cases.append(i.islower())
		return cases


	def raiseMessage(self, messageTrigger):
		if messageTrigger == "Glyph not in Font":
			Message("Hell no!", "That glyph is not part of the Font. Please try again.", OKButton="OK")



	#==============
	# F I L T E R S
	#==============

	def addSuffixToTails(self, thisGlyphName, leftTail, rightTail):
		''' rewrite kerning string tails to match number suffix. E.g. `/zero/*/zero` -> `/zero.lf/*.lf/zero.lf` '''
		tails = []
		possibleNumberSuffixes = ["lf", "osf", "dnom", "numr", "hb"]  # more? Include dnom & numr? **UC**
		numberSuffix = thisGlyphName.split(".")[-1]
		if numberSuffix in possibleNumberSuffixes:
			tails.append( "".join(['/{0}.{1}'.format(x, numberSuffix) for x in leftTail.split("/")][1:]) )  # leftTail
			tails.append( "".join(['/{0}.{1}'.format(x, numberSuffix) for x in rightTail.split("/")][1:]) )  # rightTail
		return tails


	def getKerningGroupMembers(self, glyphName, side):
		''' *new in 1.7* '''
		for itrG in self.thisFont.glyphs:
			if side == "L":
				if itrG.leftKerningGroup == self.thisFont.glyphs[glyphName].leftKerningGroup:
					yield itrG.name
			if side == "R":
				if itrG.rightKerningGroup == self.thisFont.glyphs[glyphName].rightKerningGroup:
					yield itrG.name

	# def getKerningGroupMembers(seolf, glyphName, side): # Draft for improving getKerningGroupMembers()
	# 	_thisGlyph = thisFont.glyphs[glyphName]
	# 	_LKG = _thisGlyph.leftKerningGroup
	# 	_RKG = _thisGlyph.rightKerningGroup

	# 	for itrG in self.thisFont.glyphs:
	# 		_itrLKG = itrG.leftKerningGroup
	# 		_itrRKG = itrG.rightKerningGroup

	# 		if side == "L":
	# 			if _itrLKG == _LKG:
	# 				yield itrG.name
	# 		if side == "R":
	# 			if _itrRKG == _RKG:
	# 				yield itrG.name


	def checkIfKGIsAGlyph(self, KerningGroupName):
		if KerningGroupName in self.allGlyphsInFont:
			return True
		else:
			return False


	# def skipForExcludedSubCategories(self, glyphName, category, subCategory):
	# 	''' *new in 1.7* '''
	# 	for item in excludedSubCategories:
	# 		[thisCat, thisSubCat], dic = item
	# 		# if glyphName.split(".")[0] in dic['Exceptions']:  # DEBUG
	# 		# 	print "++++++++++ in exceptions, kept in", glyphName  # DEBUG
	# 		if glyphName.split(".")[0] not in dic['Exceptions']:  # let through all suffixed versions (e.g. ampersand, ampersand.ss01, etc)
	# 			if category == thisCat:
	# 				if subCategory == thisSubCat:
	# 					if debugMode:
	# 						print '{:10}{:45}{} {} {}'.format("skipped:", glyphName, u"-> excluded Cat & SubCat:", thisCat, thisSubCat)
	# 					return True  # Skip
	# 		else:
	# 			return False  # Don’t Skip


	def skipForExcludedSubCategories(self, inputGlyphName, glyphName, category, subCategory):
		''' *new in 1.7* '''
		for item in excludedSubCategories:
			[thisCat, thisSubCat], dic = item
			# if glyphName.split(".")[0] in dic['Exceptions']:  # DEBUG
			# 	print "++++++++++ in exceptions, kept in", glyphName  # DEBUG
			if glyphName.split(".")[0] not in dic['Exceptions']:  # let through all suffixed versions (e.g. ampersand, ampersand.ss01, etc)
				if category == thisCat:
					if subCategory == thisSubCat:
						if ".sc" in inputGlyphName and ".sc" in glyphName: # * 1.8
							return False # CASE: Input is SC, hence do not skip here
						self.debugPrint( '{:10}{:45}{} {} {}'.format("skipped:", glyphName, u"-> excluded Cat & SubCat:", thisCat, thisSubCat) )
						return True  # Skip
			else:
				return False  # Don’t Skip





	#================================
	# C H E C K S   F O R   R E U S E
	#================================
	# 1
	def glyphIsReusedInAnotherScipt(self, glyphName, masterID): # *new in 1.9.2*

		if Glyphs.buildNumber >= 911:

			collector = []

			thisGlyphsReusedGlyphs = self.thisFont.glyphsContainingComponentWithName_masterID_(glyphName, self.thisFont.masters[masterID].id)
			if len(thisGlyphsReusedGlyphs) > 0:
				for glyph in thisGlyphsReusedGlyphs:
					masterLayer = glyph.layers[masterID]
					layerComponents = masterLayer.components
					if len(layerComponents) == 1:
						if len(masterLayer.paths) == 0:
							if layerComponents[0].componentName == glyphName:
								if layerComponents[0].transform == noTransform:
									collector.append(glyph.name)
				if len(collector) > 0:
					collector.insert(0, glyphName)
					return collector
				return None
		else:
			return None

	# 2
	def glyphsWithSameKG(self, glyphName, masterID): # *new in 1.9.5*
		''' *Not active yet* '''
		# also catch the glyphs with the same KG on both sides:
		if Glyphs.buildNumber >= 911:

			collector = []

			try:
				thisGlyphLKG = self.thisFont.glyphs[glyphName].leftKerningGroup
				thisGlyphRKG = self.thisFont.glyphs[glyphName].rightKerningGroup
				for ggg in [self.thisFont.glyphs[g] for g in self.allGlyphsInFont]:
					if thisGlyphLKG == ggg.leftKerningGroup and thisGlyphRKG == ggg.rightKerningGroup:
						collector.append(ggg.name)

				if len(collector) > 0:
					collector.insert(0, glyphName)
					return list(set(collector))
				return None

			except:
				print traceback.format_exc()

		else:
			return None

	# TODO: Also add another, third check: If all the components are reused the same way. E.g.: idieresis --> iotadieresis
	# 3
	def sameComponentSetup(self, glyphName, masterID):
		'''
			Return list of GlyphNames that are made from the same components as the Input Glyph (including that one)
			Avoids situations like:
			`jdotlessstrokehook > [u'ghook', u'jdotlessstrokehook', u'dhook', u'eshcurl', u'qhook']`
			So it also checkes that not paths are in the layer
		'''
		if Glyphs.buildNumber >= 911:

			collector = []

			try:

				try:
					thisGlyphComponents = [c.componentName for c in self.thisFont.glyphs[glyphName].layers[self.mID].components]
				except:
					thisGlyphComponents = None

				if thisGlyphComponents and len(self.thisFont.glyphs[glyphName].layers[self.mID].paths) == 0:
					for ggg in self.allGlyphsInFont:
						try:
							iteratedGlyphComponents = [c.componentName for c in self.thisFont.glyphs[ggg].layers[self.mID].components]
						except:
							iteratedGlyphComponents = None

						if iteratedGlyphComponents and len(self.thisFont.glyphs[ggg].layers[self.mID].paths) == 0:
							if thisGlyphComponents == iteratedGlyphComponents:
								collector.append(ggg)

					if len(collector) > 0:
						collector.insert(0, glyphName)
						return list(set(collector))
					return None

			except:
				print traceback.format_exc()

		else:
			return None





	def stringMaker(self, inputGlyphName, inputGlyphScript, itrGlyphName, itrGlyphCase, removeUIGlyphAtSide=None):
		''' GENERATE THE STRING ACCORDING TO THE GIVEN PREREQUISITES '''
		try:
			category = self.thisFont.glyphs[inputGlyphName].category
			subCategory = self.thisFont.glyphs[inputGlyphName].subCategory

			if inputGlyphScript == "hebrew":
				self.writingDirection = 1 # RTL

			tailFallback = "/n/n"

			try:
				gCat = self.kenringStrings[inputGlyphScript][category]
			except:
				gCat = None
				gCatError = "__NOTE: Input Glyph '%s' did not find a nice kerning string. Will use a default string." % inputGlyphName
				if gCatError not in self.errorCollector:
					self.errorCollector.append(gCatError)

			try:
				leftTail = gCat[subCategory]['Left']
			except:
				leftTail = tailFallback
			try:
				rightTail = gCat[subCategory]['Right']
			except:
				rightTail = tailFallback

			try:
				leftTailUC = gCat["Uppercase"]['Left']
			except:
				leftTailUC = tailFallback

			try:
				rightTailLC = gCat["Lowercase"]['Right']
			except:
				rightTailLC = tailFallback


			if category == "Number":
				try:
					leftTail = self.addSuffixToTails(inputGlyphName, leftTail, rightTail)[0]
					rightTail = self.addSuffixToTails(inputGlyphName, leftTail, rightTail)[1]
				except: pass


			thisLine = ""
			keyGlyph = self.escName(inputGlyphName)  # --> *
			itrGlyph = self.escName(itrGlyphName)  # --> #


			if self.thisFont.glyphs[itrGlyphName].subCategory == "Ligature":  # if last glyph of liga is LC
				if self.caseOfLigature(itrGlyphName)[-1]:
					itrGlyphCase = "Lowercase"

			## Hacky forcement of Smallcaps treatment into given the switches below
			if subCategory == "Smallcaps" and itrGlyphCase == "Uppercase":
				leftTail = gCat["Uppercase"]['Left']
				subCategory = "Lowercase"



			# HANDLING OF LC-UC-RELATIONS
			#----------------------------
			# change HHOH#*#NNOI to HHOH#*nnoi [* = UC] (if not chop right)
			# Case: keyGlyph is LC, itrGlyph is LC
			if itrGlyphCase == "Lowercase" and subCategory == "Uppercase":
				if removeUIGlyphAtSide == "chopRight": # the only case that is possible here next to default (else), since left side aint there anyway
					thisLine = None
				else:
					thisLine = leftTail + keyGlyph + itrGlyph + rightTailLC  # HHOH*#nnoi

			# change HHOH#*#nnoi to HHOH#*nnoi  [* = LC] (if not chop left)
			# Case: keyGlyph is LC, itrGlyph is UC
			elif itrGlyphCase == "Uppercase" and subCategory == "Lowercase":
				if removeUIGlyphAtSide == "chopLeft": # the only case that is possible here next to default (else), since right side aint there anyway
					thisLine = None
				else:
					thisLine = leftTailUC  + itrGlyph + keyGlyph + rightTail

			# change nnon#*#nnoi to HHOH#*#nnoi (in else)
			elif subCategory == "Lowercase":
				if removeUIGlyphAtSide == "chopLeft":
					thisLine = leftTailUC + keyGlyph + itrGlyph + rightTail  # HHOH*#nnoi
				elif removeUIGlyphAtSide == "chopRight":
					thisLine = leftTailUC + itrGlyph + keyGlyph + rightTail  # HHOH#*nnoi
				else:
					thisLine = leftTailUC + keyGlyph + itrGlyph + keyGlyph + rightTail

			# default thisLine HHOH#*#HOOI (in else)
			else:
				if removeUIGlyphAtSide == "chopLeft":
					thisLine = leftTail + keyGlyph + itrGlyph + rightTail  # HHOH*#HHOI
				elif removeUIGlyphAtSide == "chopRight":
					thisLine = leftTail + itrGlyph + keyGlyph + rightTail  # HHOH#*HHOI
				else:
					thisLine = leftTail + keyGlyph + itrGlyph + keyGlyph + rightTail

			return thisLine

		except:
			print traceback.format_exc()







	def checkKerningForPair(self, relation, G1, G2, anyKerning):
		''' append kerning to any Kerning if any of these pair-relations match'''
		# TODO: Rewrite as dictionary

		if relation == "noGroupToNoGroup":
			thisKerning = self.kfp(self.mID, '%s' % G1, '%s' % G2)
			# print "noGroupToNoGroup %s %s" % (G1, G2)

		if relation == "groupToGroup":
			thisKerning = self.kfp(self.mID, '@MMK_L_%s' % self.thisFont.glyphs[G1].rightKerningGroup, '@MMK_R_%s' % self.thisFont.glyphs[G2].leftKerningGroup)
			# print "groupToGroup %s %s" % (G1, G2)

		if relation == "groupToNoGroup":
			thisKerning = self.kfp(self.mID, '@MMK_L_%s' % self.thisFont.glyphs[G1].rightKerningGroup, '%s' % G2)
			# print "groupToNoGroup %s %s" % (G1, G2)

		if relation == "noGroupToGroup":
			thisKerning = self.kfp(self.mID, '%s'  % G1, '@MMK_R_%s' % self.thisFont.glyphs[G2].leftKerningGroup)
			# print "noGroupToGroup %s %s" % (G1, G2)

		try:
			if thisKerning not in anyKerning:
				# print thisKerning
				anyKerning.append(thisKerning)
		except:
			print traceback.format_exc()



	# def returnKerningBool(self, inputGlyph, iteratedGlyph, anyKerning, side):
	#	'''WHY IS THIS FUNCTION NOT WORKING PROPERLY ???? '''
	# 	if len(anyKerning) == 1 and anyKerning[0].__long__() == 9223372036854775808:
	# 		return False # no kerning set
	# 	else:
	# 		print "skipped %s, %s, (%s) [2b]" % (inputGlyph, iteratedGlyph, side)
	# 		return True # kerning set




	def hasKerning(self, inputGlyph, iteratedGlyph, side):
		''' UNDER CONSTRUCTION, STILL VERY COMPLEX '''
		''' Also:  why is the returnKerningBool() not working like expected? '''
		### check if kerning is already in the pair

		try:
			anyKerningRight = []
			anyKerningLeft = []

			self.kfp = self.thisFont.kerningForPair

			# 1A)	RIGHT -> RIGHT SIDE OF INPUT GLYPH
			#---------------------------------------
			if side == "rightKerning":
				pairAndKerningSide = inputGlyph, iteratedGlyph, anyKerningRight
				for kerningRelation in self.kerningRelations:
					self.checkKerningForPair(kerningRelation, *pairAndKerningSide)

				anyKerning = anyKerningRight
				# self.returnKerningBool(inputGlyph, iteratedGlyph, anyKerning, side)
				if len(anyKerning) == 1 and anyKerning[0].__long__() == 9223372036854775808:
					return False # no kerning set
				else:
					# print "skipped %s, %s, (%s) [2a]" % (inputGlyph, iteratedGlyph, side)
					return True # kerning set


			# 2A)	LEFT -> LEFT SIDE OF INPUT GLYPH
			#-------------------------------------
			if side == "leftKerning":
				pairAndKerningSide = iteratedGlyph, inputGlyph, anyKerningLeft
				for kerningRelation in self.kerningRelations:
					self.checkKerningForPair(kerningRelation, *pairAndKerningSide)

				anyKerning = anyKerningLeft
				# self.returnKerningBool(inputGlyph, iteratedGlyph, anyKerning, side)
				if len(anyKerning) == 1 and anyKerning[0].__long__() == 9223372036854775808:
					return False # no kerning set
				else:
					# print "skipped %s, %s, (%s) [2b]" % (inputGlyph, iteratedGlyph, side)
					return True # kerning set

		except:
			print traceback.format_exc()




	#================
	# C O N T R O L S
	#================

	def deactivateReporters(self):
		try:
			for reporter in self.Glyphs.activeReporters:
				self.Glyphs.deactivateReporter(reporter)
		except:
			print traceback.format_exc()


	def setupTab(self):
		# ZOOM TO POINT SIZE & SET WRITING DIRECTION
		#-------------------------------------------
		zoomFactor = self.UIPointSize/1000.0
		thisTab = self.Glyphs.font.tabs[-1]

		thisTab.graphicView().zoomViewToAbsoluteScale_( zoomFactor )
		thisTab.setWritingDirection_( self.writingDirection )
		try: thisTab.previewHeight = 80
		except: pass # pre Glyphs 2.3 +
		thisTab.setMasterIndex_(self.prefwindow.w.ChoseMaster.get())

		# SET CARET INTO POSITION
		#------------------------
		# **NOT 100 PERCENT READY**
		ContentView = self.Doc.windowController().activeEditViewController().contentView()
		# location = len( ContentView.textStorage().string() ) -6  # len of rightTail
		location = len( ContentView.textStorage().text() ) -6  # len of rightTail // change in API, Glyphs 2.4 AND 2.5
		myRange = NSMakeRange( location, 0 ) # 0 = length
		GraphicView = self.Doc.windowController().activeEditViewController().graphicView()
		GraphicView.setSelectedRange_( myRange )

		GraphicView.setToolTip_("Kernkraft Tab")

		try: self.Glyphs.font.tool = 'TextTool'
		except: pass # pre Glyphs 2.3 +


	def makeTab(self, tabOutput):
		''' OUTPUT TO EDIT-TAB '''

		self.UIPointSize = float(self.prefwindow.drawer.pointSize.get())
		thisTabOutput = "\n".join(tabOutput)

		self.Doc = self.Glyphs.currentDocument
		if self.prefwindow.w.separateTabsUI.get() == False:
			self.Doc.windowController().addTabWithString_( thisTabOutput )
			self.setupTab()

		else:
			print
			splittedTabOutput =  thisTabOutput.split("\n__")
			for x in splittedTabOutput[1:]:  # 0 index would be empty, so we exclude it here
				self.Doc.windowController().addTabWithString_( "__%s" % x )
				self.setupTab()

		if debugMode:
			self.Glyphs.showMacroWindow()



	#========
	# M A I N
	#========

	def generateTabOutput(self, inputGlyphName, showLetterCategoryOnly=False):
		''' MAIN FUNCTION GENERATING THE KERNING STRINGS '''

		glyphsList = [g for g in self.thisFont.glyphs if g.category not in self.prohibitedCategories]


		UI_inputGlyph_Name = inputGlyphName


		isReused = self.glyphIsReusedInAnotherScipt(inputGlyphName, self.prefwindow.w.ChoseMaster.get())
		if isReused:
			self.showAllScripts = isReused
			self.showAllScripts.remove(inputGlyphName)

		# *new in 1.9.5*
		# sameComponents = self.sameComponentSetup(inputGlyphName, self.prefwindow.w.ChoseMaster.get())
		# if sameComponents:
		# 	try:
		# 		self.showAllScripts = list(set(isReused.append(sameComponents)))
		# 	except:
		# 		self.showAllScripts = sameComponents


		# *new in 1.9.5*
		# isReused_B = self.glyphsWithSameKG(inputGlyphName, self.prefwindow.w.ChoseMaster.get())
		# if isReused_B:
		# 	try:
		# 		self.showAllScripts = isReused.append(isReused_B)
		# 	except:
		# 		self.showAllScripts = isReused_B
		# 	print "-_-_-_-_-_", self.showAllScripts
		# 	# self.showAllScripts.remove(inputGlyphName)




		UI_SkipComponents = self.prefwindow.w.skipComponentCheck.get()
		UI_SkipKGMembers = self.prefwindow.w.skipKGMembersCheck.get()
		UI_SkipAlreadyKernedLeftCheck = self.prefwindow.w.skipAlreadyKernedLeftCheck.get()
		UI_SkipAlreadyKernedRightCheck = self.prefwindow.w.skipAlreadyKernedRightCheck.get()

		UI_inputGlyph_Category = self.thisFont.glyphs[UI_inputGlyph_Name].category
		UI_inputGlyph_SubCategory = self.thisFont.glyphs[UI_inputGlyph_Name].subCategory

		UI_inputGlyph_LKG = self.thisFont.glyphs[UI_inputGlyph_Name].leftKerningGroup
		UI_inputGlyph_RKG = self.thisFont.glyphs[UI_inputGlyph_Name].rightKerningGroup
		UI_inputGlyph_LKGroupMembers = list(self.getKerningGroupMembers(UI_inputGlyph_Name, "L"))
		UI_inputGlyph_RKGroupMembers = list(self.getKerningGroupMembers(UI_inputGlyph_Name, "R"))


		### MAKE FUNCTION
		### **UC**, yield Bool if Glyph is KG-Representative
		UI_inputGlyph_IsLGK = False
		UI_inputGlyph_IsRGK = False
		if UI_inputGlyph_Name == UI_inputGlyph_LKG:
			self.debugPrint( (UI_inputGlyph_Name, "=", UI_inputGlyph_LKG, "LEFT") )
			UI_inputGlyph_IsLGK = True
		if UI_inputGlyph_Name == UI_inputGlyph_RKG:
			self.debugPrint( (UI_inputGlyph_Name, "=", UI_inputGlyph_RKG, "RIGHT") )
			UI_inputGlyph_IsRGK = True

		## make group key: either first item of group OR the letter itself, if in group
		if UI_inputGlyph_IsLGK:
			firstLKGItem = UI_inputGlyph_Name
		else:
			firstLKGItem = UI_inputGlyph_LKGroupMembers[0]
		if UI_inputGlyph_IsRGK:
			firstRKGItem = UI_inputGlyph_Name
		else:
			firstRKGItem = UI_inputGlyph_RKGroupMembers[0]
		###











		# VALIDATE UI INPUT
		#------------------
		if UI_inputGlyph_Name in self.allGlyphsInFont:
			tabOutput = []
			inputGlyphScript = self.thisFont.glyphs[UI_inputGlyph_Name].script

			''' ITERATE OVER ALL GLYPHS IN THE FONT THAT FULFILL CERTAIN REQUIREMENTS '''
			thisCategory = None


			itrGKerningGroups = []
			for idx, itrG in enumerate(glyphsList): ## excluding prohibited categories

				itrG_Name = itrG.name                # iteratedGlyphName
				itrG_LKG = itrG.leftKerningGroup     # iteratedGlyphLeftKenringGroup
				itrG_RKG = itrG.rightKerningGroup    # iteratedGlyphRightKenringGroup
				itrG_Script = itrG.script            # iteratedGlyphScript
				itrG_Cat = itrG.category             # iteratedGlyphCategory
				itrG_SubCat = itrG.subCategory       # iteratedGlyphSubCategory



				#==================================================================================
				# S K I P   A L L   C A T E G O R I E S   T H A T   A R E   N O T   ` L E T T E R `
				#==================================================================================
				# In the case of `Include Other Scripts` for the Input Glyph
				if showLetterCategoryOnly:
					if itrG_Cat != "Letter":
						continue


				#================
				# S K I P   . T F
				#================
				### CHECK IF `.tf` or `.tosf` is *IN* gName (not only at the end of gName)
				### Cover cases like `zero.tf.sc`
				# if itrG_Name[-3:] == ".tf" or itrG_Name[-5:] == ".tosf": # DEPRECATED
				if ".tf" in itrG_Name or ".tosf" in itrG_Name: # *new in 1.8*
					# print "__excluded %s for being .tf or .tosf" % itrG_Name
					continue


				#======================================================================================
				# S K I P   A L R E A D Y   K E R N E D   P A I R S   I F   S E L E C T E D   I N   U I
				#======================================================================================
				skipSide = None
				if UI_SkipAlreadyKernedRightCheck:
					## UNDER CONSTRUCTION
					if self.hasKerning(UI_inputGlyph_Name, itrG_Name, "rightKerning"):
						# print "__excluded %s for already kerned right" % itrG_Name
						self.debugPrint( "special Case [RK] %s" % itrG_Name )
						skipSide = "chopRight"
						# continue ## DONT CONTINUE, BUT REWRITE STRING
				if UI_SkipAlreadyKernedLeftCheck:
					## UNDER CONSTRUCTION
					if self.hasKerning(UI_inputGlyph_Name, itrG_Name, "leftKerning"):
						# print "__excluded %s for already kerned left" % itrG_Name
						self.debugPrint( "special Case [LK] %s" % itrG_Name )
						skipSide = "chopLeft"
						# continue ## DONT CONTINUE, BUT REWRITE STRING

				## Skip if BOTH sides do have kerning
				if UI_SkipAlreadyKernedRightCheck and UI_SkipAlreadyKernedLeftCheck:
					if self.hasKerning(UI_inputGlyph_Name, itrG_Name, "rightKerning") and self.hasKerning(UI_inputGlyph_Name, itrG_Name, "leftKerning"):
						self.debugPrint( "special Case [LK & RK] %s" % itrG_Name )
						continue


				#====================================================================
				# S K I P   N U M B E R S   W I T H   D I F F E R E N T   S Y N T A X
				#====================================================================
				if UI_inputGlyph_Category == "Number":
					# Case: e.g. input is `five.lf` then skip `five` (no .suffix) lines
					if itrG_Cat == "Number":
						if len(UI_inputGlyph_Name.split(".")) > 1:
							if UI_inputGlyph_Name.split(".")[-1] != itrG_Name.split(".")[-1]:
								continue
						# Case: e.g. input is `five` then skip `five.lf` (.suffix) lines
						elif "." not in UI_inputGlyph_Name: 	# no suffix meets
							if "." in itrG_Name:				# suffix
								if itrG_Name != "fraction":	# more than `fraction` to keep?
									continue


				#================================================================
				# S K I P   S M A L L C A P S   B E T W E E N   L O W E R C A S E
				#================================================================
				if UI_inputGlyph_SubCategory == "Smallcaps" and itrG_SubCat == "Lowercase":
					self.debugPrint( '{:10}{:45}{}'.format("skipped:", itrG_Name, "-> SC between LC") )
					continue


				#==============================
				# S K I P   C O M P O N E N T S
				#==============================
				# Under Construction
				if UI_SkipComponents:
					itrG_Layer = itrG.layers[self.mID]  # create this here, only if needed!
					if len(itrG_Layer.components) > 0 and len(itrG_Layer.paths) == 0:
						if itrG_Cat == "Letter": # or "Number" (Not using Number or it might exclude denominators or alike)
						# if itrG_Cat == "Number": # excluding Numbers, excludes denominators or alike **UC**
							self.debugPrint( '{:10}{:45}{}'.format("skipped:", itrG_Name, u"-> only components & category: 'Letter'") )
							continue


				#====================================================
				# S K I P   K E R N I N G   G R O U P   M E M B E R S
				#====================================================
				# *New in 1.7*
				# [PART A]
				# TODO: Is this Part A really neccessary?!

				if UI_SkipKGMembers:
					# print "__KG-inp: %s --%s-- %s" % (UI_inputGlyph_LKG, UI_inputGlyph_Name, UI_inputGlyph_RKG)
					# print "__KG-itr: %s --%s-- %s" % (itrG_LKG, itrG_Name, itrG_RKG)
					# print

					# if UI_inputGlyph_LKG == itrG_LKG:
					# 	print "match Left", itrG_LKG
					# if UI_inputGlyph_RKG == itrG_RKG:
					# 	print "match Right", itrG_RKG
					# ^^^ *** DITCH THAT ***

					## --------------------------------
					## SKIP KERNING GROUP MEMBERS A) (see end of chain for part B! )
					## SKIP MEMBERS OF INPUT GLYPH'S LKG & RKG
					if itrG_Name != firstLKGItem and itrG_Name != firstRKGItem:
						isLKGMember = False
						isRKGMember = False
						if itrG_Name in UI_inputGlyph_LKGroupMembers:
							# print "IN LKG:", itrG_Name
							isLKGMember = True
						if itrG_Name in UI_inputGlyph_RKGroupMembers:
							# print "IN RKG:", itrG_Name
							isRKGMember = True

						if isLKGMember and isRKGMember:
							self.debugPrint( '{:10}{:45}{}'.format("skipped:", itrG_Name, u"-> member of Input Glyph's LKG & RKG") )
							continue
					#####--------------------------------




				# '''
				# EXCLUDE CASES LIKE HEBREW PUNCTUATION IN LATIN OR CYRILLIC STRING
				### *UC* because it still excludes ALL Punctiation!!!
				# '''
				# if itrG_Cat == "Punctuation":
				# 	if inputGlyphScript != itrG_Script:
				# 		continue


				#========================================================================================================================
				# F I L T E R   S A M E   S C R I P T ;   C U R R E N T L Y   T H I S   E X C L U D E S   A L L   N O N   L E T T E R S !
				#========================================================================================================================
				if inputGlyphScript != None and itrG_Script != None:
					if itrG_Script != inputGlyphScript:
						self.debugPrint( "__excluded %s for not being input script (%s != %s)" % (itrG_Name, itrG_Script, inputGlyphScript) )
						continue


				#====================================
				# S K I P   U I   C A T E G O R I E S
				#====================================
				if itrG_Cat in self.skippedCategories:
					self.debugPrint( "__excluded %s for being Category excluded via UI" % itrG_Name )
					continue


				#====================================================
				# S K I P   D I S A L L O W E D   C A T E G O R I E S
				#====================================================
				if itrG_Cat not in self.allowedCategories:
					self.debugPrint( "__excluded %s for not being in allowedCategories (= %s)" % (itrG_Name, itrG_Cat) )
					continue


				#================================================
				# S K I P   S U B C A T E G O R I E S   *   1 . 7
				#================================================
				# if self.skipForExcludedSubCategories(itrG_Name, itrG_Cat, itrG_SubCat):
				if self.skipForExcludedSubCategories(UI_inputGlyph_Name, itrG_Name, itrG_Cat, itrG_SubCat): # * 1.8
					continue


				#==========================================================================================================================
				# E X C H A N G E   I T R G _ N A M E   B Y   K E R N I N G - G R O U P   I F   K G   =   G L Y P H   O F   T H E   F O N T
				#==========================================================================================================================
				# *New in 1.9*
				# Behaviour and position in algorithm chain = experimental (!)
				if UI_SkipKGMembers:
					if UI_SkipComponents:
						if itrG_LKG == itrG_RKG:
							if self.checkIfKGIsAGlyph(itrG_LKG): # use only left, because right is the same
								itrG_Name = itrG_LKG


				#====================================================
				# S K I P   K E R N I N G   G R O U P   M E M B E R S
				#====================================================
				# [PART B]
				# *New in 1.7*
				### !! KEEP AT END OF THIS CHAIN (otherwise it could perform the skip based on a glyph’s condition that might be skipped itself)
				if UI_SkipKGMembers:
					### SKIP IF THIS ITERATED GLYPH'S LKG & RKG where already displayed once
					if (itrG_LKG, itrG_RKG) in itrGKerningGroups:
						self.debugPrint( '{:10}{:45}{}'.format("skipped:", itrG_Name, u"-> sharing LKG & RKG of an already displayed Glyph [%s %s]" % (itrG_LKG, itrG_RKG) ) )
						continue
				## IPORTANT: add these only AFTER this ^ condition (but outside the UI_SkipKGMembers condition):
				if (itrG_LKG, itrG_RKG) not in itrGKerningGroups:
					if itrG_LKG != None and itrG_RKG != None:
						itrGKerningGroups.append( (itrG_LKG, itrG_RKG) )


				#================================================================================
				# T A G   T H E   C U R R E N T   C A T E G O R Y   I N T O   T H E   O U T P U T
				#================================================================================
				# (MAKE AN OPTION IN UI?)
				try:
					nexGlyph = glyphsList[idx + 1]
					nexGlyphCat = glyphsList[idx + 1].category
					categoryTag = "\n__%s:" % itrG_Cat
					if nexGlyph:
						# if nexGlyphCat == itrG_Cat:
						if thisCategory != itrG_Cat:
						# if nexGlyphCat != itrG_Cat:
							tabOutput.append( categoryTag )
							thisCategory = itrG_Cat
				except: pass


				#============================================
				# F E E D   T H E   A C T U A L   O U T P U T
				#============================================
				thisOutput = self.stringMaker(UI_inputGlyph_Name, inputGlyphScript, itrG_Name, itrG_SubCat, removeUIGlyphAtSide=skipSide)
				if thisOutput:
					tabOutput.append( thisOutput )

			self.makeTab(tabOutput)

		else:
			self.raiseMessage("Glyph not in Font")
			## reset default using first glyph in font
			self.prefwindow.w.glyphInput.set(self.firstGlyphInFont)
			self.Glyphs.defaults["%s.glyphInput" % self.prefwindow.vID] = self.firstGlyphInFont
			self.prefwindow.updateGlyphPreview(self.firstGlyphInFont)



##########################################################################
##########################################################################
##########################################################################
##########################################################################


# # For the editable TextBoxes
# #---------------------------
# class AppDelegate(NSObject): # New in 1.9.6

# 	def textDidChange_(self, sender):
# 		try:
# 			print sender.stringValue()
# 		except:
# 			pass #print traceback.format_exc()



class PreferenceWindow(object):

	def __init__(self, parent):
		super(PreferenceWindow, self).__init__()
		self.parent = parent
		# print help(self.parent)

		self.Glyphs = self.parent.Glyphs
		self.thisFont = self.parent.thisFont
		self.mID = self.parent.mID
		self.allGlyphsInFont = self.parent.allGlyphsInFont
		self.firstGlyphInFont = self.allGlyphsInFont[0]

		self.chosenMasterID = self.thisFont.selectedFontMaster.id # default as long as no master is chosen in the UI

		self.specialGuests = u"Ąj  Ą_  Ą)  Ęj  Ę_  Ę)  Įj  Į_  Į)  fï  Tï  Fï  *ï*  ‘ï‘  Ł⁰  Ł‘  ß‘  ß⁰  ¿j  ¿y  ¿g  c//o  …"


		self.catToSkipUI = ["Letter", "Number", "Punctuation", "Symbol", "Other", "Private Use", ]
		#### catToSkipUI--> UI will auto resize with items in this list; preferece save&load as well.
		#### The latter does so just for developping (load/save prefs with variable number of items is not recommended.)

		self.title = u"Kernkraft %s (beta)" % self.parent.version # ⚛
		self.vID = "com.markfromberg.kernkraft" # vendorID
		self.IOSTitle = "Include Other Scripts"

		rowHeight = 30
		mrgn = 5
		self.scrollViewMargin = 0
		m = 12
		bW = 25
		prevBox = 250.0
		layerScale = 1
		self.previewSize = self.thisFont.upm / (self.thisFont.upm / prevBox) # 2000 / (2000 / 300.0)  # keep same size (300) no matter which upm the font has
		windowWidth = self.previewSize # 230

		y = 0
		self.w = Window((50, 50, 0, 0), self.title, autosaveName="%s.mainwindow" % self.vID ) ## restore window position
		y += self.previewSize

		self.w.line_Scrooller = HorizontalLine((0, y, self.previewSize, 1))
		y += 8
		# ----------------------------------------------------------------------------------------------------
		# / KERN-GLYPH INPUT
		#
		self.w.glyphInput = EditText((m + bW + mrgn*2, y, -m - bW - mrgn*2, 23), placeholder="GlyphName", callback=self.SavePreferences)
		self.w.buttonLeft = Button((m, y, bW, 23 ), u"←", callback=self.buttonLeftCallback)
		self.w.buttonLeft.bind("leftarrow", [])
		self.w.buttonRight = Button(( -m - bW, y, bW, 23 ), u"→", callback=self.buttonRightCallback)
		self.w.buttonRight.bind("rightarrow", [])
		y += 30
		# ----------------------------------------------------------------------------------------------------
		# / CHOSE MASTER
		#
		mastersList = ["%s" % thisMaster.name for thisMaster in self.thisFont.masters]
		self.w.ChoseMaster = PopUpButton((m, y, -m, 20), mastersList, callback=self.masterSelection) ## **UC** NOT IMPLEMENTED IN SAVE & LOAD
		self.w.ChoseMaster.set( self.masterIndex(self.mID) )
		y += 28
		self.w.line_CM = HorizontalLine((m, y, -m, 1))
		y+= 4
		# ----------------------------------------------------------------------------------------------------
		# / Include other scripts
		#
		if Glyphs.buildNumber >= 911:
			self.w.includeOtherScripts = CheckBox((m, y, -m, 20), self.IOSTitle, callback=self.SavePreferences)
			y += 20
		# ----------------------------------------------------------------------------------------------------
		# / SKIP COMPONENTS
		#
		self.w.skipComponentCheck = CheckBox((m, y, -m, 20), "Skip Components", callback=self.SavePreferences)
		y += 20
		# ----------------------------------------------------------------------------------------------------
		# / SKIP KERNING CLASS MEMBERS
		#
		self.w.skipKGMembersCheck = CheckBox((m, y, -m, 20), "Skip Kerning Group Members", callback=self.SavePreferences)
		y += 24
		# ----------------------------------------------------------------------------------------------------
		# / SKIP KERNING
		#
		self.w.skipKernText = TextBox((m + 17, y, -m, 20), "Skip already kerned pairs:")
		y += 18
		self.w.skipAlreadyKernedLeftCheck = CheckBox((m, y, -m, 20), "Left", callback=self.SavePreferences)
		self.w.skipAlreadyKernedRightCheck = CheckBox((windowWidth * 0.33, y, -m, 20), "Right", callback=self.SavePreferences)
		y += 24
		# ----------------------------------------------------------------------------------------------------
		# / SKIP CATEGORIES
		#
		# y+= 10
		self.w.skipCategoriesText = TextBox((m + 17, y, -m, 20), "Skip Categories:")
		y += 18
		for i, thisCat in enumerate(self.catToSkipUI):
			exec("self.w.skipCategory"+str(i+1)+" = CheckBox( (m, y, -m, 20), '" + thisCat + "', sizeStyle='regular', callback=self.SavePreferences )")
			exec("y += 20")
		y += 4
		self.w.line_SCT = HorizontalLine((m, y, -m, 1))
		# ----------------------------------------------------------------------------------------------------
		# / SPLIT CATEGORIES INTO SEPARATE TABS
		#
		y+= 2
		self.w.separateTabsUI = CheckBox((m, y + 5, -m, 20), "Separate Categories Tabs", callback=self.SavePreferences) # Split Categories into separate Tabs
		# ----------------------------------------------------------------------------------------------------
		# / DEACTIVATE REPORTERS
		#
		y += 20
		self.w.deactivateReporterUI = CheckBox((m, y + 5, -m, 20), "Deactivate Reporter Plugins", callback=self.SavePreferences)
		y += 30
		self.w.line_PS = HorizontalLine((m, y, -m, 1))
		# ----------------------------------------------------------------------------------------------------
		# / SUBMIT BUTTON
		#
		y += 8 # 35
		self.w.make_button = Button((m, y, -m - 30, 20), u"Open Tab", callback=self.submitButtonCallback)  # u"💥🚀⚛" # (m, y, -m, 20)
		self.w.setDefaultButton(self.w.make_button)
		# / HELP BUTTON
		# self.w.helpButton = HelpButton((windowWidth - 30, y, -m, 20), callback=self.helpButtonCallback)
		self.w.helpButton = Button((windowWidth - 35, y, -m, 20), u"...", callback=self.helpButtonCallback)
		# / DRAWER (TOGGLED BY HELP BUTTON)
		self.drawer = Drawer((220, 150), self.w)
		#self.drawer.textBox = TextBox((10, 10, -10, -10), u"Don’t forget:\n%s" % self.specialGuests )
		#self.drawer.openSpecialGuest = Button((10, 10, -10, -10), u"open in Tab")
		self.drawer.specialGuestLabel = TextBox((m+10, 0, -0, 20), u"Don’t forget:\n%s")
		self.drawer.specialGuest =      TextEditor((5, 20, -0, 60), self.specialGuests)

		self.drawer.notesLabel =        TextBox((m+10, 86, -0, 20), "Notes:")
		self.drawer.UINotes =           TextEditor((5, 106, -0, -476), callback=self.SavePreferences)

		self.drawer.doneLabel =         TextBox((m+10, -470, -0, 20), "Done:")
		self.drawer.UIDone =            TextEditor((5, -450, -0, -30), callback=self.SavePreferences)
		# ----------------------------------------------------------------------------------------------------
		# / POINT SIZE
		#
		self.drawer.pointSizeText = TextBox((m+10, -24, -m, 23), "Font Size:")
		self.drawer.pointSize = EditText((m+75, -27, 50, 23), "250", callback=self.SavePreferences)



		if not self.LoadPreferences():
			print "Could not load preferences. Will resort to defaults."

		self.w.resize(windowWidth, 30 + y)
		self.w.makeKey() ### Focus on Window and Button
		self.w.open()
		self.setCheckboxIOS(self.w.glyphInput.get(), self.chosenMasterID)


		#==============================
		# /   G L Y P H   P R E V I E W
		#==============================
		#self.view = preview.GlyphView.alloc().initWithFrame_( ((0, 0), (self.previewSize - self.scrollViewMargin * 2, self.previewSize - self.scrollViewMargin * 2)) )  # visible frame (crops if too small), if too big, the view scrolls
		self.view = preview.GlyphView.alloc().init()
		self.view._layer = self.thisFont.glyphs[self.w.glyphInput.get()].layers[self.mID] # self.thisFont.selectedFontMaster.id
		self.view._upm = self.thisFont.upm # fontUPM
		self.view._scaleFactor = layerScale / (self.thisFont.upm / (2 * 100.0) ) # 0.25 ## UNDER CONSTRUCTION: The bigger the UPM, the smaller the scale result :(
		self.view._margin = self.previewSize / 4
		# self.view._scaleFactor
		self.view.setFrame_( ((0, 0), (self.previewSize - self.scrollViewMargin * 2, self.previewSize - self.scrollViewMargin * 2)) )  # visible frame (crops if too small), if too big, the view scrolls
		self.view.setNeedsDisplay_( True )
		# help(self.view), self.view.bounds(), self.view.setAlphaValue_(0.1)
		try: self.view.setToolTip_(self.w.glyphInput.get())
		except:	pass

		# Scroll View
		#------------
		attrName = "box"
		setattr(self.w, attrName, self.scrollView())

		# print self.w.getPosSize()


	# Belongs to Glyph Preview
	#-------------------------
	def scrollView(self):
		''' Generate vanilla attribute ScrollView'''
		m = 10
		bgColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(.96, .96, .96, 1) # NSColor.yellowColor()
		s = ScrollView((self.scrollViewMargin, self.scrollViewMargin, self.previewSize - self.scrollViewMargin*2, self.previewSize - self.scrollViewMargin*2), # with margins
			self.view,
			hasHorizontalScroller=False,
			hasVerticalScroller=False,
			backgroundColor=bgColor,
			# drawsBackground=False,
			)
		s._nsObject.setBorderType_(NSNoBorder)
		return s


	def helpButtonCallback(self, sender):
		self.Glyphs.defaults["%s.drawer" % self.vID] = not self.Glyphs.defaults["%s.drawer" % self.vID] # Toggle Value and= safePreference
		self.drawer.getNSDrawer().toggle_( self.Glyphs.defaults["%s.drawer" % self.vID] ) # Toggle Drawer
		# self.SavePreferences(sender)


	def masterIndex(self, master):
		''' return the index [0, 1, 2, ...] of the selected master '''
		for mi, master in enumerate(self.thisFont.masters):
			if master.id == self.mID:
				return mi


	def masterSelection(self, sender):
		''' selected Master in the UI PopUpButton '''
		self.chosenMasterID = sender.get()
		self.updateGlyphPreview(self.w.glyphInput.get())
		# self.SavePreferences()


	def updateGlyphPreview(self, glyphName):
		# self.view._layer = self.thisFont.glyphs[glyphName].layers[self.mID] # selected in GlyphsApp Master
		try:
			chosenMaster = self.thisFont.masters[self.chosenMasterID]
			self.view._layer = self.thisFont.glyphs[glyphName].layers[chosenMaster.id] # chosen in UI Master
			# print "updateGlyphPreview"
		except:
			self.view._layer = self.thisFont.glyphs[glyphName].layers[self.mID] # selected Master from GlyphsApp

		## print self.view._layer
		delattr(self.w, "box")
		setattr(self.w, "box", self.scrollView())
		self.view.setToolTip_(glyphName)

		self.setCheckboxIOS(glyphName, self.chosenMasterID)



	def setCheckboxIOS(self, glyphName, masterID):
		if Glyphs.buildNumber >= 911:
			### check if the current glyph is reused at all
			### TODO: trigger the enable() of the UI checkbox to include other script’s occurrences of this glyph
			mid = self.thisFont.masters[masterID].id
			glyphIsReused = self.parent.glyphIsReusedInAnotherScipt(glyphName, mid) # print self.glyphIsReusedAtAll(glyphName, mid)

			if glyphIsReused:
				self.w.includeOtherScripts.enable(1)
				self.w.includeOtherScripts.setTitle( "%s (%s)" % (self.IOSTitle, ", ".join([g for g in glyphIsReused][1:])) )
			else:
				self.w.includeOtherScripts.enable(0)
				self.w.includeOtherScripts.setTitle( self.IOSTitle )

			# print "2:", self.parent.glyphsWithSameKG(glyphName, mid) # *new in 1.9.5* *UC*
			# print "3:", self.parent.sameComponentSetup(glyphName, mid) # *new in 1.9.5* *UC*

		else: pass

	# def glyphIsReusedAtAll(self, glyphName, masterID): # unused function
	# 	isReusedAtAll = None
	# 	isReusedAtAll = len(self.thisFont.glyphsContainingComponentWithName_masterID_(glyphName, masterID))
	# 	if isReusedAtAll > 0:
	# 		return True
	# 	return False



	def SavePreferences( self, sender ):
		try:
			if sender == self.w.glyphInput:
				self.updateGlyphPreview(sender.get())
		except: pass

		try:
			if self.w.glyphInput.get() != "":
				self.Glyphs.defaults["%s.glyphInput" % self.vID] = self.w.glyphInput.get()
			else:
				self.Glyphs.defaults["%s.glyphInput" % self.vID] = self.firstGlyphInFont # allGlyphsInFont[0]
			if Glyphs.buildNumber >= 911:
				self.Glyphs.defaults["%s.includeOtherScripts" % self.vID] = self.w.includeOtherScripts.get()
			self.Glyphs.defaults["%s.skipComponentCheck" % self.vID] = self.w.skipComponentCheck.get()
			self.Glyphs.defaults["%s.skipKGMembersCheck" % self.vID] = self.w.skipKGMembersCheck.get()
			self.Glyphs.defaults["%s.skipAlreadyKernedLeftCheck" % self.vID] = self.w.skipAlreadyKernedLeftCheck.get()
			self.Glyphs.defaults["%s.skipAlreadyKernedRightCheck" % self.vID] = self.w.skipAlreadyKernedRightCheck.get()
			for i, thisCat in enumerate(self.catToSkipUI):
				exec('self.Glyphs.defaults["%s.skipCategory%i"] = self.w.skipCategory%i.get()' % (self.vID, i+1, i+1) ) # self.Glyphs.defaults["com.markfromberg.kernkraft.skipCategory1"] = self.w.skipCategory1.get() # etc.
			self.Glyphs.defaults["%s.pointSize" % self.vID] = self.w.pointSize.get()
			self.Glyphs.defaults["%s.deactivateReporterUI" % self.vID] = self.w.deactivateReporterUI.get()
			self.Glyphs.defaults["%s.separateTabsUI" % self.vID] = self.w.separateTabsUI.get()

			# self.Glyphs.defaults["%s.drawer" % self.vID] = self.drawer.getNSDrawer().isOpen() # Not needed here, will be toggled in helpButtonCallback
			self.Glyphs.defaults["%s.UINotes" % self.vID] = self.drawer.UINotes.get()
			self.Glyphs.defaults["%s.UIDone" % self.vID] = self.drawer.UIDone.get()
		except:
			return False

		return True


	def LoadPreferences( self ):
		try:
			''' MAKE DEFAULTS DICT TO INJECT INTO NSUserDefaults '''
			collectedDefaults = {}
			collectedDefaults["%s.glyphInput" % self.vID] = "a"
			if Glyphs.buildNumber >= 911:
				collectedDefaults["%s.includeOtherScripts" % self.vID] = "True"
			collectedDefaults["%s.skipComponentCheck" % self.vID] = "True"
			collectedDefaults["%s.skipKGMembersCheck" % self.vID] = "True"
			collectedDefaults["%s.skipAlreadyKernedLeftCheck" % self.vID] = "False"
			collectedDefaults["%s.skipAlreadyKernedRightCheck" % self.vID] = "False"
			collectedDefaults["%s.pointSize" % self.vID] = "250"
			collectedDefaults["%s.deactivateReporterUI" % self.vID] = "True"
			collectedDefaults["%s.separateTabsUI" % self.vID] = "False"
			collectedDefaults["%s.UINotes" % self.vID] = "" #"None"
			collectedDefaults["%s.UIDone" % self.vID] = "" #"None"
			collectedDefaults["%s.drawer" % self.vID] = "False"
			for i, thisCat in enumerate(self.catToSkipUI):
				collectedDefaults["%s.skipCategory%s" % (self.vID, str(i+1) ) ] = "False"
			# print collectedDefaults

			NSUserDefaults.standardUserDefaults().registerDefaults_( collectedDefaults )

			''' SET THE UI ELEMENTS WITH VALUES FROM THE PREFERENCES '''
			if self.Glyphs.defaults["%s.glyphInput" % self.vID] in self.allGlyphsInFont:
				self.w.glyphInput.set( self.Glyphs.defaults["%s.glyphInput" % self.vID] )
			else:
				self.w.glyphInput.set( self.firstGlyphInFont ) # allGlyphsInFont[0]
				# Fallback Layer if user switched from one font to another and the stored glyph is not available
			if Glyphs.buildNumber >= 911:
				self.w.includeOtherScripts.set( self.Glyphs.defaults["%s.includeOtherScripts" % self.vID] )
			self.w.skipComponentCheck.set( self.Glyphs.defaults["%s.skipComponentCheck" % self.vID] )
			self.w.skipKGMembersCheck.set( self.Glyphs.defaults["%s.skipKGMembersCheck" % self.vID] )
			self.w.skipAlreadyKernedLeftCheck.set( self.Glyphs.defaults["%s.skipAlreadyKernedLeftCheck" % self.vID] )
			self.w.skipAlreadyKernedRightCheck.set( self.Glyphs.defaults["%s.skipAlreadyKernedRightCheck" % self.vID] )
			for i, thisCat in enumerate(self.catToSkipUI):
				exec('self.w.skipCategory%i.set( self.Glyphs.defaults["%s.skipCategory%s"] )' % (i+1, self.vID, i+1) )
			self.w.pointSize.set( self.Glyphs.defaults["%s.pointSize" % self.vID] )
			self.w.deactivateReporterUI.set( self.Glyphs.defaults["%s.deactivateReporterUI" % self.vID] )
			self.w.separateTabsUI.set( self.Glyphs.defaults["%s.separateTabsUI" % self.vID] )

			if self.Glyphs.defaults["%s.drawer" % self.vID] == True:
				self.drawer.getNSDrawer().open()
			else:
				self.drawer.getNSDrawer().close()
			self.drawer.UINotes.set( self.Glyphs.defaults["%s.UINotes" % self.vID] )
			self.drawer.UIDone.set( self.Glyphs.defaults["%s.UIDone" % self.vID] )
		except:
			print traceback.format_exc()
			return False

		return True


	def categoriesToSkipUI(self):
		''' MAKE A LIST OF SELECTED CATEGORIES '''
		catsToSkipUI = []
		for i, thisCat in enumerate(self.catToSkipUI):
			exec('if self.w.skipCategory%s.get(): catsToSkipUI.append(self.w.skipCategory%s.getTitle())' % ( str(i+1), str(i+1) ) )
		return catsToSkipUI


	def neighbourGlyph(self, direction):
		''' GET THE NEIGHBOUR GLYPH, PREV = -1, NEXT = 1 '''
		currentGlyph = self.w.glyphInput.get()
		if currentGlyph == self.allGlyphsInFont[-1] and direction == 1:  # reset to first glyph when last one reached
			return self.firstGlyphInFont # self.allGlyphsInFont[0]
		if currentGlyph in self.allGlyphsInFont:  # validate current text input, if not input first glyph as fallback
			otherGlyphIndex = self.allGlyphsInFont.index(currentGlyph) + direction
			otherGlyph = self.allGlyphsInFont[otherGlyphIndex]
			return otherGlyph
		else:
			return self.firstGlyphInFont # self.allGlyphsInFont[0]


	def setNeighbourGlyphInEditText(self, direction):
		otherGlyph = self.neighbourGlyph(direction)
		self.w.glyphInput.set(otherGlyph)
		self.Glyphs.defaults["%s.glyphInput" % self.vID] = otherGlyph
		self.updateGlyphPreview(otherGlyph)


	def addGlyphToDoneList(self, glyphName):
		## Add current Glyphs to List [New in 1.9.9]
		# TODO: Check Current Glyph if in this list and notify!
		try:
			currentUIDone = self.drawer.UIDone.get()
			currentUIDone += u"✅ %s\n" % glyphName
			self.drawer.UIDone.set(currentUIDone)
			self.Glyphs.defaults["%s.UIDone" % self.vID] = self.drawer.UIDone.get() # Same as in savePreferences
		except:
			print traceback.format_exc()


	def buttonLeftCallback(self, sender):
		self.setNeighbourGlyphInEditText(-1)  # previous Glyph in Font


	def buttonRightCallback(self, sender):
		self.setNeighbourGlyphInEditText(+1)  # next Glyph in Font


	def submitButtonCallback(self, sender):
		self.parent.skippedCategories = self.categoriesToSkipUI()

		try:
			actualInputGlyphName = self.w.glyphInput.get()

			self.addGlyphToDoneList(actualInputGlyphName)

			self.parent.generateTabOutput(actualInputGlyphName) # first main run
			if Glyphs.buildNumber >= 911:
				if self.w.includeOtherScripts.get() == 1:
					# if there are more glyphs like the input glyph in other scripts:
					while len( self.parent.showAllScripts ) > 0:
						self.parent.generateTabOutput(self.parent.showAllScripts[0], showLetterCategoryOnly=True)

						# A
						self.parent.showAllScripts.pop(0) # remove the currently set input script
						# B
						# try:
						# 	self.parent.showAllScripts.pop(0) # remove the currently set input script
						# except: pass

		except:
			print traceback.format_exc()

		self.w.close()

		if self.w.deactivateReporterUI.get():
			self.parent.deactivateReporters()

		for error in self.parent.errorCollector:
			print error


#KernKraft()
