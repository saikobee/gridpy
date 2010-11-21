#!/usr/bin/python2
'''
Gridpy is a simple library for drawing grid based graphics, based on Pygame.
It will not support images. This is merely a really convenient way of drawing squares on the screen.
'''
__author__  = "Brian Mock <mock.brian@gmail.com>"
__version__ = "1.0"

import atexit
import pygame
import pygame.locals

### {{{ Color related stuff
def hsv2rgb(hsv):
    '''Create a new color from an HSV triplet. Hues range from 0 to 359,
    saturation ranges from 0 to 100, and value ranges from 0 to 100.'''
    c = pygame.Color(0)
    c.hsva = hsv + (100,) 
    return c[0:-1]

def hsl2rgb(hsl):
    '''Create a new color from an HSL triplet. Hues range from 0 to 359,
    saturation ranges from 0 to 100, and lightness ranges from 0 to 100.'''
    c = pygame.Color(0)
    c.hsla = hsl + (100,) 
    return c[0:-1]

def hex2rgb(hexcode):
    '''\
    Create a new color from a six digit hexadecimal number, as in HTML (but
    but without the the # sign). The format is a string of the form "RRGGBB"
    where RR, GG, and BB are two digit hexadecimal digits specifying the color
    values for red, green and blue respectively.
    '''
    r = int(hexcode[0:2], 16)
    g = int(hexcode[2:4], 16)
    b = int(hexcode[4:6], 16)
    c = pygame.Color(r, g, b)
    return c[0:-1]

# Constants for border styles
NONE   = 0
SINGLE = 1
DOUBLE = 2
TRIPLE = 3

# {{{ Basic color palette for simple drawing
RED     = hex2rgb("FF0000")
ORANGE  = hex2rgb("FFA500")
YELLOW  = hex2rgb("FFFF00")
GREEN   = hex2rgb("00FF00")
BLUE    = hex2rgb("0000FF")
INDIGO  = hex2rgb("A020F0")
VIOLET  = hex2rgb("EE82EE")
###########################
PINK    = hex2rgb("FFC0CB")
###########################
CYAN    = hex2rgb("00FFFF")
MAGENTA = hex2rgb("FF00FF")
###########################
CRIMSON = hex2rgb("880000")
###########################
BLACK   = hex2rgb("000000")
GREY    = hex2rgb("888888")
GRAY    = hex2rgb("888888")
WHITE   = hex2rgb("FFFFFF")
###########################
GREY1 = hex2rgb("111111")
GREY2 = hex2rgb("222222")
GREY3 = hex2rgb("333333")
GREY4 = hex2rgb("444444")
GREY5 = hex2rgb("555555")
GREY6 = hex2rgb("666666")
GREY7 = hex2rgb("777777")
GREY8 = hex2rgb("888888")
GREY9 = hex2rgb("999999")
GREYA = hex2rgb("AAAAAA")
GREYB = hex2rgb("BBBBBB")
GREYC = hex2rgb("CCCCCC")
GREYD = hex2rgb("DDDDDD")
GREYE = hex2rgb("EEEEEE")
GREYF = hex2rgb("FFFFFF")
#=======================#
GRAY1 = hex2rgb("111111")
GRAY2 = hex2rgb("222222")
GRAY3 = hex2rgb("333333")
GRAY4 = hex2rgb("444444")
GRAY5 = hex2rgb("555555")
GRAY6 = hex2rgb("666666")
GRAY7 = hex2rgb("777777")
GRAY8 = hex2rgb("888888")
GRAY9 = hex2rgb("999999")
GRAYA = hex2rgb("AAAAAA")
GRAYB = hex2rgb("BBBBBB")
GRAYC = hex2rgb("CCCCCC")
GRAYD = hex2rgb("DDDDDD")
GRAYE = hex2rgb("EEEEEE")
GRAYF = hex2rgb("FFFFFF")
# }}} End palettes
# }}} End color stuff

### BEGIN PRIVATES
# Screen starting size
_width, _height = None, None
_old_size = None

def _size():
    '''Returns the screen size.'''
    global _width
    global _height
    return (_width, _height)

_style = TRIPLE

def set_style(style):
    '''Sets the style of the grid squares'''
    global _style
    _style = style

_cols, _rows = 10, 10
_square_size = 25

def set_square_size(size):
    '''Sets the size of the grid squares'''
    global _square_size
    _square_size = size

# Border colors
_primary   = GREY2
_secondary = GREY2

def set_border_colors(primary, secondary):
    '''Sets the border colors (primary, secondary).'''
    global _primary
    global _secondary
    _primary   = primary
    _secondary = secondary

def set_border_color(color):
    '''Sets both border colors to color.'''
    global _primary
    global _secondary
    _primary   = color
    _secondary = color

# Background color
_background = GREY1

def set_background_color(color):
    '''Sets the background color.'''
    global _background
    _background = color

_clock         = None
_paused        = False
_show_fps      = False
_explicit_exit = False
_video_is_on   = False

_TITLE = "Gridpy " + __version__
_program = None

