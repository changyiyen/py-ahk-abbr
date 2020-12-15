#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# abbr.py - Abbreviation expansion in the spirit of AutoHotkey
# Author: Chang-Yi Yen <changyiyen gmail com>
# License: coffeeware
# Version 0.2.0 (2020-12-08)

# Version history
# 0.2.0    (2020-12-08)
# 0.1.2.1  (2020-11-19)
# 0.1.2    (2020-05-19)
# 0.1.1    (2020-10-12)
# 0.1.0    (2019-09-24)

import argparse
import collections
import datetime
import os
import re
import sys
import time

import pynput

def load_hotstrings(args):
    '''Loads hotstrings from file and performs some preprocessing'''
    # TODO: Add support for multiline text
    # N.b. Default behavior is different from AutoHotkey default in that case sensitivity is on;
    #      also, due to parsing and returning the file as a dict, *the last match wins*, unlike AutoHotkey's default.
      # *: no end character needed to trigger
      # ?: trigger inside word
        # TODO: pending testing on AHK: if 2 abbreviations match, which one wins?
        # (e.g., for hotstrings 'AVE' and 'RAVE', which one will 'CRAVE' match if 'trigger inside word' is on?)
        # Also, replace() needs to be modified such that, instead of a full match,
        # the text buffer will just need endswith(trigger_string) to return true to trigger a match)
      # C0: case insensitive
    with open(args.file, 'r') as f:
        # Initialize state variables and dicts
        in_comment_block = False
        # Starting from Python 3.7 (and CPython 3.6), dictionaries are guaranteed to preserve
        # element insertion order; nevertheless we're using OrderedDicts for compatibility
        no_endchar_hotstrings = collections.OrderedDict()
        intraword_hotstrings = collections.OrderedDict()
        no_case_hotstrings = collections.OrderedDict()
        # [extension] literal hotstrings (i.e. replacement strings are typed as-is)
        literal_hotstrings = collections.OrderedDict()
        default_hotstrings = collections.OrderedDict()
        # Define regexes
        directive_exp = re.compile('#(?P<directive_name>[a-zA-Z]+)(?P<directive_contents>.*)')
        hotstring_exp = re.compile('^:(?P<options>.*):(?P<abbr>.+)::((?P<full>[^;]*\S)(\s+;.*)?)?$')
        raw_line = f.readline()
        while raw_line:
            # Strip comments
            ## multi-line comment
            if raw_line.strip().startswith('/*'):
                in_comment_block = True
                # in case the multi-line comment is actually a single-line comment
                if raw_line.strip().endswith('*/'):
                    n_comment_block = False
                raw_line = f.readline()
                continue
            if raw_line.strip().endswith('*/'):
                # nested comments not supported
                in_comment_block = False
                raw_line = f.readline()
                continue
            if in_comment_block:
                raw_line = f.readline()
                continue
            ## single-line comment
            if raw_line.strip().startswith(';'):
                raw_line = f.readline()
                continue
            # Parse line
            ## directives 
            directive = re.search(directive_exp, raw_line)
            if directive:
                if directive['directive_name'] == 'Hotstring':
                    # TODO: Change behavior based on directive
                    if directive['directive_contents'] == 'NoMouse':
                        # Prevents mouse clicks from resetting buffer
                        #...
                        continue
                    else:
                        hotstring_options = directive['directive_contents'].split()
            ## hotstring
            match = re.search(hotstring_exp, raw_line)
            if match:
                if args.regex:
                    # No end character to trigger
                    if match['options'] == '*':
                        no_endchar_hotstrings[re.compile(match['abbr'])] = [match['full'], match['options']]
                    # Match within word
                    if match['options'] == '?':
                        intraword_hotstrings[re.compile(match['abbr'])] = [match['full'], match['options']]
                    # Ignore case
                    if match['options'] == 'C0':
                        no_case_hotstrings[re.compile(match['abbr'])] = [match['full'], match['options']]
                    # [extension] Literal hotstring
                    if args.extensions and match['options'] == 'L':
                        literal_hotstrings[re.compile(match['abbr'])] = [match['full'], match['options']]
                    else:
                        default_hotstrings[re.compile(match['abbr'])] = [match['full'], match['options']]
                else:
                    # No end character to trigger
                    if match['options'] == '*':
                        no_endchar_hotstrings[match['abbr']] = [match['full'], match['options']]
                    # Match within word
                    if match['options'] == '?':
                        intraword_hotstrings[match['abbr']] = [match['full'], match['options']]
                    # [extension] Literal hotstring
                    if args.extensions and match['options'] == 'L':
                        literal_hotstrings[match['abbr']] = [match['full'], match['options']]
                    # Ignore case
                    if match['options'] == 'C0':
                        no_case_hotstrings[match['abbr']] = [match['full'], match['options']]
                    else:
                        default_hotstrings[match['abbr']] = [match['full'], match['options']]
            raw_line = f.readline()
        for hs in (no_endchar_hotstrings, intraword_hotstrings, no_case_hotstrings, default_hotstrings):
            for k in hs.keys():
                # Replace special keys with unassigned Unicode characters:
                    # Left: U+0380
                    # Right: U+0381
                    # Up: U+0382
                    # Down: U+0383
                hs[k][0] = re.sub('{left (\d+)}', lambda a: '\u0380' * int(a[1]), hs[k][0])
                hs[k][0] = re.sub('{right (\d+)}', lambda a: '\u0381' * int(a[1]), hs[k][0])
                hs[k][0] = re.sub('{up (\d+)}', lambda a: '\u0382' * int(a[1]), hs[k][0])
                hs[k][0] = re.sub('{down (\d+)}', lambda a: '\u0383' * int(a[1]), hs[k][0])
                # Replace backspace with U+0008
                hs[k][0] = re.sub('{backspace (\d+)}', lambda a: '\u0008' * int(a[1]), hs[k][0])
                hs[k][0] = re.sub('{bs (\d+)}', lambda a: '\u0008' * int(a[1]), hs[k][0])
                # AutoHotkey built-in variables
                # TODO: complete list of builtins
                ## special characters
                ### half-width space
                hs[k][0] = hs[k][0].replace('A_Space', ' ')
                ### Unicode horizontal tab: U+0009
                hs[k][0] = hs[k][0].replace('A_Tab', '\u0009')
                ## script properties
                ### A_Args: list of command line parameters 
                ### NB. This has been changed to a space-separated string created from the list)
                hs[k][0] = hs[k][0].replace('A_Args', ' '.join(sys.argv))
                ### A_WorkingDir: current working directory
                hs[k][0] = hs[k][0].replace('A_WorkingDir', os.getcwd())
                ### A_ScriptDir: full path of directory of current script
                hs[k][0] = hs[k][0].replace('A_ScriptDir', os.path.abspath(os.path.dirname(sys.argv[0])))
                ### A_ScriptName: file name of current script
                hs[k][0] = hs[k][0].replace('A_ScriptName', __file__)
                ### A_ScriptFullPath: full path of script
                hs[k][0] = hs[k][0].replace('A_ScriptFullPath',
                    os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), __file__))
        # Merge literal_hotstrings into default_hotstrings since the trigger conditions are the same
        default_hotstrings.update(literal_hotstrings)
    return (no_endchar_hotstrings, intraword_hotstrings, no_case_hotstrings, default_hotstrings)

