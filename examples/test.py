#!/usr/bin/python2

# TODO stuff
# - Optimize to not redraw grid lines and background unless you need to?
# - Fix single pixel mode
# - Fix grid line drawing
# - How do we want to add keybindings?
#   - Use pygame.locals
#   - Use ord('K')
#       - Use 'K' and have ord() happen behind the scenes

import gridpy

#gridpy.set_dim((100, 100))
#gridpy.set_square_size(1)
#gridpy.set_background_color(gridpy.BLACK)
#gridpy.set_border_colors(gridpy.BLUE, gridpy.BLACK)
#gridpy.set_border_colors(gridpy.GREY, gridpy.WHITE)
#gridpy.set_fps(60)
#gridpy.set_style(gridpy.TRIPLE)
#gridpy.set_style(gridpy.DOUBLE)
#gridpy.set_style(gridpy.SINGLE)
#gridpy.set_style(gridpy.NONE)

gridpy.title("A simple demo")
gridpy.show()

def cycle(list):
    while True:
        for item in list:
            yield item

rainbow = cycle([
    gridpy.CYAN,
    gridpy.YELLOW,
    gridpy.MAGENTA,
    gridpy.RED,
    gridpy.GREEN,
    gridpy.BLUE,
    gridpy.WHITE,
    gridpy.GREY,
])

while True:
    for c in xrange(gridpy.cols()):
        color = rainbow.next()
        for r in xrange(gridpy.rows()):
            gridpy.plot(color, (c, r))
            gridpy.update()
            #gridpy.remove((c, r))
    gridpy.clear()
