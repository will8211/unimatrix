import curses

class Status:
    """
    Displays a status message at top left when a setting is changed.
    """

    def __init__(self, screen, args):
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.args = args
        self.screen = screen
        self.countdown = 0
        self.last_message = ''

    def update(self, message, delay):
        """
        Writes new message to the status area
        """
        if not self.args.status_off:
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
