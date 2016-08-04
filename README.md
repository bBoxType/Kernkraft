<img src="https://raw.githubusercontent.com/carrois/Kernkraft/master/Kernkraft%2001.png" height="900">

### About:

#### »Kernkraft«
»Kernkraft« is a tool that might help you to be easily confronted with all the neccessary pairs your Font provides (no matter how extended the character set is). If you want to kern the glyph `k`, without any filtering checkboxes but `Skip Components` checked, you will get a tab with a bunch of stings like:
```
__Letter:
HHOHAknnoi
HHOHÆknnoi
HHOHBknnoi
HHOHCknnoi
HHOHDknnoi
...
HHOHkaknnoi
HHOHkæknnoi
HHOHkbknnoi
HHOHkcknnoi
HHOHkdknnoi
...
__Punctuation:
HHOHk*knnoi
HHOHk\knnoi
HHOHk·knnoi
HHOHk•knnoi
HHOHk:knnoi
HHOHk,knnoi
HHOHk…knnoi
HHOHk!knnoi
HHOHk¡knnoi
HHOHk#knnoi
...
__Symbol:
HHOHk¢knnoi
HHOHk$knnoi
HHOHk€knnoi
HHOHk£knnoi
HHOHk¥knnoi
...
```
And so on. The presentation of kerning strings depends on the Font’s character set. No predefined lists are used, as they would cause the overlooking of glyph pairs.

Navigate through your glyphset with your keyboard: ←,  → and hit enter ⏎ to open the new tab(s).

Putting the caret to the right hand side of the to-be-kerned-glyph (in this example `k` --> `HHOHk|aknnoi`) allows you to kern both sides (`ka` and `ak`) with the Glyphs kerning shortcuts `ctrl + opt + ←/→` for left and `cmd + opt + ←/→` for right . Hold `shift` for 10 units increments.Then just use the up or down keys to dedicate yourself to the next kerning pair.

The checkboxes help you to increase the speed of your workflow. In the very beginning it could be useful to have `Skip already kerned pairs` unchecked. `Skip Components` and `Skip Kerning Group Members`could be checked in most cases. This means, that you are not confronted with duplicates of an already kerned pair (e.g. KA, KÄ, …). In case you want to see them anyway, uncheck these boxes.

The other settings are hopefully self explanatory. Let me know if you got any questions.

#### »Kernschmelze«
»Kernschmelze« is a tool that will help you interpolate the kerning (given a glyphs file with at least 2 masters). It uses the weight value to calculate, no further axes (e.g. width) are currently supported.

This set of plugins for the font editor »Glyphs« is based on the way of kerning by [Carrois Apostrophe](https://www.carrois.com). The code is written by [Mark Frömberg](http://www.markfromberg.com) (@Mark2Mark). Please contact me for any issues or ideas.

##
### Features:

#### Scripts supported so far:
- Latin
- Cyrillic
- Greek
- Hebrew *(Under Construction)*

#### Filters:
- Include Other Scripts
	E.g. when you deal with /A and it is also used in Greek and/or Cyrillic as /Alpha and /A-cy, you can see these in one go.
- Skip categories (UI-Option)
	Check the categories that you don’t want to see in the new tab.
- Skip SubCategories (Hardcoded)
	There is a customizable list with exceptions.
- Exclude `.tf` & `.tosf`
- When Input = `LC`: Exclude `SC
	(e.g. `nnona/a.sc annoi` does not make sense, does it?)
- When Input = `SC`: Output -->
	- a) `HHOHA/a.sc/h.sc/o.sc/o.sc/i.sc` for iteratedGlyph = `UC`
	- b) `/h.sc/h.sc/o.sc/h.sc/a.sc/a.sc/a.sc/h.sc/o.sc/o.sc/i.sc` for iteratedGlyph = `SC`
- Skip Kerning Group Members (UI-Option) (2-way)

#### Functions in new Tab(s):
- Set point size (UI-option)
- Set caret in optimal position (currently at the bottom)
- Open Preview Panel (default size)
- Set Text Tool
- Hebrew inputGlyph triggers RTL writing direction
	*under construction: Does it need to switch the kerning sides as well (?!), also the labels need to be written backwards.*

#### User Interface:
- GlyphPreview (best scale @ 1000 UPM):
	Only-Components = Gray, Non-Exported = Orange
- Display Kerning Groups in blue
- Cycling through glyphs via Buttons or Cursor Keys
- Fallback for Glyph Input when Glyph not in Font
- Master Selection
- Deactivate Reporter Plugins (speed up Glyphsapp)
- Drawer with user-reminder for special Guests and Notepad
- Save Settings and Notes

#### Error handling:
- validate input glyph for being part of the font

##### More: see changelog!


##
### Changelog:
##### 1.9.3
- Add `Private Use` to the UI as an option to skip.

##### 1.9.2
- New Function: Include all occurrences of the Input Glyph in other scripts (Option in UI); (Showing only the Category `Letter`)

#### 1.9
- Use Glyph with KG-Name if given (instead of the first KG Member) [if both sides’ KG are the same]; example: `HHOHAƔAHOOI` will display `HHOHAYAHOOI` now if `/Ɣ` got `Y` as KG left & right. Very useful especially with very large character sets. *(Note: this function and its position in the algorithm chain is experimental, please report any issues)* — ([1.9.1] Only applies if `Skip Group Members` and `Skip Components` are active in the UI.)

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
- Exclude Kerning Group (»KG«) Members:
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
- ~~check handling `SC` when iteratedGlyph is `SC` (currently it gets between `UC`)~~
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

