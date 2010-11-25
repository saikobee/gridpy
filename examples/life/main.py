#!/usr/bin/python2

from gui    import GUI
from reader import Reader

import sys

f = None
if len(sys.argv) > 1:
    f = open(sys.argv[1])
else:
    f = sys.stdin

the_reader = Reader(f)
the_gui    = GUI(the_reader.get_char_map())

the_gui.run()
