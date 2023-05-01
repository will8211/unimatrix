from .column import Column
import curses

class Canvas:
    """
    Represents the whole screen and stores its height and width. Gets
    overwritten whenever the screen resizes. Serves as a container for columns.
    """

    def __init__(self, screen, column_spacing, args):
        screen.clear()
        rows, cols = screen.getmaxyx()
        self.col_count = cols
        self.row_count = rows
        self.size_changed = False
        self.columns = []
        for col in range(0, cols, column_spacing * 2):
            self.columns.append(Column(col, self.row_count, args))
        self.nodes = []
        self.flashers = set()

        # Draw a background
        for x in range(self.row_count):
            try:
                screen.addstr(x, 0, ' ' * self.col_count, curses.color_pair(1))
            except curses.error:
                pass
