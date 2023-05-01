import curses

class KeyHandler:
    """
    Handles keyboard input.
    """

    def __init__(self, screen, stat, start_delay, start_color, start_bg, colors_str, args):
        self.args = args
        self.screen = screen
        self.stat = stat
        self.screen.nodelay(True)
        self.delay = start_delay
        self.fg = start_color
        self.bg = start_bg
        self.colors_str = colors_str

    def cycle_bold(self):
        """
        Called on 'b' press. Cycles though Bold options:
        off -> on -> all bold
        """
        if self.args.all_bold:
            self.args.no_bold = True
            self.args.all_bold = False
            self.stat.update('Bold: off', self.delay)
        elif self.args.no_bold:
            self.args.no_bold = False
            self.args.all_bold = False
            self.stat.update('Bold: on', self.delay)
        else:
            self.args.no_bold = False
            self.args.all_bold = True
            self.stat.update('Bold: all', self.delay)

    def get(self):
        """
        Handles key presses. Returns True if a key was found, False otherwise.
        """
        if self.args.ignore_keyboard:
            return False

        kp = self.screen.getch()

        if kp == -1:
            return False
        elif kp == ord(" ") or kp == ord("q") or kp == 27:  # 27 = ESC
            exit()
        elif kp == ord('a'):
            self.args.asynchronous_off = not self.args.asynchronous_off
            on_off = 'off' if self.args.asynchronous_off else 'on'
            self.stat.update('Async: %s' % on_off, self.delay)
        elif kp == ord('b'):
            self.cycle_bold()
        elif kp == ord('f'):
            self.args.flashers_off = not self.args.flashers_off
            on_off = 'off' if self.args.flashers_off else 'on'
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
        self.fg = self.colors_str[name.lower()]
        curses.init_pair(1, self.fg, self.bg)
        if name == 'default':
            name = "Def't color"
        self.stat.update(name, self.delay)

    def set_bg_color(self, name):
        """
        Set background color
        """
        self.bg = self.colors_str[name.lower()]
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
