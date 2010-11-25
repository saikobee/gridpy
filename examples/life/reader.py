#!/usr/bin/python2

class Reader(object):
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
            if  char != "\n"]
                for line in lines]
        
        self.str = self._str()

    def _str(self):
        lines = ["".join(line) for line in self.char_map]
        return "\n".join(lines)

    def get_char_map(self):
        '''Return the char map matrix'''
        return char_map

    def __str__(self):
        return self.str

# GameReader test code
if __name__ == "__main__":
    f = "test.life"
    r = Reader(f)
    print r
