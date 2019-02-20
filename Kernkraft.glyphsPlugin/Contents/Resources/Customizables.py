## 
##	Customizable Data for the Kernkraft Script
##	written by Mark Froemberg ( markfroemberg.com )
##	@Mark2Mark
##	at Carrois Apostrophe ( www.carrois.com )
##
##	+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##	First entry is a list of 2 items: Category and its SubCategory
##		These will be excluded from the kerning output by default.
##	Second entry is a dictionary with the uneditable(!) key `Exceptions` that takes a (empty) list of all exceptions.
##		These `exceptions` will be passed through even if the subcategory is filtered out.
##
##	+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



excludedSubCategories = [
	[ [ "Letter", "Ligature" ],		{ "Exceptions" : [] } ],
	[ [ "Letter", "Smallcaps" ],	{ "Exceptions" : [] } ],
	[ [ "Letter", "Superscript" ],	{ "Exceptions" : [] } ],

	[ [ "Number", "Other" ],		{ "Exceptions" : [
													"zeroinferior",
													"oneinferior",
													"twoinferior",
													"threeinferior",
													"fourinferior",
													"fiveinferior",
													"sixinferior",
													"seveninferior",
													"eightinferior",
													"nineinferior",
												 	]} ],

	[ [ "Symbol", "Arrow" ],		{ "Exceptions" : [] } ],
	[ [ "Symbol", "Geometry" ],		{ "Exceptions" : [] } ],
	[ [ "Symbol", "Other" ],		{ "Exceptions" : [
													"ampersand",
												  	"at",
												  	"trademark",
												 	"lozenge",
													"paragraph",
													"section",
													"registered",
													"degree",
													"bar",
													"brokenbar",
													"dagger",
													"daggerdbl",
													"numero",
													"estimated",
												 	]} ],
]