_fps = 60

def set_fps(fps):
    '''Sets the FPS.'''
    global _fps
    _fps = fps

_WINDOW_OPTS = (
    pygame.DOUBLEBUF |
    pygame.HWSURFACE
)

_FULLSCREEN_OPTS = (
    pygame.DOUBLEBUF  |
    pygame.HWSURFACE  |
    pygame.FULLSCREEN
)

_full_screen = False

def set_dim(dim):
    '''Sets the dimensions of the grid.'''
    global _cols
    global _rows
    _cols, _rows = dim

def dim():
    '''Returns the dimensions of the grid.'''
    global _cols
    global _rows
    return (_cols, _rows)

def rows():
    '''Returns the number of rows in the grid.'''
    global _rows
    return _rows

def cols():
    '''Returns the number of rows in the grid.'''
    global _cols
    return _cols

def _debug(*xs):
    if __debug__:
        print " ".join(map(str, xs))

def _debug_noln(*xs):
    import sys
    if __debug__:
        print " ".join(map(str, xs)),
        sys.stdout.flush()

# This should really be expressable with a lambda, python...
def _toggle_show_fps():
    global _show_fps
    _show_fps = not _show_fps

# This should really be expressable with a lambda, python...
def toggle_paused():
    global _paused
    _paused = not _paused

def _explicit_exit_func():
    global _explicit_exit
    _explicit_exit = True
    exit()

def toggle_full_screen():
    global _full_screen
    buf = _screen().copy()
    if not _full_screen:
        # (0, 0) means native resolution
        pygame.display.set_mode((0, 0), _FULLSCREEN_OPTS)
    else:
        pygame.display.set_mode(_size(), _WINDOW_OPTS)
    # TODO:
    # Should this be kept? If our screen res changes,
    # we can't really just copy the old buffer back over
    #_screen().blit(buf, (0, 0))
    _full_screen = not _full_screen

def _cycle_styles():
    '''Switches to the next border style.'''
    global _style
    _style += 1
    _style %= 4
    _maybe_resize()

def _maybe_resize():
    '''Calculates the new size needed and resizes if necessary.'''
    global _width
    global _height
    _calc_size()
    if _width  < 10: _width  = 10
    if _height < 10: _height = 10
    if _old_size != _size():
        pygame.display.set_mode(_size(), _WINDOW_OPTS)

def _grid_square_grow():
    '''Increases the grid square size.'''
    global _square_size
    _square_size += 2
    _maybe_resize()

def _grid_square_shrink():
    '''Decreases the grid square size.'''
    global _square_size
    _square_size -= 2
    _maybe_resize()

def _fps_increase():
    '''Increases the FPS.'''
    global _fps
    _fps += 5

def _fps_decrease():
    '''Decreases the FPS.'''
    global _fps
    _fps -= 5
    if _fps < 5:
        _fps = 5

# Mapping of keys to functions
_keybinds = {
    pygame.locals.K_q: _explicit_exit_func,
    #pygame.locals.K_f: toggle_full_screen,
    pygame.locals.K_v: _toggle_show_fps,
    pygame.locals.K_p: toggle_paused,

    pygame.locals.K_ESCAPE: _explicit_exit_func,

    pygame.locals.K_0: _cycle_styles,

    pygame.locals.K_MINUS: _grid_square_shrink,
    pygame.locals.K_EQUALS: _grid_square_grow,

    pygame.locals.K_LEFTBRACKET: _fps_decrease,
    pygame.locals.K_RIGHTBRACKET: _fps_increase
}

def add_keybinding(key, function):
    '''Adds a keybinding'''
    global _keybinds
    _keybinds[key] = function

# This should really be expressable with a lambda, python...
def _noop():
    pass

def _handle_events():
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            _explicit_exit_func()
        elif event.type == pygame.locals.KEYDOWN:
            # Execute the keybinding function, defaulting to a noop method
            _keybinds.get(event.key, _noop)()
    _try_to_flip()
    _clock.tick(_fps)

def _try_to_flip():
    if _video_is_on:
        pygame.display.flip()

def _pause():
    '''\
    Pauses the currently running program. Useful to examine the current state
    of the screen.
    '''
    global _paused
    _debug("::: Pausing")
    _paused = True
    pygame.display.flip()
    while _paused:
        _handle_events()

def _play_pause():
    '''Toggle between paused and unpaused states.'''
    global _paused
    _paused = not _paused


def _check():
    '''\
    Check to see if the user wants to quit.
    That is, if they pressed Q, Esc, or tried to close the window.
    Also checks to see if the user pressed F for fullscreen.
    '''
    _handle_events()
    if _paused:
        _pause()

def _screen():
    return pygame.display.get_surface()

@atexit.register
def _end():
    '''\
    If the user explicitly asks to quit the animation or image, this
    function does nothing and immediately exits. Otherwise, this function
    retains the image on the screen until the user explicitly exits.
    '''
    if _video_is_on and not _explicit_exit:
        _pause()

