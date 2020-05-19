#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# abbr.py - Abbreviation expansion in the spirit of AutoHotkey
# Author: Chang-Yi Yen <changyiyen gmail com>
# License: coffeeware
# Version 0.1.2 (2020-05-19)

# Version history
# 0.1.2 (2020-05-19): add support for 'C0', '*' option
# 0.1.1 (2020-10-12): add support for specifying hotstring file, directional keys, 'O' option, 'B0' option
# 0.1.0 (2019-09-24): initial commit; added support for comments

import argparse
import re
import sys

import pynput

def load_hotstrings(args):
    # Using AHK hotstring format
    exp = re.compile('^:(?P<options>.*):(?P<abbr>.+)::(?P<full>[^;]+\S)(\s+;.*)?$')
    # TODO: Add support for multiline text
    # N.b. Default behavior is different from AutoHotkey default in that case sensitivity is on;
    #      also, due to parsing and returning the file as a dict, *the last match wins*, unlike AutoHotley's default.
      # *: no end character needed to trigger
      # ?: trigger inside word
        # TODO: pending testing on AHK: if 2 abbreviations match, which one wins?
        # (e.g., for hotstrings 'AVE' and 'RAVE', which one will 'CRAVE' match if 'trigger inside word' is on?)
        # Also, replace() needs to be modified such that, instead of a full match,
        # the text buffer will just need endswith(trigger_string) to return true to trigger a match)
      # C0: case insensitive
    with open(args.file, 'r') as f:
        # Ignore non-hotstring lines
        raw_lines = filter(lambda x: x.startswith(':'),[i.strip() for i in f.readlines()])
        hotstrings = {re.search(exp,i)['abbr']:(re.search(exp,i)['full'],re.search(exp,i)['options']) for i in raw_lines}

        ## New parser ##
        # Initialize state variables and dicts
        #in_comment_block = False
        #no_endchar_hotstrings = dict()
        #intraword_hotstrings = dict()
        #no_case_hotstrings = dict()
        # Define regexes
        #directive_exp = re.compile('#(?P<directive_name>[a-zA-Z]+)(?P<directive_contents>.*)')
        #hotstring_exp = re.compile('^:(?P<options>.*):(?P<abbr>.+)::((?P<full>[^;]+\S)(\s+;.*)?)?$')
        #raw_line = f.readline()
        #while raw_line:
        #    # Strip comments
        #    ## single-line comment 
        #    if raw_line.strip().startswith(';'):
        #        raw_line = f.readline()
        #        continue
        #    ## multi-line comment
        #    if raw_line.strip().startswith('/*'):
        #        in_comment_block = True
        #        raw_line = f.readline()
        #        continue
        #    if in_comment_block == True:
        #        raw_line = f.readline()
        #        continue
        #    if raw_line.strip().startswith('*/'):
        #        in_comment_block = False
        #        raw_line = raw_line[raw_line.rindex('*/')+2:]
        #        continue
        #    # Parse line
        #    ## directives 
        #    directive = re.search(directive_exp, raw_line)
        #    if directive:
        #        # TODO: change behavior based on directive
        #        if directive['directive_name'] == 'Hotstring':
        #            if directive['directive_content'] == 'NoMouse':
        #                # Prevents mouse clicks from resetting buffer
        #                #...
        #                continue
        #            else:
        #                hotstring_options = directive['directive_content'].split()
        #        continue
        #    ## hotstring
        #    match = re.search(hotstring_exp, raw_line)
        #    if match:
        #        # TODO: build hotstring dicts based on hotstring options
        #        # No end character to trigger
        #        if match['options'] == '*':
        #            no_endchar_hotstrings[match['abbr']] = match['full']
        #        # Match within word
        #        if match['options'] == '?':
        #            intraword_hotstrings[match['abbr']] = match['full']
        #        # Ignore case
        #        if match['options'] == 'C0':
        #            no_case_hotstrings[match['abbr']] = match['full']
        # TODO: return more than one dict
    return hotstrings

