#!/usr/bin/python2

class Cell(object):
    '''This class represents a cell in the game grid'''
    def __str__(self):
        return "#<Cell>"

if __name__ == "__main__":
    c = Cell()
    d = Cell()

    print c
    print d
