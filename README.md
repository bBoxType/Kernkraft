![Kernkraft](https://raw.githubusercontent.com/carrois/Kernkraft/master/Kernkraft%2001.png "Kernkraft")
![Kernschmelze](https://raw.githubusercontent.com/carrois/Kernkraft/master/Kernschmelze%2001.png "Kernschmelze")

## Kernkraft:
This is a set of scripts (»Kernkraft« & »Kernschmelze«) for the Font Editor Glyphs. It might help you to be easily confronted with all the neccessary pairs your Font provides (no matter how extended the character set is).

Based on the way of kerning by Carrois’ (carrois.com). Code written by Mark Frömberg (@Mark2Mark). Please contact me for any issues or ideas.

## Features:

### Scripts supported so far:
- Latin
- Cyrillic
- Greek
- Hebrew *Under Construction*

### Filters:
- Different Scripts are not shown side by side. (Latin keeps Latin, Cyrillic keeps Cyrillic, ...).
- Skip SubCategories (customizable list with Exceptions).
- Exclude `SC` when the inputGlyph is `LC`
(e.g. `nnona/a.sc annoi` does not make sense, does it?)
- Exclude `.tf` & `.tosf`. They are not to be kerned.
- When Input = `SC`: Output -->
	a) `HHOHA/a.sc/h.sc/o.sc/o.sc/i.sc`
		for iteratedGlyph = `UC`
	b) `/h.sc/h.sc/o.sc/h.sc/a.sc/a.sc/a.sc/h.sc/o.sc/o.sc/i.sc`
		for iteratedGlyph = `SC`
- Skip Kerning Group Members (UI-Option)
	--> a) skip members of the input glyph’s group, because they will follow the kerning anyway.
	--> b) skip members of any already displayed glyph’s group, too.
	– Currently only for glyphs that share the same groups left *and* right.

### Functions in new Tab(s):
- Set point size (UI-option)
- Set caret in optimal position (currently at the bottom)
- Open Preview Panel (default size)
- Set Text Tool
- Hebrew inputGlyph triggers RTL writing direction
	*under construction: Does it need to switch the kerning sides as well (?!)*

### User Interface:
- GlyphPreview (best scale @ 1000 UPM):
	Components = Gray, Non-Exported = Orange
- Display Kerning Groups and Auto-Width-Glyphs
- Cycling through glyphs via Buttons or Cursor Keys
- Master Selection
- Skip Components
- Skip Kerning Group Members
- Skip already kerned Pairs (L and/or R)
- Skip Categories
- Separate Categories Tabs
- Deactivate Reporter Plugins (speed up Glyphsapp)
- Font Size
- Drawer with user-reminder for special Guests and Notepad
- Fallback for Glyph Input when Glyph not in Font
- Saved Settings (with Fallback for Glyph Input)

### Error handling:
- validate input glyph for being part of the font

- - - 
## Changelog

### 1.8
- Rebuild modules to make compilable package
- Tried to use Georgs GlyphView, works, but cannot customize, back to my own GlyphPreview
- Added Tooltip: Glyphname of displayed Layer
- Added `Auto-Width` Label to UI (when glyph’s width is automatically set)
- Added Special Guests*** to Drawer (as a user-reminder for now)
- Added Notes to Drawer
- Changed skipping ".tf" and ".tosf" to not check if it is at the end of glyphname, but *in* glyphname at all
- Fixed display of SC-to-SC right after UC-to-SC if input = SC
- Tried to implement better flank-rewrite function to adapt input glyph .suffix **NOT READY YET (see `KernKraftModule-OFF-Branch (tryouts from 1.8).py`)**

### 1.7
- Tried to add SubCategories to the UI. Decided to ditch them there: UI-Overkill
- Instead:
 	customizable list: `excludedSubCategories` with Exceptions.
- Exclude Kerning Class Members:
	- A) The group members from the UI-Input Glyph
	- B) The iterated Glyph when both it’s KG appeared already once in the Tab
- Added All-Component highlight to GlyphPreview
- Added UI Option to spread Categories into separate Tabs

### 1.6
- Rewritten the behaviour of skipped Kernings:
	-> dont skip the whole line if one side applies, instead just skip the to-be-kerned-glyph on the to-skip-side *under construction: Check bulletproofnes*
- Ligatures dont catch `LC`-rightTail; solution:
	- SubCategory `ligature` (eg. ff, f_f, T_h, ...)
	-> if last part of liga `.islower()`: trigger being `LC`
