#!/usr/bin/python2

class GameReader(object):
    EMPTY_CHAR = "."
    FILL_CHAR  = "@"

    def __init__(self, file):
        self.file = file

    def read(self):
        f = open(self.file)
        self.lines = f.readlines()
        f.close()

        rows = len(self.lines)
        cols = len(self.lines[0])
        self.map = [[
            self.lines[r][c]
            for c in xrange(cols)
            if not self.lines[r][c] == "\n"]
                for r in xrange(rows)]

    def __str__(self):
        lines = ["".join(row) for row in self.map]
        return "\n".join(lines)

if __name__ == "__main__":
    f = "test.life"
    g = GameReader(f)
    g.read()
    print g
