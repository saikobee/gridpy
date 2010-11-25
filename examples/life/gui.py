#!/usr/bin/python2

import gridpy

from game       import Game
from reader     import Reader

class GUI(object):
    '''This class manages displaying an instance of Game'''

    SQUARE_SIZE = 2
    CELL_COLOR  = gridpy.WHITE
    TITLE       = "Game of Life ::: Gridpy Edition"

    def __init__(self, char_map):
        self.game = Game(char_map)
        self.dim  = self.game.dimensions

    def config(self):
        gridpy.set_dim(self.dim)
        gridpy.set_square_size(GUI.SQUARE_SIZE)
        #gridpy.set_background_color(gridpy.BLACK)
        #gridpy.set_border_colors(gridpy.BLUE, gridpy.BLACK)
        #gridpy.set_border_colors(gridpy.GREY, gridpy.WHITE)
        gridpy.set_fps(5)
        #gridpy.set_style(gridpy.TRIPLE)
        #gridpy.set_style(gridpy.DOUBLE)
        #gridpy.set_style(gridpy.SINGLE)
        #gridpy.set_style(gridpy.NONE)

        gridpy.title(GUI.TITLE)

    def run(self):
        self.config()
        gridpy.show()
        self.main_loop()

    def main_loop(self):
        while True:
            self.game.tick()
            for cell, position in self.game.cells():  
                gridpy.plot(GUI.CELL_COLOR, position)
            gridpy.update()
            gridpy.clear()

if __name__ == "__main__":
    r = Reader("test.life")
    g = GUI(r.get_char_map())
    g.run()