def replace(hs):
    '''Searches hotstring dictionaries for a replacement phrase and performs the replacement'''
    global text
    if args.regex:
        patterns = hs.keys()
    try:
        if args.regex:
            for p in patterns:
                if re.search(p, text):
                    expansion = hs[p]
        else:
            expansion = hs[text]
    except KeyError:
        print('[WARNING] expansion not found in ', hs, file=sys.stderr)
        
    out = expansion[0]
    options = expansion[1]
    if options != 'L':
        ## AutoHotkey built-in variables which may vary between calls
        ## date and time
        ## NB. date and time need to be updated with each keystroke
        ### A_YYYY, A_Year: 4-digit current year
        out = out.replace('A_YYYY', str(time.localtime().tm_year))
        out = out.replace('A_Year', str(time.localtime().tm_year))
        ### A_MM, A_Mon: 2-digit month
        out = out.replace('A_MM', str(time.localtime().tm_mon))
        out = out.replace('A_Mon', str(time.localtime().tm_mon))
        ### A_DD, A_MDay: 2-digit day of month
        out = out.replace('A_DD', str(time.localtime().tm_mday))
        out = out.replace('A_MDay', str(time.localtime().tm_mday))
        ### A_MMMM: current full name of month
        out = out.replace('A_MMMM', time.strftime('%B'))
        ### A_MMM: abbreviation of current month
        out = out.replace('A_MMM', time.strftime('%b'))
        ### A_DDDD: current full name of day of week
        out = out.replace('A_DDDD', time.strftime('%A'))
        ### A_DDD: current abbreviated name of day of week
        out = out.replace('A_DDD', time.strftime('%a'))
        ### A_WDay: 1-digit day of week (1-7, 1 always Sunday); Python sets Monday as 0
        out = out.replace('A_WDay', str((time.localtime().tm_wday + 2) % 7))
        ### A_YDay: current day of year
        out = out.replace('A_YDay', str(time.localtime().tm_yday))
        ### A_YWeek: current year and week number
        out = out.replace('A_YWeek', str(time.localtime().tm_year) + str(datetime.date.isocalendar(datetime.date.today())[1]))
        ### A_Hour: 2-digit hour
        out = out.replace('A_Hour', str(time.localtime().tm_hour))
        ### A_Min: 2-digit minute
        out = out.replace('A_Min', str(time.localtime().tm_min))
        ### A_Sec: 2-digit second
        out = out.replace('A_Sec', str(time.localtime().tm_sec))
        ### A_MSec: 3-digit millisecond
        out = out.replace('A_MSec', str(datetime.datetime.now().microsecond / 1000))
        ### A_Now: current local time (YYYYMMDDHH24MISS)
        out = out.replace('A_Now',time.strftime('%Y%m%d%H%M%S'))
        ### A_NowUTC: current UTC time (YYYYMMDDHH24MISS)
        out = out.replace('A_NowUTC',time.strftime('%Y%m%d%H%M%S', time.gmtime()))
        ## [extension] extra time variables
        ### DATE_I: local date in ISO 8601 format
        out = out.replace('DATE_I', time.strftime('%Y-%m-%d'))
        ### DATETIME_I: local date and time in ISO 8601 format, to second precision
        out = out.replace('DATETIME_I', time.strftime('%Y-%m-%dT%H:%M:%S%z'))
        ### DATE_R: local date in RFC 5322 format
        out = out.replace('DATE_R', time.strftime('%A, %d %m %Y %H:%M:%S %z'))

    # 'B0' turns off auto backspacing
    if 'B0' not in expansion[1]:
        bs_count = len(text)
        if '*' not in expansion[1]:
            bs_count += 1
        # Text buffer is clobbered beyond this point
        for x in range(bs_count):
            controller.press(pynput.keyboard.Key.backspace)
            controller.release(pynput.keyboard.Key.backspace)
    # Replace the 'out' variable with an list of varying length strings
    # (alphaneumerics/spaces and Unicode) so they can be typed out faster
    if len(out) > 0:
        outlist = re.split('([^\w\s])', out)
    if args.debug:
        print("[DEBUG] outlist:", outlist, file=sys.stderr)
    for c in outlist:
        time.sleep(args.delay)
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
        elif c == '\u0009':
            controller.press(pynput.keyboard.Key.tab)
            controller.release(pynput.keyboard.Key.tab)
        else:
            controller.type(c)

