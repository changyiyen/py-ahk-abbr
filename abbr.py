#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# abbr.py - Abbreviation expansion in the spirit of AutoHotkey
# Author: Chang-Yi Yen <changyiyen gmail com>
# License: coffeeware
# Version 0.1.0 (2019-09-25)

import json
import re

import pynput

def load_hotstrings():
    # Using JSON file
    #with open('hotstrings.json', 'r') as f:
    #    hotstrings = json.load(f)
    #return hotstrings
    # Using AHK hotstring format
    #exp = re.compile('^:(?P<options>.*):(?P<abbr>.+)::(?P<full>.*)$')
    exp = re.compile('^::(?P<abbr>.+)::(?P<full>[^;]+\S)(\s+;.*)?$')
    with open('hotstrings.txt', 'r') as f:
        # Ignore non-hotstring lines
        raw_lines = filter(lambda x: re.search('^:', x),[i.strip() for i in f.readlines()])
        hotstrings = {re.search(exp,i)['abbr']:re.search(exp,i)['full'] for i in raw_lines}
    return hotstrings

def on_press(key):
    global text
    endchars = ['-', '(', ')', '[', ']', '{', '}', ':', ';', "'", '"', '/', '\\', ',', '.', '?', '!', pynput.keyboard.Key.space, pynput.keyboard.Key.enter]
    #if key == pynput.keyboard.Key.space:
    if key in endchars:
        if text in hotstrings.keys():
            out = hotstrings[text]
            #print("Bksp ", len(text)+1, "times")
            for x in range(len(text)+1):
                controller.press(pynput.keyboard.Key.backspace)
                controller.release(pynput.keyboard.Key.backspace)
            controller.type(out)
        text = ''
    elif key == pynput.keyboard.Key.backspace:
        text = text[:-1]
    else:
        try:
            text += key.char
        except AttributeError:
            print("[DEBUG] Key:", key)
    print("[DEBUG] current buffer:", text, ", length:",len(text))

def on_release(key):
    if key == pynput.keyboard.Key.esc:
        return False

if __name__ == '__main__':
    # Read hotstring file
    # TODO: add signal handler to reload file
    hotstrings = load_hotstrings()

    # Current text buffer
    text = ''

    controller = pynput.keyboard.Controller()
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
