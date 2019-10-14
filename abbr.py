#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# abbr.py - Abbreviation expansion in the spirit of AutoHotkey
# Author: Chang-Yi Yen <changyiyen gmail com>
# License: coffeeware
# Version 0.1.1 (2019-10-12)

import argparse
import json
import re
import sys

import pynput

def load_hotstrings(args):
    # Using JSON file
    #with open('hotstrings.json', 'r') as f:
    #    hotstrings = json.load(f)
    #return hotstrings
    # Using AHK hotstring format
    exp = re.compile('^:(?P<options>.*):(?P<abbr>.+)::(?P<full>[^;]+\S)(\s+;.*)?$')
    # TODO: Add support for hotstring options
    # N.b. Default behavior is different from AutoHotkey default in that case sensitivity is the default
      # *: no end character needed to trigger
        # Create a separate dictionary where every keystroke triggers replace()
        # Also, replace() needs to be modified such that, instead of a full match,
        # the text buffer will just need endswith(trigger_string) to return true to trigger a match)
      # ?: trigger inside word
        # Pending testing on AHK: if 2 abbreviations match, which one wins?
        # (e.g., for hotstrings 'AVE' and 'RAVE', which one will 'CRAVE' match if 'trigger inside word' is on?)
      # C1: case insensitive
        # Create a separate dictionary with all lowercase keys like {key.lower():hotstrings[key] for key in hotstrings}
        # then match the all-lowercase buffer text.lower() against that
    with open(args.file, 'r') as f:
        # Ignore non-hotstring lines
        raw_lines = filter(lambda x: re.search('^:', x),[i.strip() for i in f.readlines()])
        hotstrings = {re.search(exp,i)['abbr']:(re.search(exp,i)['full'],re.search(exp,i)['options']) for i in raw_lines}
    return hotstrings

def replace(hotstrings):
    global text
    out = hotstrings[text][0]
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
    if 'B0' not in hotstrings[text][1]:
        for x in range(len(text)+1):
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
    endchars = ['-', '(', ')', '[', ']', '{', '}', ':', ';', "'", '"', '/', '\\', ',', '.', '?', '!', pynput.keyboard.Key.space, pynput.keyboard.Key.enter]
    if (key in endchars) or (key.__str__()[1] in endchars):
        if text in hotstrings.keys():
            # The reason we're determining which logical branch to take up here and not one level below is
            # because the text buffer will get clobbered as soon as replace() is called
            if 'O' not in hotstrings[text][1]:
                replace(hotstrings)
                controller.press(key)
                controller.release(key)
            else:
                replace(hotstrings)
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
    if args.debug:
        print("[DEBUG] current buffer:", text, ", length:", len(text), file=sys.stderr)

def on_release(key):
    if key == pynput.keyboard.Key.esc:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Abbreviation expansion in the spirit of AutoHotkey",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug info")
    parser.add_argument("-f", "--file", type=str, help="Hotstring file", default="hotstrings.txt")
    args = parser.parse_args()

    # Read hotstring file
    if args.debug:
        print('[DEBUG] Loading hotstring file: ', args.file, file=sys.stderr)
    hotstrings = load_hotstrings(args)

    # Create text buffer
    text = ''

    controller = pynput.keyboard.Controller()
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
