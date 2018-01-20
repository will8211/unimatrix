# UniMatrix

Python script to simulate the display from "The Matrix" in terminal. Uses half-width katakana unicode characters by default, but can use custom character sets. Accepts keyboard controls while running.

Based on CMatrix by Chris Allegretta and Abishek V. Ashok. The following option should produce virtually the same output as CMatrix:
```
$ unimatrix -n -s 96 -l o
```
## Install

You can use curl to install:
```
sudo curl -L https://raw.githubusercontent.com/will8211/unimatrix/master/unimatrix.py -o /usr/local/bin/unimatrix
sudo chmod a+rx /usr/local/bin/unimatrix
```
If you do not have curl, you can alternatively use a recent wget:
```
sudo wget https://raw.githubusercontent.com/will8211/unimatrix/master/unimatrix.py -O /usr/local/bin/unimatrix
sudo chmod a+rx /usr/local/bin/unimatrix
```

## Screenshots

Default settings:

![screenshot1](/screenshot1.png?raw=true "Default")


Blue with custom character set 'Linux' (```$ unimatrix -c blue -u 'Linux'```):

![screenshot2](/screenshot2.png?raw=true "Custom character set")


Yellow with alternate character set: Emoji (```$ unimatrix -c yellow -l 'e'```):

![screenshot3](/screenshot3.png?raw=true "Alternate character set: Emoji")


Emulating CMatrix (```unimatrix -n -s 96 -l 'o'```):

![screenshot4](/screenshot4.png?raw=true "Emulating CMatrix")


## Manual
```
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
  S   All common keyboard symbols ( `-=~!@#$%^&*()_+[]{}|\;':",./<>?" )
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
```

## License

Unimatrix is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Unimatrix is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License at <http://www.gnu.org/licenses/> for more details.
