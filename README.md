# UniMatrix

Python script to simulate the display from "The Matrix" in terminal. Uses half-width katakana unicode characters by default, but can use custom character sets. Accepts keyboard controls while running.

Based on CMatrix by Chris Allegretta and Abishek V. Ashok. The following option should produce virtually the same output as CMatrix:
```
$ unimatrix -n -s 96 -l o
```
## Install

Linux users can use curl to install:
```
sudo curl -L https://raw.githubusercontent.com/will8211/unimatrix/master/unimatrix.py -o /usr/local/bin/unimatrix
sudo chmod a+rx /usr/local/bin/unimatrix
```
If you do not have curl, you can alternatively use a recent wget:
```
sudo wget https://raw.githubusercontent.com/will8211/unimatrix/master/unimatrix.py -O /usr/local/bin/unimatrix
sudo chmod a+rx /usr/local/bin/unimatrix
```
You can also install it with pip:
```
pip install git+https://github.com/will8211/unimatrix.git
```

Users of Arch-based distros can get it from the AUR as ```unimatrix-git```, although it might not be the most recent version.

### User install (without sudo)

With curl:

```
curl -L https://raw.githubusercontent.com/will8211/unimatrix/master/unimatrix.py -o ~/.local/bin/unimatrix
chmod a+rx ~/.local/bin/unimatrix
```

With wget:

```
wget https://raw.githubusercontent.com/will8211/unimatrix/master/unimatrix.py -O ~/.local/bin/unimatrix
chmod a+rx ~/.local/bin/unimatrix
```

# Nix
Users of NixOS and Nix Package Manager can use fetchGit in both configuration.nix and home-manager to install it
```nix
# configuration.nix
{ config, pkgs, lib, ... }:

let
  unimatrix = import (builtins.fetchGit {
    url = "https://github.com/will8211/unimatrix";
    name = "unimatrix";
  }) { inherit pkgs; };
in
{
  environment.systemPackages = [
    unimatrix
    # ... Rest of your packages
  ];
  # ... Rest of your configuration
}

# home.nix
{ config, pkgs, ... }:

let
  unimatrix = import (builtins.fetchGit {
    url = "https://github.com/will8211/unimatrix";
    name = "unimatrix";
  }) { inherit pkgs; };
in
{
  home.packages = [
    unimatrix
    # ... Rest of your packages
  ];
  # ... Rest of your configuration
}

```
It's also possible to install it with flakes in home-manager or configuration.nix
```
# flake.nix
{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.unimatrix.url = "github:will8211/unimatrix";
}
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
  unimatrix [-a] [-b] [-c COLOR] [-f] [-g COLOR] [-h] [-i] [-l CHARACTER_LIST]
            [-n] [-o] [-s SPEED] [-u CUSTOM_CHARACTERS]

OPTIONAL ARGUMENTS
  -a                   Asynchronous scroll. Lines will move at varied speeds.

  -b                   Use only bold characters

  -c COLOR             One of: green (default), red, blue, white, yellow, cyan,
                       magenta, black

  -f                   Enable "flashers," characters that continuously change.

  -g COLOR             Background color (See -c). Defaults to keeping
                       terminal's current background.

  -h                   Show this help message and exit

  -i                   Ignore keyboard input

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
                       terminal launches. Works well with speed at 95. See -i
                       to not block keyboard input during visual effect.

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
    you don't have to select it in your terminal settings. 'Horta' seems not to
    work in Konsole. Fonts may need to be set manually as fallbacks in
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
    $ unimatrix -b -u Linux -c blue

  Use default character set, plus dollar symbol (note single quotes around
      special character):
    $ unimatrix -l knnssssu -u '$'

  No bold characters, slowly, using emojis, numbers and a few symbols:
    $ unimatrix -n -l ens -s 50
```

## License

Unimatrix is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Unimatrix is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License at <http://www.gnu.org/licenses/> for more details.
