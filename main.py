from pygex.text import bufferize_font, render_text
from pygex.mouse import Mouse
from pygex.input import Input
from pygame import display
from curve import Curve
from grid import Grid
import pygame
import theme


start_pos = end_pos = interact_vertex_index = None
vertexes = []

# Constants
ANCHOR = (800, 800)
RADIUS = 7
WIDTH = 1

# Pygame stuff
display.set_caption("Bezier curve")
display.set_mode(ANCHOR, pygame.RESIZABLE)

surface = display.get_surface()
clock = pygame.time.Clock()

# Pygex stuff
bufferize_font(20)

mouse = Mouse()
input = Input()

# Core stuff
curve = Curve(RADIUS)
grid = Grid(curve, 100, ANCHOR)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

        input.process_event(e)
        mouse.process_event(e)

    grid.prerender()
    curve.prerender()

    # Render
    surface.fill(theme.BG_COLOR)

    grid.render(surface, theme.BG_ACCENT_COLOR, display.get_window_size(), WIDTH, RADIUS)
    curve.render(surface, WIDTH)

    surface.blit(render_text(f'fps: {clock.get_fps():.3f}', theme.TEXT_COLOR), (0, 0))

    display.flip()
    input.flip()
    mouse.flip()
    clock.tick(60)
