from pygex.text import bufferize_font, render_text
from pygame.event import get as get_event
from pygame.constants import RESIZABLE
from pygame import display
from curve import Curve
from grid import Grid
from pygex import *
import theme


start_pos = end_pos = interact_vertex_index = None
vertexes = []

# Constants
ANCHOR = (800, 800)
RADIUS = 7
WIDTH = 1

# Pygame stuff
display.set_caption("Bezier curve")
display.set_mode(ANCHOR, RESIZABLE)

surface = display.get_surface()

# Pygex stuff
bufferize_font(20)

# Core stuff
curve = Curve(RADIUS)
grid = Grid(curve, 70, ANCHOR)

while True:
    for e in get_event():
        process_event(e)

    grid.prerender()
    curve.prerender()

    # Render
    grid.render(surface, theme.BG_ACCENT_COLOR, theme.BG_NOT_ACCENT_COLOR, display.get_window_size(), WIDTH, RADIUS)
    curve.render(surface, WIDTH)

    surface.blit(render_text(f'fps: {get_clock().get_fps():.3f}', theme.TEXT_COLOR), (0, 0))

    flip(theme.BG_COLOR, 60)
