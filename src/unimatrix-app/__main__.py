#!/usr/bin/env python3
#
# unimatrix.py
# <https://github.com/will8211/unimatrix>
#
# Python script to simulate the display from "The Matrix" in terminal. Uses
# half-width katakana unicode characters by default, but can use custom
# character sets. Accepts keyboard controls while running.
#
# Based on CMatrix by Chris Allegretta and Abishek V. Ashok. The following
# option should produce virtually the same output as CMatrix:
# $ unimatrix -afn -l o
#
# Unimatrix is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Unimatrix is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License at
# <http://www.gnu.org/licenses/> for more details.
#
# Created by William Mannard
# 2018/01/19

import curses
import json
import time
import unicodedata
from random import randint

from .canvas import Canvas
from .key_handler import KeyHandler
from .help import help_msg
from .build_parser import build_parser
from .status import Status
from .writer import Writer

### Set up parser and apply arguments settings

parser = build_parser()
args = parser.parse_args()

if args.help:
    print(help_msg)
    exit()

with open('char_sets.json') as f:
    char_set = json.load(f)

colors_str = {
    'green': curses.COLOR_GREEN,
    'red': curses.COLOR_RED,
    'blue': curses.COLOR_BLUE,
    'white': curses.COLOR_WHITE,
    'yellow': curses.COLOR_YELLOW,
    'cyan': curses.COLOR_CYAN,
    'magenta': curses.COLOR_MAGENTA,
    'black': curses.COLOR_BLACK,
    'default': -1}

start_color = colors_str[args.color]
start_bg = colors_str[args.bg_color]

speed = args.speed
start_delay = (100 - speed) * 10

runtime = None

if args.time:
    runtime = args.time

characters = ''
if args.character_set:
    try:
        value = char_set[args.character_set]
    except KeyError:
        print("Character set '%s' not found" % args.character_set)
        exit()
    if type(value) == dict:
        for character in range(0x4e00, 0x9fa6): 
            characters += chr(character)
    else:
        characters = value
else:
    characters = 'ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ12345678901234567890-=*_+|:<>"-=*_+|:<>"-=*_+|:<>"-=*_+|:<>"'

def has_double_width_chars(string):
    for char in string:
        status = unicodedata.east_asian_width(char)
        if status == 'F':
            return True
    return False

column_spacing = args.column_spacing
if column_spacing > 5 :
    column_spacing = 5
elif column_spacing < 1 :
    column_spacing = 1
if column_spacing == 1 and has_double_width_chars(characters):
    column_spacing == 2



if args.no_bold:
    args.all_bold = False


def draw_loop(screen):
    """
    Main loop that redraws the canvas each frame
    """
    writer = Writer(screen, start_color, start_bg, characters, args)
    stat = Status(screen, args)
    key = KeyHandler(screen, stat, start_delay, start_color, start_bg, colors_str, args)
    # Prevent single_wave mode from shutting down too early:
    if args.single_wave:
        wave_delay = 10
    else:
        wave_delay = 0

    starttime = time.time()

    # Keep restarting however many times the screen resizes
    while True:
        canvas = Canvas(screen, column_spacing, args)
        # Set a rhythm for asynchronous movement
        async_clock = 5
        # Loop to draw the green rain
        while not canvas.size_changed:
            if runtime and time.time() - starttime > runtime:
                exit()
            # Catch keypress
            if key.get():
                continue
            # Spawn new nodes
            for col in canvas.columns:
                if col.timer == 0:
                    col.spawn_node(canvas)
                col.timer -= 1

            for node in canvas.nodes:

                if not args.flashers_off:
                    if node.n_type == 'writer' and not randint(0, 9):
                        canvas.flashers.add((node.y_coord, node.x_coord))
                    elif node.n_type == 'eraser':
                        try:
                            canvas.flashers.remove((node.y_coord, node.x_coord))
                        except KeyError:
                            pass

                if not args.asynchronous_off:
                    if async_clock % node.async_speed == 0:
                        writer.draw(node)
                        node.y_coord += 1
                else:
                    writer.draw(node)
                    node.y_coord += 1

                # Mark old nodes for deletion
                if node.y_coord >= canvas.row_count:
                    if node.white:
                        # Stop white nodes from staying 'stuck' on last row.
                        # Creates a special green node with a last_char
                        # attribute to overwrite last white node.
                        node.white = False
                        node.y_coord -= 1
                    else:
                        node.expired = True

            if not args.flashers_off and (not async_clock % 3):
                for f in canvas.flashers:
                    writer.draw_flasher(f)

            # Rewrite nodes list without expired nodes
            canvas.nodes = [node for node in canvas.nodes if not node.expired]

            if args.single_wave:
                if len(canvas.nodes) == 0 and wave_delay < 0:
                    exit()
                wave_delay -= 1

            # End of loop, refresh screen
            if stat.countdown > 0:
                if stat.countdown == 1:
                    stat.clear()
                else:
                    stat.refresh()
                stat.countdown -= 1
            screen.refresh()

            # Check for screen resize
            if screen.getmaxyx() != (canvas.row_count, canvas.col_count):
                canvas.size_changed = True

            # Add delay before next loop
            curses.napms(key.delay)

            # update async clock
            if async_clock:
                async_clock -= 1
            else:
                async_clock = 5

def main():
    """
    Wrapper to allow CTRL-C to exit smoothly:
    """
    try:
        curses.wrapper(draw_loop)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
