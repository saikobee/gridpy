#!/usr/bin/python2

class GameReader(object):
    '''This class turns a text file into a matrix of characters'''

    def __init__(self, file):
        '''Initializes the map from the given file'''
        self.read(file)

    def read(self, file):
        '''This method reads in the file data and processes it'''
        f = open(file)
        lines = f.readlines()
        f.close()

        rows = len(lines)
        cols = len(lines[0])
        self.char_map = [[
            char
            for char in line
            if char != "\n"]
                for line in lines]

    def get_char_map(self):
        '''Return the char map matrix'''
        return char_map

    def __str__(self):
        lines = ["".join(row) for row in self.char_map]
        return "\n".join(lines)

# GameReader test code
if __name__ == "__main__":
    f = "test.life"
    g = GameReader(f)
    print g