# TODO XXX FIXME
# Need to make sure primary color lines get drawn last
def _draw_grid_lines():
    '''Draws the grid lines in the window.'''
    for n in xrange(_cols+1):
        p = (_square_size + _style) * n
        _vert_line_at_style(p, _style, True)

    for n in xrange(_rows+1):
        p = (_square_size + _style) * n
        _horz_line_at_style(p, _style, True)

    for n in xrange(_cols+1):
        p = (_square_size + _style) * n
        _vert_line_at_style(p, _style, False)

    for n in xrange(_rows+1):
        p = (_square_size + _style) * n
        _horz_line_at_style(p, _style, False)

def _vert_line_at_style(x, style, want_odd):
    '''Draw a vertical line at x with the given style'''
    for n in xrange(style):
        if n % 2 == 0:
            if not want_odd:
                _line(_primary, (x+n, 0), (x+n, _height-1))
        else:
            if want_odd:
                _line(_secondary, (x+n, 0), (x+n, _height-1))

def _horz_line_at_style(y, style, want_odd):
    '''Draw a horizontal line at x with the given style'''
    for n in xrange(style):
        if n % 2 == 0:
            if not want_odd:
                _line(_primary, (0, y+n), (_width-1, y+n))
        else:
            if want_odd:
                _line(_secondary, (0, y+n), (_width-1, y+n))

### END PRIVATES

def show():
    '''Set up the basic gridpy environment, like the main window.'''
    global _clock
    global _video_is_on
    global _width
    global _height
    pygame.init()
    title(None)
    _calc_size()
    pygame.display.set_mode(_size(), _WINDOW_OPTS)
    pygame.mouse.set_visible(False)
    _draw_grid()
    _clock = pygame.time.Clock()
    _video_is_on = True

def _calc_size():
    '''Recalculates the window size.'''
    global _old_size
    global _width
    global _height
    _old_size = _size()
    _width  = _style + _cols*(_square_size + _style)
    _height = _style + _rows*(_square_size + _style)

def _draw_grid():
    '''Draws the background and the grid.'''
    _fill(_background)
    _draw_grid_lines()

def update():
    '''Update the display and check if the user wants to quit.'''
    global _grid
    _draw_grid()
    for pos, color in _grid.iteritems():
        _plot_no_insert(color, pos)
    pygame.display.flip()
    _check()
    _clock.tick(_fps)
    if _show_fps:
        _debug_noln("> %6.2f FPS\r" % _clock.get_fps())

def _line(color, start, end, width=1):
    '''\
    Draw a line on the screen.
    If width is not given, make it 1px wide.
    '''
    pygame.draw.line(_screen(), color, start, end, width)

def _rectangle(color, rect, width=0, **kwargs):
    '''\
    Draws a rectangle.
    The optional width specifies the outline width. The rectangle is filled
    if this is 0. The keyword args may contain "center", which is a boolean
    that instructs pypixel to use the coordinate specified for the rectangle
    to be the center instead of the top left corner. The rect itself is a pair
    of pairs, specifiying a location and dimensions.
    '''
    rect2 = pygame.Rect(*rect)
    if kwargs.get("center", False):
        rect2.center = rect[0]
    pygame.draw.rect(_screen(), color, rect2, width)

def _square(color, square, width=0, **kwargs):
    '''\
    Draws a square.
    The optional width specifies the outline width. The rectangle is filled
    if this is 0. The keyword args may contain "center", which is a boolean
    that instructs pypixel to use the coordinate specified for the rectangle
    to be the center instead of the top left corner. The rect itself is a pair
    and a number, specifiying a location and width.
    '''
    pos, w = square
    if 0 < w <= 1:
        _pixel(color, pos)
    else:
        _rectangle(color, (pos, (w, w)), width, **kwargs)

_grid = {}

def plot(color, pos):
    '''Plots a square of color color at position pos on the grid.'''
    _plot_no_insert(color, pos)

    _grid[pos] = color

def _plot_no_insert(color, pos):
    '''Plots a square of color color at position pos without touching the grid internal.'''
    col, row = pos
    
    x = _style + (col * (_square_size + _style))
    y = _style + (row * (_square_size + _style))
    pos = (x, y)

    _square(color, (pos, _square_size))

def is_occupied(pos):
    '''Checks to see if position pos is occupied.'''
    global _grid
    return pos in _grid

def _pixel(color, point):
    '''Sets the pixel at the given point to the given color.'''
    _screen().set_at(point, color)

def _fill(color):
    '''Fills the screen with the given color.'''
    _rectangle(color, ((0, 0), _size()))

def clear():
    '''Removes all things from the grid.'''
    global _grid
    _grid = {}

def remove(pos):
    '''Removes the square at position pos from the grid.'''
    global _grid
    # TODO
    # What is going on here? FIXME
    del _grid[pos]

def title(t):
    '''Sets the title of the currently running program.
    Using None, this resets to a default title.'''
    global _program
    if t is not None:
        _program = t
    if _program is None:
        pygame.display.set_caption(_TITLE)
    else:
        pygame.display.set_caption(_program + '   :::   ' + _TITLE)
