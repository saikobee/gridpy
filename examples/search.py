#!/usr/bin/python

import math
import random
import gridpy

def nom(s):
    return s[1:-1]

map = nom('''
XXXXXXXXXXXXXXXXXXXXX
X.X..........X......X
X.X.XXXXXXXXXX......X
X.X.X...........B...X
X...XXXXXXXXXX.XXX..X
X.X.X........X.X.X..X
X.X.XXXXXXXX.X.X.X..X
X.X........X.X.X.X..X
X.X.XXXXXX.X.X.X.X..X
X.X.X....X.X.X.X.X..X
X.X.X.XXXX.X.X.X.X..X
X.X.X......X.X.X.X..X
XAX.XXXXXXXX.XXX.XX.X
X.X.................X
XXXXXXXXXXXXXXXXXXXXX
''').split()

r = len(map)
c = len(map[0])
gridpy.set_dim((c, r))
gridpy.set_square_size(20)

class World:
    def __init__(self, map):
        self.items = {}
        self.rows  = len(map)
        self.cols  = len(map[0])
        
        gridpy.set_fps(10)

        for r in xrange(self.rows):
            for c in xrange(self.cols):
                square = map[r][c]
                pos = (c, r)
                if square == 'A':
                    self.items[pos] = Player(pos, self)
                elif square == 'B':
                    self.items[pos] = Goal(pos, self)
                elif square == 'X':
                    self.items[pos] = Rock(pos, self)

        gridpy.title("Search demo")
        gridpy.show()

        for pos, thing in self.items.iteritems():
            gridpy.plot(thing.color(), pos)

    def add(self, pos, thing):
        self.items[pos] = thing
        gridpy.plot(thing.color(), pos)

    def remove(self, pos):
        del self.items[pos]
        gridpy.remove(pos)

    def step(self):
        for thing in self.items.itervalues():
            thing.act()

        for pos, thing in self.items.iteritems():
            gridpy.plot(thing.color(), pos)

        gridpy.update()

    def first_goal(self):
        for item in self.items.itervalues():
            if isinstance(item, Goal):
                return item
        return None

    def adjacents(self, pos):
        c, r = pos
        poss = [
            (c+x, r+y)
            for x in (-1, 0, 1)
            for y in (-1, 0, 1)
            if not (x == 0 and y == 0)
        ]
        return [pos for pos in poss if self.is_legal(pos)]

    def is_legal(self, pos):
        c, r = pos
        return 0 < c < self.cols and 0 < r < self.rows and self.is_empty(pos)

    def is_empty(self, pos):
        return not (pos in self.items)

    def distance(self, p1, p2):
        c1, r1 = p1
        c2, r2 = p2
        return math.sqrt((c1-c2)**2 + (r1-r2)**2)

class Player:
    def __init__(self, pos, world):
        self.pos   = pos
        self.world = world
        self.goal  = world.first_goal()
        self.bad   = {}
        self.last_pos = pos

    def act(self):
        if self.goal is not None:
            self.move_idk()
            #self.move_stupid()
            #self.move_random()
        else:
            self.move_random()

    def move_idk(self):
        adj = self.world.adjacents(self.pos)
        if self.goal in adj:
            return
        adj = [pos for pos in adj if not (pos in self.bad)]
        if adj == []:
            for pos in self.bad:
                gridpy.remove(pos)
            self.bad = {}
            adj = [pos for pos in adj if not (pos in self.bad)]
            #gridpy._debug(adj)
        adj.sort(key=lambda pos: self.world.distance(pos, self.goal.pos))
        while len(adj) > 0 and adj[0] == self.last_pos:
            self.bad[adj[0]] = True
            gridpy.plot(gridpy.YELLOW, adj[0])
            del adj[0]
        if len(adj) > 0:
            self.last_pos = self.pos
            self.move_to(adj[0])

    def move_stupid(self):
        adj = self.world.adjacents(self.pos)
        adj.sort(key=lambda pos: self.world.distance(pos, self.goal.pos))
        self.move_to(adj[0])

    def move_random(self):
        adj = self.world.adjacents(self.pos)
        adj.sort(key=lambda x: random.random())
        self.move_to(adj[0])

    def move_to(self, pos):
        if self.world.is_empty(pos):
            self.world.remove(self.pos)
            self.world.add(pos, self)
            self.pos = pos

    def color(self):
        return gridpy.CYAN

class Immobile:
    def __init__(self, pos, world):
        self.pos   = pos
        self.world = world

    def act(self):
        pass
    

class Goal(Immobile):
    def color(self):
        return gridpy.MAGENTA

class Rock(Immobile):
    def color(self):
        return gridpy.WHITE

def main():
    world = World(map)
    while True:
        world.step()

main()