- Set Text Tool in Tab
- Added Small Caps behaviour
- Skip numbers with different syntax **(still needs to be tested)**	
	- works for inputGlyphs: `.lf`, `.dnom`, `.numr`
	- skips non-matches, changes kerningTails @ matches
- No empty category label anymore at EOL in Tab
- Switch off reporter Plugins as UIoption
- Added Master Selection to UI. Does not save and load preferences, but initializes the PopupButton with the currently active master


- - - 
## TODO

### Important

- Check `.fina`, `.init`, `.swsh`, etc (!)
- Case: `zero.lf.sc` --> `nn0nn`, supposed case: --> `000000` (+ w/ same suffix(es))
- `one.sc` and alike --> put between `zero.sc` flanks
- not too sure about simply copying UC kerning to SC:
	`/V/A/` versus `/v.sc/a.sc` or `/V/asterisk` versus `/v.sc/asterisk` often need different kerning!
- What about these SPECIAL GUESTS***: ??
> `Ąj Ą_ Ą) Ęj Ę_ Ę) Įj Į_ Į) fï Tï Fï *ï* ‘ï‘ Ł⁰ Ł‘ ß‘ ß⁰
> ¿j ¿y ¿g c//o`
> --> /trademark is passed through [a/™  c/™  e/™  f/™  g/™  i/™  k/™  l/™  o/™  r/™  s/™  t/™  v/™  w/™  x/™  y/™  z/™]
> (along with /ampersand and /at) in `excludedSubCategories`
> --> BUT Do we need an extra invitation for these guys?

- Keep an eye on `excludedSubCategories` list and its Exceptions.
	- exclude `Private Use` as well?
- Filter input=Letter better, e.g.:
	- Currencies between Letters? `HHOHa/yen.osf annoi` etc
	- Math Symbols between Letters? `HHOHa¬annoi`, `HHOHa%annoi` etc
	- `.osf` comes along in letters: `HHOHa/percent.osf annoi` etc [FIRA]
- General Question: How to deal with Multiple Masters?
	+ Remind the user in using only the heavies master (eg. little indicator in Master-PopupButton or GlyphView)
(- What if kerning is not consistent among masters?!?!
	- a) maybe add another tab with critical pairs?
	- b) or add checkbox at the kerning Q; sth like `check all masters`?
	  if this attempt, better:
		- b1) skip only when all masters have any kerning? Or: (prefered, I think)
		- b2) skip only when any master has any kerning?
	- Script to keep them in sync (num of pairs), or even make possible in Glyphsapp by default to apply kerning to all masters?
	- Check »Kernschmelze« for most of these needs.
	)
~~- Remove version b) from the SC Output (see features > switches)
	Message: `use script: Copy Caps Kerning to Small Caps Kerning instead.`~~
- handle `SC` when iteratedGlyph is `SC` (currently it gets between `UC`)
- add to `SC` handling in StringMaker()`:
	currently:	`/h.sc/h.sc/o.sc/h.sc/a.sc ﬁ/a.sc/h.sc/o.sc/o.sc/i.sc`
	needed:  	No Liga (?)
- Number-Skipping/changing also with `[number]superior` & `[number]inferior` ?
- Skip fractions with inputGlyph=letter (maybe even in general except with `number`) --> currently: `HHOHa⁄annoi` `HHOHa⅟annoi` `HHOHa⅔annoi` etc
- What if inputGlyph is e.g. `/backslash` and currently also Hebrew letters are used as iteratedGlyph? In this case we get no RTL!
- Set focus on first/last line in Tab (UIOption)
- Check (and/or change) the definition of the skipped components (!)
	needs to be bullet proof, especially with Cyrillic or Greek

### Nice to have
- Improve Performance by taking everything out of the loops that can be set once [see `categoriesToSkipUI()``]
- Add `Skip Non-Exporting Glyphs`
- Noob-Mode (CheckBox): If checked: Messages as Tutorials
- if `SC` in input, inform about the copy `UC` to `SC` script (*** Not too sure about that copying!)
- if `germandbl` or `germandbl(UC)` follows a `UC` consonant: `continue`
- If multiple tabs for different categories:
	- add Buttons to cycle through tabs
	`Glyphs.currentDocument.windowController().showNextTab_(True) # and (showPreviousTab_)`
- TotenkopfModus: "inno#*#*nnoi" (* = inputGlyph, # = iteratedGlyph)
	(default behaviour switched off where the comment says: "### = Exclude `TotenkopfModus`")


- - - 
### Notes

- NB: All glyphname checks might be checked against part of glyphname (eg. ampersand, ampersand.ss01, etc) -->
- Everything, but especially "SkipComponents" and "Skip Kernig" are of course Master-connected elements.

