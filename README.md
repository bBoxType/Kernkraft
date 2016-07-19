<img src="https://raw.githubusercontent.com/carrois/Kernkraft/master/Kernkraft%2001.png" height="900">

### About:

#### »Kernkraft«
»Kernkraft« is a tool that might help you to be easily confronted with all the neccessary pairs your Font provides (no matter how extended the character set is).

#### »Kernschmelze«
»Kernschmelze« is a tool that will help you interpolate the kerning (given a glyphs file with at least 2 masters). It uses the weight value to calculate, no further axes (e.g. width) are currently supported.

This set of plugins for the font editor »Glyphs« is based on the way of kerning by [Carrois Apostrophe](https://www.carrois.com). The code is written by [Mark Frömberg](http://www.markfromberg.com) (@Mark2Mark). Please contact me for any issues or ideas.

##
### Features:

#### Scripts supported so far:
- Latin
- Cyrillic
- Greek
- Hebrew *Under Construction*

#### Filters:
- Skip categories (UI-Option)
- Skip SubCategories (customizable list with Exceptions)
- Exclude `SC` when the inputGlyph is `LC`
(e.g. `nnona/a.sc annoi` does not make sense, does it?)
- Exclude `.tf` & `.tosf`
- when Input = `SC`: Output -->
	a) `HHOHA/a.sc/h.sc/o.sc/o.sc/i.sc`
		for iteratedGlyph = `UC`
	b) `/h.sc/h.sc/o.sc/h.sc/a.sc/a.sc/a.sc/h.sc/o.sc/o.sc/i.sc`
		for iteratedGlyph = `SC`
- Skip Kerning Group Members (UI-Option) (2-way)

#### Functions in new Tab(s):
- Set point size (UI-option)
- Set caret in optimal position (currently at the bottom)
- Open Preview Panel (default size)
- Set Text Tool
- Hebrew inputGlyph triggers RTL writing direction
	*under construction: Does it need to switch the kerning sides as well (?!)*

#### User Interface:
- GlyphPreview (best scale @ 1000 UPM):
	Only-Components = Gray, Non-Exported = Orange
- Display Kerning Groups
- Cycling through glyphs via Buttons or Cursor Keys
- Saved Settings with Fallback for Glyph Input
- Fallback for Glyph Input when Glyph not in Font
- Master Selection
- Deactivate Reporter Plugins (speed up Glyphsapp)
- Drawer with user-reminder for special Guests and Notepad

#### Error handling:
- validate input glyph for being part of the font

##### More: see changelog!


##
### Changelog:

#### 1.8
- rebuild modules to make compilable package
- tried to use Georgs GlyphView, works, but cannot customize, back to my own GlyphPreview
- Added Tooltip: Glyphname of displayed Layer
- Added `Auto-Width` Label to UI (when Glyph’s width is automatically set)
- Added Special Guests*** to Drawer (as a user-reminder for now)
- Added Notes to Drawer
- changed skipping ".tf" and ".tosf" to not check if it is at the end of glyphname, but *in* glyphname at all
- fixed display of SC-to-SC right after UC-to-SC if input = SC
- tried to implement better flank-rewrite function to adapt input glyph .suffix **NOT READY YET (see `KernKraftModule-OFF-Branch (tryouts from 1.8).py`)**

#### 1.7
- tried to add SubCategories to the UI. Decided to ditch them there: UI-Overkill
- Instead:
 	customizable list: `excludedSubCategories` with Exceptions.
- Exclude Kerning Class Members:
	- A) The group members from the UI-Input Glyph
	- B) The iterated Glyph when both it’s KG appeared already once in the Tab
- Added All-Component highlight to GlyphPreview
- Added UI Option to spread Categories into separate Tabs

#### 1.6
- Rewritten the behaviour of skipped Kernings:
	-> dont skip the whole line if one side applies, instead just skip the to-be-kerned-glyph on the to-skip-side *under construction: Check functionality*
- Ligatures dont catch `LC`-rightTail; solution:
	- SubCategory `ligature` (eg. ff, f_f, T_h, ...)
	-> if last part of liga `.islower()`: trigger being `LC`
