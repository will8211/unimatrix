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

import argparse
import curses
import time
from random import choice, randint

help_msg = '''
USAGE
  unimatrix [-a] [-b] [-c COLOR] [-f] [-g COLOR] [-h] [-l CHARACTER_LIST] [-n]
            [-o] [-s SPEED] [-u CUSTOM_CHARACTERS]

OPTIONAL ARGUMENTS
  -a                   Asynchronous scroll. Lines will move at varied speeds.

  -b                   Use only bold characters

  -c COLOR             One of: green (default), red, blue, white, yellow, cyan,
                       magenta, black

  -f                   Enable "flashers," characters that continuously change.

  -g COLOR             Background color (See -c). Defaults to keeping
                       terminal's current background.

  -h                   Show this help message and exit

  -i                   Ignore keyboard

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
  -a --asynchronous
  -b --all-bold
  -c --color=COLOR
  -f --flashers
  -g --bg-color=COLOR
  -h --help
  -i --ignore-keyboard
  -l --character-list=CHARACTER_LIST
  -s --speed=SPEED
  -n --no-bold
  -o --status-off
  -t --time
  -u --custom-characters=CUSTOM_CHARACTERS
  -w --single-wave

CHARACTER SETS
  When using '-l' or '--character-list=' option, follow it with one or more of
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
  p   Klingon pIqaD (requires 'Horta' family font)*
  P   Klingon pIqaD (requires 'Klingon-pIqaD' or 'Code2000' family font)*
  r   Lowercase Roman numerals ( mcclllxxxxvvvvviiiiii )
  R   Uppercase Roman numerals ( MCCLLLXXXXVVVVVIIIIII )
  s   A subset of symbols actually used in the Matrix films ( -=*_+|:<>" )
  S   All common keyboard symbols ( `-=~!z#$%^&*()_+[]{}|\;':",./<>?" )
  u   Custom characters selected using -u switch

  For example: '-l naAS' or '--character-list=naAS' will give something similar
  to the output of the original cmatrix program in its default mode.
  '-l ACG' will use all the upper-case character sets. Use the same
  letter multiple times to increase the frequency of the character set. For
  example, the default setting is equal to '-l knnssss'.

  * With most modern Linux terminals (gnome-terminal, konsole, lxterminal,
    xfce4-terminal, mate-terminal) simply having the font installed system-wide
    is enough. The terminal will fall back to it for the Klingon, meaning that
    you don't have to select the font in your terminal settings. 'Horta' seems
    not to work in Konsole. Fonts may need to be set manually as fallbacks in
    .Xresources for older terminals, such as urxvt and xterm.

KEYBOARD CONTROL
  SPACE, CTRL-c or q   exit
  - or LEFT            decrease speed by 1
  + or RIGHT           increase speed by 1
  [ or DOWN            decrease speed by 10
  ] or UP              increase speed by 10
  a                    toggle asynchronous scrolling
  b                    cycle through bold character options
                           (bold off-->bold on-->all bold)
  f                    toggle flashing characters
  o                    toggle on-screen status
  1 to 9               set color: (1) Green   (2) Red   (3) Blue     (4) White
                                  (5) Yellow  (6) Cyan  (7) Magenta  (8) Black
                                  (9) Terminal default
  ! to (               set background color (same colors as above, but pressing
                           shift + number)

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

parser.add_argument('-a', '--asynchronous',
                    action='store_true',
                    help='use asynchronous scrolling')
parser.add_argument('-b', '--all-bold',
                    action='store_true',
                    help='use all bold characters')
parser.add_argument('-c', '--color',
                    default='green',
                    help='one of: green (default), red, blue, white, yellow, \
                          cyan, magenta, black',
                    type=str)
parser.add_argument('-f', '--flashers',
                    action='store_true',
                    help='some characters will continuously change in place')
parser.add_argument('-g', '--bg-color',
                    default='default',
                    help='background color (see -c)',
                    type=str)
parser.add_argument('-h', '--help',
                    help='display extended usage information and exit.',
                    action='store_true')
parser.add_argument('-i', '--ignore-keyboard',
                    help='ignore all keyboard input.',
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
         '1234567890-=*_+|:<>"-=*_+|:<>"-=*_+|:<>"-=*_+|:<>"',
    'n': '1234567890',
    'o': 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
         '`-=~!@#$%^&*()_+[]{}|\;\':",./<>?"',
    'p': '',
    'P': '',
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
    'black': curses.COLOR_BLACK,
    'default': -1}

start_color = colors_str[args.color]
start_bg = colors_str[args.bg_color]

speed = args.speed
start_delay = (100 - speed) * 10

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

chars_len = len(chars) - 1


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
        self.flashers = set()

        # Draw a background
        for x in range(self.row_count):
            try:
                screen.addstr(x, 0, ' ' * self.col_count, curses.color_pair(1))
            except curses.error:
                pass


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
            self.countdown = (100 // (delay // 10 + 1)) + 2

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
        self.screen.addstr(0, 0, ' ' * 11, curses.color_pair(1))


class Column:
    """
    Creates nodes (points that move down the screen) that are then stored in
    canvas.nodes. Countdown timer determines time to spawn new node.
    """

    def __init__(self, x_coord, row_count):
        self.drawing = None  # None means not yet. Later will be True or False
        self.x_coord = x_coord
        self.timer = randint(1, row_count)
        self.async_speed = randint(1, 3)
        if args.single_wave:
            # Speeds it up a bit
            self.timer = int(0.6 * self.timer)

    def spawn_node(self, canvas):
        """
        Creates nodes: points that move down the screen either writing or
        erasing characters as they go down
        """
        if args.single_wave and self.drawing is False:
            return

        self.drawing = not self.drawing

        # Multiplier (mult) is for spawning slow-moving asynchronous nodes
        # less frequently in order to maintain their length
        if args.asynchronous:
            mult = self.async_speed
        else:
            mult = 1

        if self.drawing:
            # "max_range" prevents crash with very small terminal height
            max_range = max((3 * mult), ((canvas.row_count - 3) * mult))
            self.timer = randint(3 * mult, max_range)
            if args.single_wave:
                # A bit faster for single wave mode
                self.timer = int(0.8 * self.timer)
        else:
            self.timer = randint(1 * mult, canvas.row_count * mult)

        x = self.x_coord
        n_type = 'eraser'
        async_speed = self.async_speed
        white = False
        if self.drawing:
            n_type = 'writer'
            if randint(0, 2) == 0:
                white = True

        canvas.nodes.append(Node(x, n_type, async_speed, white))


class Node:
    """
    A point that runs down the screen drawing or erasing characters.
    n_type    -> 'writer' or 'eraser'
    white     -> Bool. If True, a white char is written before the green one.
    last_char -> Stores last character, since white characters have to be
                     overwritten with the same one in green one.
    expired   -> Bool. If True, node is marked for deletion
    """

    def __init__(self, x_coord, n_type, async_speed, white=False):
        self.x_coord = x_coord
        self.y_coord = 0
        self.n_type = n_type
        self.white = white
        self.last_char = None
        self.expired = False
        self.async_speed = async_speed


class KeyHandler:
    """
    Handles keyboard input.
    """

    def __init__(self, screen, stat):
        self.screen = screen
        self.stat = stat
        self.screen.nodelay(True)
        self.delay = start_delay
        self.fg = start_color
        self.bg = start_bg

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
        if args.ignore_keyboard:
            return False;

        kp = self.screen.getch()

        if kp == -1:
            return False
        elif kp == ord(" ") or kp == ord("q") or kp == 27:  # 27 = ESC
            exit()
        elif kp == ord('a'):
            args.asynchronous = not args.asynchronous
            on_off = 'on' if args.asynchronous else 'off'
            self.stat.update('Async: %s' % on_off, self.delay)
        elif kp == ord('b'):
            self.cycle_bold()
        elif kp == ord('f'):
            args.flashers = not args.flashers
            on_off = 'on' if args.flashers else 'off'
            self.stat.update('Flash: %s' % on_off, self.delay)
        elif kp == ord('o'):
            self.toggle_status()

        # Speed control
        elif kp == ord('-') or kp == ord('_') or kp == curses.KEY_LEFT:
            self.delay = min(self.delay + 10, 10990)
            self.show_speed()
        elif kp == ord('=') or kp == ord('+') or kp == curses.KEY_RIGHT:
            self.delay = max(self.delay - 10, 0)
            self.show_speed()
        elif kp == ord('[') or kp == curses.KEY_DOWN:
            self.delay = min(self.delay + 100, 10990)
            self.show_speed()
        elif kp == ord(']') or kp == curses.KEY_UP:
            self.delay = max(self.delay - 100, 0)
            self.show_speed()

        # Foreground color control
        elif kp == ord('1'):
            self.set_fg_color('Green')
        elif kp == ord('2'):
            self.set_fg_color('Red')
        elif kp == ord('3'):
            self.set_fg_color('Blue')
        elif kp == ord('4'):
            self.set_fg_color('White')
        elif kp == ord('5'):
            self.set_fg_color('Yellow')
        elif kp == ord('6'):
            self.set_fg_color('Cyan')
        elif kp == ord('7'):
            self.set_fg_color('Magenta')
        elif kp == ord('8'):
            self.set_fg_color('Black')
        elif kp == ord('9'):
            self.set_fg_color('default')

        # Background color control
        elif kp == ord('!'):
            self.set_bg_color('Green')
        elif kp == ord('@'):
            self.set_bg_color('Red')
        elif kp == ord('#'):
            self.set_bg_color('Blue')
        elif kp == ord('$'):
            self.set_bg_color('White')
        elif kp == ord('%'):
            self.set_bg_color('Yellow')
        elif kp == ord('^'):
            self.set_bg_color('Cyan')
        elif kp == ord('&'):
            self.set_bg_color('Magenta')
        elif kp == ord('*'):
            self.set_bg_color('Black')
        elif kp == ord('('):
            self.set_bg_color('default')

        return True

    def set_fg_color(self, name):
        """
        Set foreground color
        """
        self.fg = colors_str[name.lower()]
        curses.init_pair(1, self.fg, self.bg)
        if name == 'default':
            name = "Def't color"
        self.stat.update(name, self.delay)

    def set_bg_color(self, name):
        """
        Set background color
        """
        self.bg = colors_str[name.lower()]
        curses.init_pair(1, self.fg, self.bg)
        curses.init_pair(2, curses.COLOR_WHITE, self.bg)
        self.stat.update('BG: %s' % name, self.delay)

    def show_speed(self):
        """
        Display current speed (-999 to 100) when it is changed by keypress
        """
        self.stat.update('Speed: %d' % (100 - self.delay // 10), self.delay)

    def toggle_status(self):
        """
        On 'o' keypress, turn status display on or off
        """
        args.status_off = not args.status_off
        on_off = 'off' if args.status_off else 'on'
        self.stat.update('Status: %s' % on_off, self.delay)


class Writer:
    """
    Initializes character writing options and contains methods for writing and
    erasing characters from the screen.
    """

    def __init__(self, screen):
        self.screen = screen
        self.screen.scrollok(0)
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, start_color, start_bg)
        curses.init_pair(2, curses.COLOR_WHITE, start_bg)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.white = curses.color_pair(2)

    @staticmethod
    def get_char():
        """
        Returns a random character from the active character set
        """
        return chars[randint(0, chars_len)]

    @staticmethod
    def get_attr(node, above=False):
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
        attr = self.get_attr(node)
        color = curses.color_pair(1)
        if node.n_type == 'writer':
            if not node.white and node.last_char:
                # Special green character for overwriting last white one
                # at bottom of column that was not being overwritten.
                character = node.last_char
            else:
                character = self.get_char()
            if node.white:
                color = curses.color_pair(2)

        try:
            # Draw the character
            self.screen.addstr(y, x, character, color | attr)
            if node.white:
                if node.last_char:
                    # If it's a white node, also write a green character above
                    # to overwrite last white character
                    attr = self.get_attr(node, above=True)
                    self.screen.addstr(y - 1, x, node.last_char,
                                       curses.color_pair(1) | attr)
                node.last_char = character
        except curses.error:
            # Override scrolling error if characters pushed off the screen.
            pass

    def draw_flasher(self, flasher):
        """
        Draws characters, included spaces to overwrite/erase characters.
        """
        color = curses.color_pair(1)
        attr = choice([curses.A_BOLD, curses.A_NORMAL])
        y = flasher[0]
        x = flasher[1]
        try:
            self.screen.addstr(y, x, self.get_char(), color | attr)
        except curses.error:
            pass


### Main loop

def _main(screen):
    writer = Writer(screen)
    stat = Status(screen)
    key = KeyHandler(screen, stat)
    # Prevent single_wave mode from shutting down too early:
    if args.single_wave:
        wave_delay = 10
    else:
        wave_delay = 0

    starttime = time.time()

    # Keep restarting however many times the screen resizes
    while True:
        canvas = Canvas(screen)
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

                if args.flashers:
                    if node.n_type == 'writer' and not randint(0, 9):
                        canvas.flashers.add((node.y_coord, node.x_coord))
                    elif node.n_type == 'eraser':
                        try:
                            canvas.flashers.remove((node.y_coord, node.x_coord))
                        except KeyError:
                            pass

                if args.asynchronous:
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

            if args.flashers and (not async_clock % 3):
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
    # Wrapper to allow CTRL-C to exit smoothly:
    try:
        curses.wrapper(_main)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
