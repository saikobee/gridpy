#!/usr/bin/python2

class Cell(object):
    '''This class represents a cell in the game grid'''

    def __init__(self, position):
        '''Takes the position for the cell'''
        self.x, self.y = position

    @property
    def position(self):
        return (self.x, self.y)

    def __str__(self):
        return "#<Cell x=%i, y=%i>" % self.position

if __name__ == "__main__":
    c = Cell((0, 0))
    d = Cell((2, 3))

    c.x += 1
    d.y -= 1

    print c
    print d
