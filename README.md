# py-ahk-abbr - Abbreviation expansion using AutoHotkey hotstrings in Python 3

## Overview

[AutoHotkey](https://www.autohotkey.com) is a very powerful automation tool for Windows, implementing its own programming language and capable of doing (among many other things) text substitution, e.g., changing abbreviations to full text. Sadly it has not (yet) been ported to Unix-like platforms, and recent versions don't seem to work when run on Wine. AutoKey is a nice tool that can do text substitution, but unfortunately the user has to (manually) create a file for every abbreviation that's needed, instead of having all the entries in a single file like AutoHotkey's hotstrings. This script is a rough attempt at implementing a subset of AutoHotkey's hotstring expansion using Python 3.

## Dependencies

All files were written for Python 3.6+. Currently the core of this script depends on [pynput](https://pynput.readthedocs.io/en/latest/) for keyboard listening and typing, as well as Xlib for low-level X event manipulation. These can be installed with Pip3, e.g.:

```shell
pip3 install pynput
pip3 install Xlib
```

## Running the script

Open a terminal window and start the script:

```shell
python3 abbr.py
```

The script will run in this window and print debug messages (as stated, this is a rough attempt), including the current internal text buffer contents and buffer length. The hotstring file is currently hard-coded as 'hotstring.txt', containing AutoHotkey-style hotstrings. _However, do note that only a subset of the hotstring format has been implemented; options, context and all that jazz have not been implemented (yet)._ Start typing in any other window and type your abbreviation of choice. Whenever an end character is typed immediately afterwards (see the source for details on which characters are considered end characters, but note that the end character list is modelled after AutoHotkey's), a sequence of backspaces are automatically typed out, followed by the full text. Press Escape any time to quit the script.

This script has been tested to run on Python 3.6.8 + Xubuntu 18.04 and Python 3.6.9 + FreeBSD 12.0-RELEASE-p10.

## Known bugs

* While this script works on simple text editors (e.g., Mousepad), things can get odd when typing text into certain programs, such as Firefox's Omnibar (the text deletion can be off by several characters).

* This script doesn't work for most CJK input methods (e.g. Chewing or Anthy), since pynput listens for the raw keycodes. (But then, so doesn't AutoHotkey...)

* The default behavior of this program is to type back the ending character that triggered the replacement. However, some ending characters (like the curly braces and the colon) need to have the shift key held down as they're being typed. As a result, if the shift key is _not_ held down as the ending character is being typed back, the wrong ending character may be typed out (e.g., the curly braces will be changed into square brackets on most keyboards). Workaround (short of adding special logic to these particular ending characters) is to simply hold the shift key down until the full text replacement is typed out.

## License

py-ahk-abbr is placed under the coffeeware license, itself a lightly modified beerware license.
