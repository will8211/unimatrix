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
# $ unimatrix -n -s 96 -l o
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
import argparse
import time
from random import randint, choice

help_msg = '''
USAGE
  unimatrix [-b] [-c COLOR] [-h] [-l CHARACTER_LIST] [-n] [-o] [-s SPEED]
            [-u CUSTOM_CHARACTERS]

OPTIONAL ARGUMENTS
  -b                   Use only bold characters

  -c COLOR             One of: green (default), red, blue, white, yellow, cyan,
                       magenta, black

  -h                   Show this help message and exit

  -l CHARACTER_LIST    Select character set(s) using a string over letter
                       codes (see CHARACTER SETS below.)

  -n                   Do not use bold characters (overrides -b)

  -o                   Disable on-screen status

  -s SPEED             Integer up to 100. 0 uses a one-second delay before
                       refreshing, 100 uses none. Use negative numbers for
                       even lower speeds. Default=85

  -t TIME              Exit the process after TIME seconds

  -u CUSTOM_CHARACTERS Your own string of characters to display. Enclose in
                       single quotes ('') to escape special characters. For
                       example: -u '#$('

  -w                   Single-wave mode: Does a single burst of green rain,
                       exits. You can put in a .bashrc file to run when your
                       terminal launches. Works well with speed at 95.

LONG ARGUMENTS
  -b --all-bold
  -c --color=COLOR
  -h --help
  -l --character-list=CHARACTER_LIST
  -s --speed=SPEED
  -n --no-bold
  -o --status-off
  -t --time
  -u --custom_characters=CUSTOM_CHARACTERS
  -w --single_wave

CHARACTER SETS
  When using '-l' or '--character_list=' option, follow it with one or more of
  the following letters:

  a   Lowercase alphabet
  A   Uppercase alphabet
  c   Lowercase Russian Cyrillic alphabet
  C   Uppercase Russian Cyrillic alphabet
  e   A few common emoji ( ☺☻✌♡♥❤⚘❀❃❁✼☀✌♫♪☃❄❅❆☕☂★ )
  g   Lowercase Greek alphabet
  G   Uppercase Greek alphabet
  k   Japanese katakana (half-width)
  m   Default 'Matrix' set, equal to 'knnssss'
  n   Numbers 0-9
  o   'Old' style non-unicode set, like cmatrix. Equal to 'AaSn'
  r   Lowercase Roman numerals ( mcclllxxxxvvvvviiiiii )
  R   Uppercase Roman numerals ( MCCLLLXXXXVVVVVIIIIII )
  s   A subset of symbols actually used in the Matrix films ( -=*_+|:<>" )
  S   All common keyboard symbols ( `-=~!z#$%^&*()_+[]{}|\;':",./<>?" )
  u   Custom characters selected using -u switch

  For exmaple: '-l naAS' or '--character_list=naAS' will give something similar
  to the output of the original cmatrix program in its default mode.
  '-l ACG' will use all the upper-case character sets. Use the same
  letter multiple times to increase the frequency of the character set. For
  example, the default setting is equal to '-l knnssss'.

KEYBOARD CONTROL
  SPACE, CTRL-c or q   exit
  - or LEFT            decrease speed by 1
  + or RIGHT           increase speed by 1
  [ or DOWN            decrease speed by 10
  ] or UP              increase speed by 10
  b                    cycle through bold character options
                           (bold off-->bold on-->all bold)
  1 to 8               set color: (1) Green   (2) Red     (3) Blue    (4) White
                                  (5) Yellow  (6) Cyan    (7) Magenta (8) Black
  o                    toggle on-screen status

EXAMPLES
  Mimic default output of cmatrix (no unicode characters, works in TTY):
    $ unimatrix -n -s 96 -l o

  Use the letters from the name of your favorite operating system in bold blue:
    $ unimatrix -B -u Linux -c blue

  Use default character set, plus dollar symbol (note single quotes around
      special character):
    $ unimatrix -l knnssssu -u '$'

  No bold characters, slowly, using emojis, numbers and a few symbols:
    $ unimatrix -n -l ens -s 50
'''

### Set up parser and apply arguments settings

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('-b', '--all-bold',
                    action='store_true',
                    help='use all bold characters')
parser.add_argument('-c', '--color',
                    default='green',
                    help='one of: green (default), red, blue, white, yellow, \
                          cyan, magenta, black',
                    type=str)
