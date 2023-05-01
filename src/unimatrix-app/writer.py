import curses
from random import choice, randint


class Writer:
    """
    Initializes character writing options and contains methods for writing and
    erasing characters from the screen.
    """

    def __init__(self, screen, start_color, start_bg, chars, args):
        self.args = args
        self.chars = chars
        self.screen = screen
        self.screen.scrollok(0)
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, start_color, start_bg)
        curses.init_pair(2, curses.COLOR_WHITE, start_bg)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.white = curses.color_pair(2)

    def get_char(self):
        """
        Returns a random character from the active character set
        """
        chars_len = len(self.chars) - 1
        return self.chars[randint(0, chars_len)]

    def get_attr(self, node, above=False):
        """
        Returns either A_BOLD attribute or A_NORMAL based on Bold setting
        "above=True" means it an extra green character used to overwrite the
        while head character.
        """
        if self.args.no_bold:
            return curses.A_NORMAL
        elif self.args.all_bold:
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
