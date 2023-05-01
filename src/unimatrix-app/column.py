from random import randint
from .node import Node

class Column:
    """
    Creates nodes (points that move down the screen) that are then stored in
    canvas.nodes. Countdown timer determines time to spawn new node.
    """

    def __init__(self, x_coord, row_count, args):
        self.drawing = None  # None means not yet. Later will be True or False
        self.x_coord = x_coord
        self.timer = randint(1, row_count)
        self.async_speed = randint(1, 3)
        self.args = args
        if args.single_wave:
            # Speeds it up a bit
            self.timer = int(0.6 * self.timer)

    def spawn_node(self, canvas):
        """
        Creates nodes: points that move down the screen either writing or
        erasing characters as they go down
        """
        if self.args.single_wave and self.drawing is False:
            return

        self.drawing = not self.drawing

        # Multiplier (mult) is for spawning slow-moving asynchronous nodes
        # less frequently in order to maintain their length
        if not self.args.asynchronous_off:
            mult = self.async_speed
        else:
            mult = 1

        if self.drawing:
            # "max_range" prevents crash with very small terminal height
            max_range = max((3 * mult), ((canvas.row_count - 3) * mult))
            self.timer = randint(3 * mult, max_range)
            if self.args.single_wave:
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
        