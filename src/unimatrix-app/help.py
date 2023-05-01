help_msg = '''
USAGE
  unimatrix [-a] [-b] [-c COLOR] [-f] [-g COLOR] [-h] [-i] [-l CHARACTER_SET]
            [-n] [-o] [-s SPEED] [-u CUSTOM_CHARACTERS]

OPTIONAL ARGUMENTS
  -b                   Use only bold characters

  -B                   Do not use bold characters (overrides -b)

  -c COLOR             One of: green (default), red, blue, white, yellow, cyan,
                       magenta, black

  -g COLOR             Background color (See -c). Defaults to keeping
                       terminal's current background.

  -h                   Show this help message and exit

  -i                   Ignore keyboard

  -l CHARACTER_SET     Select character set(s) using a string over letter
                       codes (see CHARACTER SETS below.)

  -s SPEED             One of "slowest", "slow", "fast", "fastest",
                       or an number value representing milliseconds between refreshs.
                       Defaults to  

  -t TIME              Exit the process after TIME seconds

  -w                   Single-wave mode: Does a single burst of green rain,
                       exits. You can put in a .bashrc file to run when your
                       terminal launches.

  -y                   Disable cycling characters that continuously change in place.
                       Good for low-resource systems

LONG ARGUMENTS
  -a --asynchronous-off
  -b --all-bold
  -B --bold-off
  -c --color=COLOR
  -f --flashers-off
  -g --bg-color=COLOR
  -h --help
  -i --ignore-keyboard
  -l --character-set=CHARACTER_SET
  -s --speed=SPEED

  -o --status-off
  -t --time
  -w --single_wave

CHARACTER SETS
  When using '-l' or '--character-set=' option, follow it with one or more of
  the following letters:

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
    $ unimatrix -afnl o

  Use the letters from the name of your favorite operating system in bold blue:
    $ unimatrix -B -u Linux -c blue

  Use default character set, plus dollar symbol (note single quotes around
      special character):
    $ unimatrix -l knnssssu -u '$'

  No bold characters, slowly, using emojis, numbers and a few symbols:
    $ unimatrix -n -l ens -s 50
'''