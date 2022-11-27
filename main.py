from pygex.text import bufferize_font, render_text
from pygame.event import get as get_event
from pygame.constants import K_F1, K_F11
from pygex import Window
from curve import Curve
from grid import Grid
import theme


start_pos = end_pos = interact_vertex_index = None
vertexes = []

# Constants
ANCHOR = (800, 800)
RADIUS = 7
WIDTH = 1

# Pygex stuff
window = Window(ANCHOR, 'Bezier curve', vsync=True)
window.bg_color = theme.BG_COLOR
window.fps_limit = 60

bufferize_font(20)

# Core stuff
curve = Curve(RADIUS)
grid = Grid(curve, 70, ANCHOR)

while True:
    for e in get_event():
        window.process_event(e)

    grid.prerender()
    curve.prerender()

    grid.render(
        window.surface,
        theme.BG_ACCENT_COLOR,
        theme.BG_NOT_ACCENT_COLOR,
        window.size,
        WIDTH,
        RADIUS
    )
    curve.render(window.surface, WIDTH)

    window.surface.blit(render_text(f'fps: {window.fps:.3f}', theme.TEXT_COLOR), (0, 0))

    if window.input.is_up(K_F1):
        window.take_screenshot()
    elif window.input.is_up(K_F11):
        window.fullscreen = not window.fullscreen

    window.flip()