def replace(hs):
    global text
    try:
        out = hs[text][0]
    except KeyError:
        print('[INFO] Exact case-matched key not found in hotstring dict, assuming case insensitivity', file=sys.stderr)
        text = text.lower()
        out = hs[text][0]
    # Replace special keys with unassigned Unicode characters:
      # Left: U+0380
      # Right: U+0381
      # Up: U+0382
      # Down: U+0383
    out = re.sub('{left (\d+)}', lambda a: '\u0380' * int(a[1]), out)
    out = re.sub('{right (\d+)}', lambda a: '\u0381' * int(a[1]), out)
    out = re.sub('{up (\d+)}', lambda a: '\u0382' * int(a[1]), out)
    out = re.sub('{down (\d+)}', lambda a: '\u0383' * int(a[1]), out)
    # Replace backspace with U+0008
    out = re.sub('{backspace (\d+)}', lambda a: '\u0008' * int(a[1]), out)
    out = re.sub('{bs (\d+)}', lambda a: '\u0008' * int(a[1]), out)
    # 'B0' turns off auto backspacing
    if 'B0' not in hs[text][1]:
        bs_count = len(text)
        if '*' not in hs[text][1]:
            bs_count += 1
        # Text buffer is clobbered beyond this point
        for x in range(bs_count):
            controller.press(pynput.keyboard.Key.backspace)
            controller.release(pynput.keyboard.Key.backspace)
    for c in out:
        if c == '\u0380':
            controller.press(pynput.keyboard.Key.left)
            controller.release(pynput.keyboard.Key.left)
        elif c == '\u0381':
            controller.press(pynput.keyboard.Key.right)
            controller.release(pynput.keyboard.Key.right)
        elif c == '\u0382':
            controller.press(pynput.keyboard.Key.up)
            controller.release(pynput.keyboard.Key.up)
        elif c == '\u0383':
            controller.press(pynput.keyboard.Key.down)
            controller.release(pynput.keyboard.Key.down)
        elif c == '\u0008':
            controller.press(pynput.keyboard.Key.backspace)
            controller.release(pynput.keyboard.Key.backspace)
        else:
            controller.type(c)

def on_press(key):
    global text
    # Trigger by endchar
    if (key in endchars) or (key.__str__()[1] in endchars):
        if text in hotstrings.keys():
            # The reason we're determining which logical branch to take up here and not one level below is
            # because the text buffer will get clobbered as soon as replace() is called.
            # 'O' option omits end character
            if 'O' not in hotstrings[text][1]:
                replace(hotstrings)
                controller.press(key)
                controller.release(key)
            else:
                replace(hotstrings)
        elif text.lower() in no_case_hotstrings.keys():
            # 'O' option omits end character
            if 'O' not in no_case_hotstrings[text.lower()][1]:
                replace(no_case_hotstrings)
                controller.press(key)
                controller.release(key)
            else:
                replace(no_case_hotstrings)
        # Clear buffer after triggering
        text = ''
    elif key == pynput.keyboard.Key.backspace:
        text = text[:-1]
    else:
        try:
            text += key.char
        except AttributeError:
            if args.debug:
                print("[DEBUG] Key:", key, file=sys.stderr)
        # No trigger by endchar
        if text in no_endchar_hotstrings.keys():
            # Defaults to omitting end character (equivalent to 'O' option) since retyping the last character makes no sense
            replace(no_endchar_hotstrings)
            # Clear buffer after triggering
            text = ''
    if args.debug:
        print("[DEBUG] current buffer:", text, ", length:", len(text), file=sys.stderr)

def on_release(key):
    # With apologies to the vim users out there...
    if key == pynput.keyboard.Key.esc:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Abbreviation expansion in the spirit of AutoHotkey",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--debug", action="store_true", help="print debug info")
    parser.add_argument("-f", "--file", type=str, help="hotstring file", default="hotstrings.txt")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.2")
    args = parser.parse_args()

    # Read hotstring file
    if args.debug:
        print('[DEBUG] Loading hotstring file: ', args.file, file=sys.stderr)
    hotstrings = load_hotstrings(args)

    no_endchar_hotstrings = {a:b for (a, b) in hotstrings.items() if '*' in b[1]}
    if args.debug:
        print('[DEBUG] no_endchar_hotstrings: ', no_endchar_hotstrings, file=sys.stderr)
    no_case_hotstrings = {a.lower():b for (a,b) in hotstrings.items() if 'C0' in b[1]}
    if args.debug:
        print('[DEBUG] no_case_hotstrings: ', no_case_hotstrings, file=sys.stderr)
    intraword_hotstrings = {a:b for (a,b) in hotstrings.items() if '?' in b[1]}
    if args.debug:
        print('[DEBUG] intraword_hotstrings: ', intraword_hotstrings, file=sys.stderr)

    # Create text buffer
    text = ''

    # Define endchars
    # TODO: add mechanism to modify this list at runtime
    # Removed forward slash from endchars since it precludes many abbreviations from triggering
    endchars = ['-', '(', ')', '[', ']', '{', '}', ':', ';', "'", '"', '\\', ',', '.', '?', '!', pynput.keyboard.Key.space, pynput.keyboard.Key.enter]

    controller = pynput.keyboard.Controller()
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