def on_press(key):
    global text
    # Trigger by endchar
    if (key in endchars) or (key.__str__()[1] in endchars):
        # Check hotstring dicts
        if args.regex:
            for pattern in default_hotstrings_keys:
                if re.search(pattern, text):
                    if 'O' not in default_hotstrings[pattern][1]:
                        replace(default_hotstrings)
                        if key in triggers_needing_shift:
                            controller.press(pynput.keyboard.Key.shift)
                        controller.press(key)
                        controller.release(key)
                        if key in triggers_needing_shift:
                            controller.release(pynput.keyboard.Key.shift)
                    else:
                        replace(default_hotstrings)
                    # Clear buffer after triggering
                    text = ''
                    break
            # We're having the hotstring option override the regex here, but
            # if you're relying on this behavior instead of writing your
            # regex properly, you should totally be ashamed of yourself...
            for pattern in no_case_hotstrings_keys:
                if re.search(pattern, text.lower()):
                    if 'O' not in no_case_hotstrings[pattern][1]:
                        replace(no_case_hotstrings)
                        if key in triggers_needing_shift:
                            controller.press(pynput.keyboard.Key.shift)
                        controller.press(key)
                        controller.release(key)
                        if key in triggers_needing_shift:
                            controller.release(pynput.keyboard.Key.shift)
                    else:
                        replace(no_case_hotstrings)
                    # Clear buffer after triggering
                    text = ''
                    break
        else:
            if text in default_hotstrings_keys:
                # The reason we're determining which logical branch to take up here and not one level below is
                # because the text buffer will get clobbered as soon as replace() is called.
                # One potential way around this problem is to use the non-blocking form of pynput's functions,
                # which should allow us to ignore the text buffer if needed.
                # 'O' option omits end character
                if 'O' not in default_hotstrings[text][1]:
                    replace(default_hotstrings)
                    if key in triggers_needing_shift:
                        controller.press(pynput.keyboard.Key.shift)
                    controller.press(key)
                    controller.release(key)
                    if key in triggers_needing_shift:
                        controller.release(pynput.keyboard.Key.shift)
                else:
                    replace(default_hotstrings)
                # Clear buffer after triggering
                text = ''
            elif text.lower() in no_case_hotstrings_keys:
                # 'O' option omits end character
                if 'O' not in no_case_hotstrings[text.lower()][1]:
                    replace(no_case_hotstrings)
                    if key in triggers_needing_shift:
                        controller.press(pynput.keyboard.Key.shift)
                    controller.press(key)
                    controller.release(key)
                    if key in triggers_needing_shift:
                        controller.release(pynput.keyboard.Key.shift)
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
        if args.regex:
            for pattern in no_endchar_hotstrings_keys:
                if re.search(pattern, text):
                    replace(no_endchar_hotstrings)
                    # Clear buffer after triggering
                    text = ''
                    break
        else:
            if text in no_endchar_hotstrings_keys:
                # Defaults to omitting end character (equivalent to 'O' option) since retyping the last character makes no sense
                replace(no_endchar_hotstrings)
                # Clear buffer after triggering
                text = ''
    if args.debug:
        print("[DEBUG] current buffer:", text, ", length:", len(text), file=sys.stderr)

