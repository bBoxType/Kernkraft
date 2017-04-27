class KerningStrings:
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# CUSTOMIZABLE DATABASE
	customKenringStrings = {
		
	## STRUCTURE:
	## [`script`]
	## 		[`category`]
	##			[`subCategory`]
	##				[*side-of-kerning-pair*]
		
		"latin" : {
			"Letter" : {
				"Uppercase" : {
					"Left" : "/H/H/O/H",
					"Right" : "/H/O/O/I",
					},
				"Lowercase" : {
					"Left" : "/n/n/o/n",
					"Right" : "/n/n/o/i",
					},
				"Smallcaps" : {
					"Left" : "/h.sc/h.sc/o.sc/h.sc",
					"Right" : "/h.sc/o.sc/o.sc/i.sc",
					},
				},
			},
		"cyrillic" : {
			"Letter" : {
				"Uppercase" : {
					"Left" : "/En-cy/En-cy/O-cy/En-cy",
					"Right" : "/En-cy/O-cy/O-cy/Ge-cy",
					},
				"Lowercase" : {
					"Left" : "/en-cy/en-cy/o-cy/ii-cy",
					"Right" : "/en-cy/en-cy/o-cy/ge-cy",
					},
				"Smallcaps" : {
					"Left" : "/en-cy.sc/en-cy.sc/o.sc/en-cy.sc",
					"Right" : "/en-cy.sc/o-cy.sc/o-cy.sc/i.sc",
					},
				},
			},
		"greek" : {
			"Letter" : {
				"Uppercase" : {
					"Left" : "/Eta/Eta/Omicron/Eta",
					"Right" : "/Eta/Omicron/Omicron/Iota",
					},
				"Lowercase" : {
					"Left" : "/eta/omicron/omicron/eta",
					"Right" : "/eta/omicron/omicron/iota",
					},
				"Smallcaps" : {
					"Left" : "/eta.sc/eta.sc/omicron.sc/eta.sc",
					"Right" : "/eta.sc/omicron.sc/omicron.sc/iota.sc",
					},
				},
			},
		"thai" : {
			"Letter" : {
				"Other" : {
					"Left" : "/thoThahan-thai/thoThahan-thai/doDek-thai/thoThahan-thai",
					"Right" : "/thoThahan-thai/doDek-thai/doDek-thai/noNu-thai",
					},
				},
			},
		"hebrew" : {
			"Letter" : {
				"Other" : {
					"Left" : "/he-hb/samekh-hb/he-hb/vav-hb/he-hb",
					"Right" : "/he-hb/samekh-hb/he-hb/he-hb",
					},
				# "Smallcaps" : {
				# 	"Left" : "/eta.sc/eta.sc/omicron.sc/eta.sc",
				# 	"Right" : "/eta.sc/omicron.sc/omicron.sc/iota.sc",
				# 	},
				},
			},		

		## Bypass not defined or not found scripts (e.g. "Number" is a category but not a script (= None))
		None : {
			"Number" : {
				"Decimal Digit" : {
					"Left" : "/zero/zero/zero/zero",
					"Right" : "/zero/zero/zero/zero",
					},
				"Fraction" : {
					"Left" : "/zero/zero/zero/zero",
					"Right" : "/zero/zero/zero/zero",
					},
				"Smallcaps" : {									###
					"Left" : "/zero/zero/zero/zero",			###
					"Right" : "/zero/zero/zero/zero",			### *added in 1.8*
					},											###
				},				
			"Punctuation" : {
				"Other" : {
					"Left" : "/n/n/o/n",
					"Right" : "/H/n/o/i", # "/N/n/o/i",
					},
				},
			"Symbol" : { # **UC**
				"Other" : {
					"Left" : "/n/n/o/n",
					"Right" : "/H/n/o/i", # "/N/n/o/i",
					},
				},

			},	

	}
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
