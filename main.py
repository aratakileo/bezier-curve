from pygame.constants import K_F1, K_F11
from pygex.text import render_text
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

# Pygex stuff
window = Window(ANCHOR, 'Bezier curve', vsync=True)
window.bg_color = theme.BG_COLOR
window.fps_limit = 60

fullscreen_toast = Toast('To exit full screen press [F11]')

# Core stuff
curve = Curve(RADIUS)
grid = Grid(curve, 70, ANCHOR)

while True:
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

        if window.fullscreen:
            fullscreen_toast.show()
        else:
            fullscreen_toast.cancel()

    window.flip()
