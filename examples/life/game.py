#!/usr/bin/python2

class UnknownCharacterException(Exception):
    pass

from cell import Cell

class Game(object):
    '''This class runs the life simulation'''

    CELL_CHAR  = "@"
    EMPTY_CHAR = "."

    def __init__(self, text_map):
        '''Takes an initial map (array of arrays of chars "." or "@")'''
        self.text_map = text_map

        self.rows = len(text_map)
        self.cols = len(text_map[0])

        self.make_initial_map()

    @property
    def dimensions(self):
        return (self.cols, self.rows)

    def make_initial_map(self):
        '''Fills the initial map with None or Cells based on the text map'''
        self.map0 = [[
            self._cell_or_empty(col, row)
            for col in xrange(self.cols)]
                for row in xrange(self.rows)]

        self.map1 = [[
            None
            for col in row]
                for row in self.text_map]

    def _cell_or_empty(self, col, row):
        '''Determines if a character represents a cell or nothing'''
        char = self.text_map[row][col]

        if   char == Game.CELL_CHAR:  return Cell()
        elif char == Game.EMPTY_CHAR: return None
        else: raise UnknownCharacterException

    def num_neighbors(self, position):
        '''Return the number of neighbors for position'''
        col, row = position

        mods1 = (-1, 0, +1)
        mods2 = [
            (c, r)
            for c in mods1
            for r in mods1
            if (c, r) != (0, 0)]

        positions = [
            (col + c, row + r)
            for c, r in mods2]

        neighbors = [self.mat_get(*position) for position in positions]
        neighbors = filter(lambda x: x != None, neighbors)

        return len(neighbors)

    def test(self):
        for c in xrange(self.cols):
            for r in xrange(self.rows):
                num = self.num_neighbors((c, r))
                if num > 0:
                    print "%i neighbors at (%i, %i)" % (num, c, r)

    def mat_get(self, col, row, default=None):
        '''Get the item at self.map0[col][row] or return default value'''
        try: 
            return self.map0[col][row]
        except IndexError:
            return None

    def tick(self):
        for r, row in enumerate(self.map0):
            for c, item in enumerate(row):
                n = self.num_neighbors((c, r))

                self.map1[r][c] = self.do_rules(item, n, (c, r))

        self.swap_mat()

    def do_rules(self, item, neighbors, position):
        c, r = position
        n = neighbors

        # If the grid is empty
        if item is None:
            if n == 3:
                return Cell()
            else:
                return None
        # If the grid has a cell
        else:
            if n < 2:
                return None
            elif n > 3:
                return None
            else:
                return item

    def swap_mat(self):
        self.map0, self.map1 = \
        self.map1, self.map0

    def cells(self):
        return [(item, (c, r))
        for r, row in enumerate(self.map0)
        for c, item in enumerate(row)
        if item is not None]

if __name__ == "__main__":
    from reader import Reader
    r = Reader("test.life")
    g = Game(r.char_map)
    g.test()
