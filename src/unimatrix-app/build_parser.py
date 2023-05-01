import argparse

def build_parser():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-a', '--asynchronous-off',
                        action='store_true',
                        help='disable asynchronous scrolling')
    parser.add_argument('-b', '--all-bold',
                        action='store_true',
                        help='use all bold characters')
    parser.add_argument('-c', '--color',
                        default='green',
                        help='one of: green (default), red, blue, white, yellow, \
                            cyan, magenta, black',
                        type=str)
    parser.add_argument('-f', '--flashers-off',
                        action='store_true',
                        help='turn off characters that change in place')
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
    parser.add_argument('-l', '--character-set',
                        help='character set. See details below',
                        type=str)
    parser.add_argument('-n', '--no-bold',
                        action='store_true',
                        help='do not use bold characters')
    parser.add_argument('-o', '--status-off',
                        action='store_true',
                        help='Disable on-screen status')
    parser.add_argument('-s', '--speed',
                        help='speed, integer up to 100. Default=96',
                        default=96,
                        type=int)
    parser.add_argument('-S', '--column-spacing',
                    help='Space between columns, integer up to 5. Default=1 (2 for fullwidth characters)',
                    default=1,
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

    return parser