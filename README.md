# py-ahk-abbr - Abbreviation expansion using AutoHotkey hotstrings in Python 3

## Overview

[AutoHotkey](https://www.autohotkey.com) is a very powerful automation tool for Windows, implementing its own programming language and capable of doing (among many other things) text substitution, e.g., changing abbreviations to full text. Sadly it has not (yet) been ported to Unix-like platforms, and recent versions don't seem to work when run on [Wine](https://www.winehq.org). [AutoKey](https://github.com/autokey/autokey) is a nice tool that can do text substitution, but unfortunately the user has to (manually) create a file for every abbreviation that's needed, instead of having all the entries in a single file like AutoHotkey's hotstrings. This script is a rough attempt at implementing a subset of AutoHotkey's hotstring expansion using Python 3.

## Dependencies

All files were written for Python 3.6+. Currently the core of this script depends on [pynput](https://pynput.readthedocs.io/en/latest/) for keyboard listening and typing, as well as [Xlib](https://pypi.org/project/python-xlib/) for low-level X event manipulation. These can be installed with Pip3, e.g.:

```shell
pip3 install pynput
pip3 install Xlib
```

## Running the script

Open a terminal window and start the script:

```shell
python3 abbr.py -d
```

The script will run in this window and print debug messages (as stated, this is a rough attempt), including the current internal text buffer contents and buffer length. The hotstring file defaults to 'hotstrings.ahk', which is supposed to be a file containing AutoHotkey-style hotstrings. _However, do note that only a subset of the hotstring format has been implemented; options, directives and all that jazz have only been been partially implemented._ Start typing in any other window and type your abbreviation of choice. Whenever an end character is typed immediately afterwards (see the source for details on which characters are considered end characters, but note that the end character list is modelled after AutoHotkey's), a sequence of backspaces are automatically typed out, followed by the full text. (This behavior can be modified at runtime by using hotstring-specific options). Press Escape any time to quit the script.

This script has been tested to run on:

* Python 3.6.8 - 3.6.9 + Xubuntu 18.04

* Python 3.6.9 + FreeBSD 12.0-RELEASE-p10

## Known bugs

* While this script works on simple text editors (e.g., Mousepad), things can get odd when typing text into certain programs, such as Firefox's Omnibar (the text deletion can be off by several characters).

* This script doesn't work (elegantly) for input methods that require character selection (most notably CJK input methods, e.g. Chewing or Anthy), since pynput listens for the raw keycodes, and there's probably no easy way of reading their buffers. (But then, so doesn't AutoHotkey or Autokey...)

* The default behavior of this program is to type back the ending character that triggered the replacement. However, some ending characters (like the curly braces and the colon) need to have the shift key held down as they're being typed. As a result, if the shift key is _not_ held down as the ending character is being typed back, the wrong ending character may be typed out (e.g., the curly braces will be changed into square brackets on most keyboards). ~~Workaround (short of adding special logic to these particular ending characters) is to simply hold the shift key down until the full text replacement is typed out.~~ _2020-12-09 Edit: fixed using extra logic for these ending characters (shift key is held down before typing); however, this fix probably only works for particular keyboard layouts, like the generic 108-key English keyboard I'm using. This will probably fail in cases where these ending characters do not need a shift key to type, in which case you can remove that key from the "triggers_needing_shift" list._

## License

py-ahk-abbr is placed under the coffeeware license, itself a lightly modified beerware license.