- Set Text Tool in Tab
- Added Small Caps behaviour
- Skip numbers with different syntax **(still needs to be tested)**	
	- works for inputGlyphs: `.lf`, `.dnom`, `.numr`
	- skips non-matches, changes kerningTails @ matches
- No empty category label anymore at EOL in Tab
- switch off reporter Plugins as UIoption
- Added Master Selection to UI. Does not save and load preferences, but initializes the PopupButton with the currently active master


##
### ToDo:

#### Important

- check `.fina`, `.init`, `.swsh`, etc (!)
- case: `zero.lf.sc` --> `nn0nn`, supposed case: --> `000000` (+ w/ same suffix(es))
- `one.sc` etc. --> put between `zero.sc` flanks
- not too sure about simply copying `UC` kerning to `SC`:
	e.g. `/V/A/` vs. `/v.sc/a.sc` or `/V/asterisk/v.sc/asterisk` often need different kerning
- What about these SPECIAL GUESTS *?:

> `Ąj Ą_ Ą) Ęj Ę_ Ę) Įj Į_ Į) fï Tï Fï *ï* ‘ï‘ Ł⁰ Ł‘ ß‘ ß⁰
> + ¿j ¿y ¿g c//o`
> 
> --> /™ is passed through [a/™  c/™  e/™  f/™  g/™  i/™  k/™  l/™  o/™  r/™  s/™  t/™  v/™  w/™  x/™  y/™  z/™]
> (along with /ampersand and /at) in `excludedSubCategories`
> --> BUT Do we need an extra invitation for these guys?

- keep an eye on `excludedSubCategories` list and its Exceptions.
	- exclude `Private Use` as well?
- Better filtering for input=Letter, e.g.:
	- Currencies between Letters? `HHOHa/yen.osf annoi` etc
	- Math Symbols between Letters? `HHOHa¬annoi`, `HHOHa%annoi` etc
	- `.osf` comes along in letters: `HHOHa/percent.osf annoi` etc [see Fira]
- ~~How to deal with different kerning in different masters (mid-process)?~~
	- ~~a) maybe add another tab with critical pairs?~~
	- ~~b) or add checkbox at the kerning Q; sth like `check all masters`?~~
	  ~~if this attempt, better:~~
		- ~~b1) skip only when all masters have any kerning? Or: (prefered, I think)~~
		- ~~b2) skip only when any master has any kerning?~~
- check handling `SC` when iteratedGlyph is `SC` (currently it gets between `UC`)
- add to `SC` handling in `StringMaker()`:
	currently:	`/h.sc/h.sc/o.sc/h.sc/a.sc ﬁ/a.sc/h.sc/o.sc/o.sc/i.sc`
	needed:  	No Liga (?)
- Number-Skipping/changing also with `[number]superior` & `[number]inferior` ?
- Skip fractions with `inputGlyph=letter` (maybe even in general except with `number`) --> currently: `HHOHa⁄annoi` `HHOHa⅟annoi` `HHOHa⅔annoi` etc
- What if inputGlyph is e.g. `/backslash` and currently also Hebrew letters are used as iteratedGlyph? In this case we get no RTL!
- Set focus on first/last line in Tab (UIOption)
- Check (and/or change) the definition of the skipped components (!) needs to be bullet proof.
- In RTL mode: write the Category Labels backwards.

#### Nice to have
- Improve Performance by taking everything out of the loops that can be set once [see `categoriesToSkipUI()`]
- Add `Skip Non-Exporting Glyphs`
- Noob-Mode (CheckBox): If checked: Messages as Tutorials
- if `germandbl` or `germandbl(UC)` follows a `UC` consonant: `continue`
- If multiple tabs for different categories:
	- add Buttons to cycle through tabs
	`Glyphs.currentDocument.windowController().showNextTab_(True) # and (showPreviousTab_)`

##
### Notes:

- NB: All glyphname checks might be checked against part of glyphname (eg. ampersand, ampersand.ss01, etc) -->
- Keep in mind: Everything, but especially "SkipComponents" and "Skip Kernig" are Master-connected elements.

