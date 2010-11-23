#!/usr/bin/python2

class GameReader(object):
    EMPTY_CHAR = "."
    FILL_CHAR  = "@"

    def __init__(self, file):
        self.file = file

    def read(self):
        f = open(file, "r")
        self.lines = f.readlines()
        f.close()

        rows = len(self.lines)
        cols = len(self.lines[0])
        self.map = [[self.lines[r][c]
            for c in cols]
            for r in rows]

    def __str__(self):
        return str(self.map)

if __name__ == "__main__":
    g = GameReader("test.life")
    g.read()
    print g
