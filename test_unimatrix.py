#!/usr/bin/env python3
"""
Tests for UniMatrix's keyboard handling, in particular the screensaver
mode added with '-S'/'--screensaver'.

Run with: python3 -m unittest discover
"""

import curses
import sys
import unittest

# unimatrix parses sys.argv at import time, so give it an empty argument list.
sys.argv = ['unimatrix']
import unimatrix


class FakeScreen:
    """Minimal stand-in for a curses window: hands out queued key codes."""

    def __init__(self, keys):
        self.keys = list(keys)

    def nodelay(self, flag):
        pass

    def getch(self):
        return self.keys.pop(0) if self.keys else -1


class FakeStatus:
    """Minimal stand-in for unimatrix.Status, recording the messages it gets."""

    def __init__(self):
        self.messages = []

    def update(self, message, delay):
        self.messages.append(message)


class KeyHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.addCleanup(setattr, unimatrix, 'args', unimatrix.args)

    def make_handler(self, argv, keys):
        unimatrix.args = unimatrix.parser.parse_args(argv)
        self.stat = FakeStatus()
        return unimatrix.KeyHandler(FakeScreen(keys), self.stat)

    def test_screensaver_flag_parsing(self):
        # Off by default, settable either way, and '-s' still means speed.
        self.assertFalse(unimatrix.parser.parse_args([]).screensaver)
        self.assertTrue(unimatrix.parser.parse_args(['-S']).screensaver)
        self.assertTrue(
            unimatrix.parser.parse_args(['--screensaver']).screensaver)
        speed_args = unimatrix.parser.parse_args(['-s', '42'])
        self.assertEqual(speed_args.speed, 42)
        self.assertFalse(speed_args.screensaver)

    def test_screensaver_exits_on_any_key(self):
        for key in [ord('a'), ord('1'), ord('!'), curses.KEY_UP, ord('z')]:
            handler = self.make_handler(['-S'], [key])
            with self.assertRaises(SystemExit):
                handler.get()

    def test_screensaver_does_not_exit_without_a_key_press(self):
        handler = self.make_handler(['-S'], [])
        self.assertFalse(handler.get())

    def test_normal_mode_controls_still_work(self):
        # 'a' toggles async scrolling and reports it on the status bar.
        handler = self.make_handler([], [ord('a')])
        self.assertTrue(handler.get())
        self.assertTrue(unimatrix.args.asynchronous)
        self.assertEqual(self.stat.messages, ['Async: on'])
        # '[' slows the rain down by 100ms.
        handler = self.make_handler([], [ord('[')])
        delay = handler.delay
        self.assertTrue(handler.get())
        self.assertEqual(handler.delay, delay + 100)
        # 'q' still quits.
        handler = self.make_handler([], [ord('q')])
        with self.assertRaises(SystemExit):
            handler.get()

    def test_ignore_keyboard_takes_precedence_over_screensaver(self):
        handler = self.make_handler(['-i', '-S'], [ord('q')])
        self.assertFalse(handler.get())


if __name__ == '__main__':
    unittest.main()