parser.add_argument('-h', '--help',
                    help='display extented usage information and exit.',
                    action='store_true')
parser.add_argument('-l', '--character-list',
                    help='character set. See details below',
                    type=str)
parser.add_argument('-n', '--no-bold',
                    action='store_true',
                    help='do not use bold characters')
parser.add_argument('-o', '--status-off',
                    action='store_true',
                    help='Disable on-screen status')
parser.add_argument('-s', '--speed',
                    help='speed, integer up to 100. Default=85',
                    default=85,
                    type=int)
parser.add_argument('-t', '--time',
                    help='time. See details below',
                    type=int)
parser.add_argument('-u', '--custom-characters',
                    help='your own string of characters to display',
                    default='',
                    type=str)
parser.add_argument('-w', '--single-wave',
                    help='runs a single "wave" of green rain then exits',
                    action='store_true')

args = parser.parse_args()

if args.help:
    print(help_msg)
    exit()

char_set = {

    'a': 'qwertyuiopasdfghjklzxcvbnm',
    'A': 'QWERTYUIOPASDFGHJKLZXCVBNM',
    'c': 'абвгдежзиклмнопрстуфхцчшщъыьэюя',
    'C': 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
    'e': '☺☻✌♡♥❤⚘❀❃❁✼☀✌♫♪☃❄❅❆☕☂★',
    'g': 'αβγδεζηθικλμνξοπρστυφχψως',
    'G': 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ',
    'k': 'ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ',
    'm': 'ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ1234567890'
          + '1234567890-=*_+|:<>"-=*_+|:<>"-=*_+|:<>"-=*_+|:<>"',
    'n': '1234567890',
    'o': 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
             + '`-=~!@#$%^&*()_+[]{}|\;\':",./<>?"',
    'r': 'mcclllxxxxvvvvviiiiii',
    'R': 'MCCLLLXXXXVVVVVIIIIII',
    's': '-=*_+|:<>"',
    'S': '`-=~!@#$%^&*()_+[]{}|\;\':",./<>?"',
    'u': args.custom_characters}

colors_str = {
    'green': curses.COLOR_GREEN,
    'red': curses.COLOR_RED,
    'blue': curses.COLOR_BLUE,
    'white': curses.COLOR_WHITE,
    'yellow': curses.COLOR_YELLOW,
    'cyan': curses.COLOR_CYAN,
    'magenta': curses.COLOR_MAGENTA,
    'black': curses.COLOR_BLACK}

start_color = colors_str[args.color]
speed = args.speed
start_delay = (100-speed)*10

runtime = None

if args.time:
    runtime = args.time

# "-l" option has been used
if args.character_list:
    chars = ''
    for letter in args.character_list:
        try:
            chars += char_set[letter]
        except KeyError:
            print("Letter '%s' does not represent a valid character list."
                  % letter)
            exit()

# "-l" not used, but "-u" is set
elif args.custom_characters:
    chars = args.custom_characters

# Neither "-l" nor "-u" has been set, use default characters
else:
    chars = char_set['m']

if args.no_bold:
    args.all_bold = False

chars_len = len(chars)-1


### Classes

class Canvas:
    """
    Represents the whole screen and stores its height and width. Gets
    overwritten whenever the screen resizes. Serves as a container for columns.
    """

    def __init__(self, screen):
        screen.clear()
        rows, cols = screen.getmaxyx()
        self.col_count = cols
        self.row_count = rows
        self.size_changed = False
        self.columns = []
        for col in range(0, cols, 2):
            self.columns.append(Column(col, self.row_count))
        self.nodes = []