def on_release(key):
    # With apologies to the vim users out there...
    if key == pynput.keyboard.Key.esc:
        raise Warning("Escape key detected")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Abbreviation expansion in the spirit of AutoHotkey",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--debug", action="store_true", help="print debug info")
    parser.add_argument("-e", "--extensions", action="store_true", help="enable extensions")
    parser.add_argument("-f", "--file", type=str, help="file containing hotstrings", default="hotstrings.ahk")
    parser.add_argument("-r", "--regex", action="store_true", help="match against regexes (experimental)")
    parser.add_argument("-t", "--delay", type=float, help="time delay between keystrokes (in seconds)", default=0.1)
    parser.add_argument("--version", action="version", version="%(prog)s 0.2.0")
    args = parser.parse_args()

    # Read hotstring file
    if args.debug:
        print('[DEBUG] Loading hotstring file: ', args.file, file=sys.stderr)
        if args.regex:
            print('[DEBUG] Running in regex mode.', file=sys.stderr)
        if args.extensions:
            print('[DEBUG] Extensions enabled.', file=sys.stderr)
    hotstrings = load_hotstrings(args)

    no_endchar_hotstrings = hotstrings[0]
    intraword_hotstrings = hotstrings[1]
    no_case_hotstrings = hotstrings[2]
    default_hotstrings = hotstrings[3]
    no_endchar_hotstrings_keys = no_endchar_hotstrings.keys()
    intraword_hotstrings_keys = intraword_hotstrings.keys()
    no_case_hotstrings_keys = no_case_hotstrings.keys()
    default_hotstrings_keys = default_hotstrings.keys()
    if args.debug:
        print('[DEBUG] no_endchar_hotstrings: ', no_endchar_hotstrings, file=sys.stderr)
        print('[DEBUG] intraword_hotstrings: ', intraword_hotstrings, file=sys.stderr)
        print('[DEBUG] no_case_hotstrings: ', no_case_hotstrings, file=sys.stderr)
        print('[DEBUG] default_hotstrings: ', default_hotstrings, file=sys.stderr)
    # Create text buffer
    text = ''
    # Define endchars
    # TODO: add mechanism to modify this list at runtime
    # Removed forward slash from endchars since it precludes many abbreviations from triggering
    # Keys requiring shift key to be held down: '(', ')', '{', '}', ':', '"', '?', '!'
    endchars = ['-', '(', ')', '[', ']', '{', '}', ':', ';', "'", '"', '\\', ',', '.', '?', '!', pynput.keyboard.Key.space, pynput.keyboard.Key.enter]
    triggers_needing_shift = [
        pynput.keyboard.KeyCode.from_char('('),
        pynput.keyboard.KeyCode.from_char(')'),
        pynput.keyboard.KeyCode.from_char('{'),
        pynput.keyboard.KeyCode.from_char('}'),
        pynput.keyboard.KeyCode.from_char(':'),
        pynput.keyboard.KeyCode.from_char('"'),
        pynput.keyboard.KeyCode.from_char('?'),
        pynput.keyboard.KeyCode.from_char('!')
    ]

    # TODO: change to a main loop to avoid blocking
    controller = pynput.keyboard.Controller()
    #with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #    listener.join()
    listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    while True:
        try:
            listener.join()
        except Warning:
            print('[INFO] Escape key pressed, exiting', file=sys.stderr)
            break