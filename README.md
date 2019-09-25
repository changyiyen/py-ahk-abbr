# py-ahk-abbr - Abbreviation expansion using AutoHotkey hotstrings in Python 3

## Overview

[AutoHotkey](https://www.autohotkey.com) is a very powerful automation tool for Windows, implementing its own programming language and capable of doing (among many other things) text substitution, e.g., changing abbreviations to full text. Sadly it has not (yet) been ported to Unix-like platforms, and recent versions don't seem to work when run on Wine. AutoKey is a nice tool that can do text substitution, but unfortunately the user has to (manually) create a file for every abbreviation that's needed, instead of having all the entries in a single file like AutoHotkey's hotstrings. This script is a rough attempt at implementing a subset of AutoHotkey's hotstring expansion using Python 3.

## Dependencies

All files were written for Python 3.6+. Currently the core of this script depends on [pynput](https://pynput.readthedocs.io/en/latest/) for keyboard listening and typing. It can be installed with Pip3, e.g.:

```shell
pip3 install pynput
```

## Running the script

Open a terminal window and start the script:

```shell
python3 abbr.py
```

The script will run in this window and print debug messages (as stated, this is a rough attempt), including the current internal text buffer contents and buffer length. The hotstring file is currently hard-coded as 'hotstring.txt', containing AutoHotkey-style hotstrings. _However, do note that only a subset of the hotstring format has been implemented; options, context and all that jazz have not been implemented (yet)._ Start typing in any other window and type your abbreviation of choice. Whenever an end character is typed immediately afterwards (see the source for details on which characters are considered end characters, but note that the end character list is modelled after AutoHotkey's), a sequence of backspaces are automatically typed out, followed by the full text. Press Escape any time to quit the script.

## Known bugs

While this script works on simple text editors (e.g., Mousepad), things can get odd when typing text into certain programs, such as Firefox's Omnibar (the text deletion can be off by several characters). Also, this script doesn't work for most CJK input methods (e.g. Chewing or Anthy), since pynput listens for the raw keycodes.

## License

py-ahk-abbr is placed under the coffeeware license, itself a lightly modified beerware license.