class Status:
    """
    Displays a status message at top left when a setting is changed.
    """

    def __init__(self, screen):
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.screen = screen
        self.countdown = 0
        self.last_message = ''

    def update(self, message, delay):
        """
        Writes new message to the status area
        """
        if not args.status_off:
            message_str = message.ljust(11)
            self.screen.addstr(0, 0, message_str, curses.color_pair(3))
            self.last_message = message_str
            # More frames for faster speeds:
            self.countdown = (100//(delay//10 + 1)) + 2

    def refresh(self):
        """
        Used to keep refreshing status message until countdown runs out
        """
        message_str = self.last_message
        self.screen.addstr(0, 0, message_str, curses.color_pair(3))

    def clear(self):
        """
        Erases message with spaces when the countdown runs out
        """
        self.screen.addstr(0, 0, ' '*11, curses.color_pair(1))


class Column:
    """
    Creates nodes (points that move down the screen) that are then stored in
    canvas.nodes. Countdown timer determines time to spawn new node.
    """

    def __init__(self, x_coord, row_count):
        self.drawing = None #None means not yet. Later will be True or False
        self.x_coord = x_coord
        self.timer = randint(1, row_count)
        if args.single_wave:
            #Speeds it up a bit
            self.timer = int(0.6 * self.timer)

    def spawn_node(self, canvas):
        """
        Creates nodes: points that move down the screen either writing or
        erasing characters as they go down
        """
        if args.single_wave and self.drawing == False:
            return

        self.drawing = not self.drawing

        if self.drawing:
            self.timer = randint(3, canvas.row_count-3)
            if args.single_wave:
                #A bit faster for single wave mode
                self.timer = int(0.8 * self.timer)
        else:
            self.timer = randint(1, canvas.row_count)

        x = self.x_coord
        n_type = 'eraser'
        white = False
        if self.drawing:
            n_type = 'writer'
            if randint(0, 2) == 0:
                white = True

        canvas.nodes.append(Node(x, n_type, white))


class Node:
    """
    A point that runs down the screen drawing or erasing characters.
    n_type    -> 'writer' or 'eraser'
    white     -> Bool. If True, a white char is written before the green one.
    last_char -> Stores last character, since white characters have to be
                     overwritten with the same one in green one.
    expired   -> Bool. If True, node is marked for deletion
    """

    def __init__(self, x_coord, n_type, white=False):
        self.x_coord = x_coord
        self.y_coord = 0
        self.n_type = n_type
        self.white = white
        self.last_char = None
        self.expired = False


class Key_hander:
    """
    Handles keyboard input.
    """

    def __init__(self, screen, stat):
        self.screen = screen
        self.stat = stat
        self.screen.nodelay(True)
        self.delay = start_delay

    def cycle_bold(self):
        """
        Called on 'b' press. Cycles though Bold options:
        off -> on -> all bold
        """
        if args.all_bold:
            args.no_bold = True
            args.all_bold = False
            self.stat.update('Bold: off', self.delay)
        elif args.no_bold:
            args.no_bold = False
            args.all_bold = False
            self.stat.update('Bold: on', self.delay)
        else:
            args.no_bold = False
            args.all_bold = True
            self.stat.update('Bold: all', self.delay)

    def get(self):
        """
        Handles key presses. Returns True if a key was found, False otherwise.
        """
        key_pressed = True
        try:
            kp = self.screen.getch()
        except:
            kp = None
            return False
        if kp == ord(" ") or kp == ord("q") or kp == 27: #27 = ESC
            exit()
        elif kp == ord('-') or kp == ord('_') or kp == curses.KEY_LEFT:
            self.delay = min(self.delay+10, 1000)
            self.show_speed()
        elif kp == ord('=') or kp == ord('+') or kp == curses.KEY_RIGHT:
            self.delay = max(self.delay-10, 0)
            self.show_speed()
        elif kp == ord('[')  or kp == curses.KEY_DOWN:
            self.delay = min(self.delay+100, 1000)
            self.show_speed()
        elif kp == ord(']')  or kp == curses.KEY_UP:
            self.delay = max(self.delay-100, 0)
            self.show_speed()
        elif kp == ord('b'):
            self.cycle_bold()
        elif kp == ord('1'):
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            self.stat.update('Green', self.delay)
        elif kp == ord('2'):
            curses.init_pair(1, curses.COLOR_RED, -1)
            self.stat.update('Red', self.delay)
        elif kp == ord('3'):
            curses.init_pair(1, curses.COLOR_BLUE, -1)
            self.stat.update('Blue', self.delay)
        elif kp == ord('4'):
            curses.init_pair(1, curses.COLOR_WHITE, -1)
            self.stat.update('White', self.delay)
        elif kp == ord('5'):
            curses.init_pair(1, curses.COLOR_YELLOW, -1)
            self.stat.update('Yellow', self.delay)
        elif kp == ord('6'):
            curses.init_pair(1, curses.COLOR_CYAN, -1)
            self.stat.update('Cyan', self.delay)
        elif kp == ord('7'):
            curses.init_pair(1, curses.COLOR_MAGENTA, -1)
            self.stat.update('Magenta', self.delay)
        elif kp == ord('8'):
            curses.init_pair(1, curses.COLOR_BLACK, -1)
            self.stat.update('Black', self.delay)
        elif kp == ord('o'):
            self.toggle_status()
        else:
            key_pressed = False

        return key_pressed

    def show_speed(self):
        """
        Display current speed (0-100) when it is changed by keypress
        """
        self.stat.update('Speed: %d' % (100 - self.delay//10), self.delay)

    def toggle_status(self):
        """
        On 'o' keypress, turn status display on or off
        """
        if args.status_off:
            args.status_off = False
            self.stat.update('Status: on', self.delay)
        else:
            self.stat.update('Status: off', self.delay)
            args.status_off = True


class Writer:
    """
    Initializes character writing options and contains methods for writing and
    erasing charcters from the screen.
    """

    def __init__(self, screen):
        self.screen = screen
        self.screen.scrollok(0)
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, start_color, -1)
        curses.init_pair(2, curses.COLOR_WHITE, -1)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.fg_color = curses.color_pair(1)
        self.white = curses.color_pair(2)

    def get_char(self):
        """
        Returns a random character from the active character set
        """
        return chars[randint(0, chars_len)]

    def get_attr(self, node, above=False):
        """
        Returns either A_BOLD attribute or A_NORMAL based on Bold setting
        "above=True" means it an extra green character used to overwrite the
        while head character.
        """
        if args.no_bold:
            return curses.A_NORMAL
        elif args.all_bold:
            return curses.A_BOLD
        else:
            if node.white and not above:
                return curses.A_BOLD
            else:
                return choice([curses.A_BOLD, curses.A_NORMAL])

    def draw(self, node):
        """
        Draws characters, included spaces to overwrite/erase characters.
        """
        y = node.y_coord
        x = node.x_coord
        character = ' '
        color = self.fg_color
        attr = self.get_attr(node)
        if node.n_type == 'writer':
            if not node.white and node.last_char:
                #Special green character for overwriting last white one
                #at bottom of column that was not being overwritten.
                character = node.last_char
            else:
                character = self.get_char()
            if node.white:
                color = self.white

        try:
            #Draw the character
            self.screen.addstr(y, x, character, color|attr)
            if node.white:
                if node.last_char:
                    #If it's a white node, also write a green character above
                    #to overwrite last white character
                    attr = self.get_attr(node, above=True)
                    self.screen.addstr(y-1, x, node.last_char,
                                      self.fg_color|attr)
                node.last_char = character
        except curses.error:
            # Override scrolling error character are pushed off the screen.
            pass


### Main loop

def main(screen):
    writer = Writer(screen)
    stat = Status(screen)
    key = Key_hander(screen, stat)
    if args.single_wave:
        wave_delay = 10 #prevent single_wave mode from shutting down too early

    starttime = time.time()

    #Keep restarting however many times the screen resizes
    while True:
        canvas = Canvas(screen)
        #Loop to draw the green rain
        while canvas.size_changed == False:
            if runtime and time.time() - starttime > runtime:
                exit()
            #Catch keypress
            if key.get():
                continue
            #Spawn new nodes
            for col in canvas.columns:
                if col.timer == 0:
                    col.spawn_node(canvas)
                col.timer -= 1

            for node in canvas.nodes:
                writer.draw(node)

                #Move node down
                node.y_coord += 1

                #Mark old nodes for deletion
                if node.y_coord >= canvas.row_count:
                    if node.white:
                        #Stop white nodes from staying 'stuck' on last row.
                        #Creates a special green node with a last_char
                        #attribute to overwrite last white node.
                        node.white = False
                        node.y_coord -= 1
                    else:
                        node.expired = True

            #Rewrite nodes list without expired nodes
            canvas.nodes = [node for node in canvas.nodes if not node.expired]

            if args.single_wave:
                if len(canvas.nodes) == 0 and wave_delay < 0:
                    exit()
                wave_delay -= 1

            #End of loop, refresh screen
            if stat.countdown > 0:
                if stat.countdown == 1:
                    stat.clear()
                else:
                    stat.refresh()
                stat.countdown -= 1
            screen.refresh()

            #Check for screen resize
            if screen.getmaxyx() != (canvas.row_count, canvas.col_count):
                canvas.size_changed = True

            #Add delay before next loop
            curses.napms(key.delay)


### Wrapper to allow CTRL-C to exit smoothly

try:
    curses.wrapper(main)
except KeyboardInterrupt:
    pass
