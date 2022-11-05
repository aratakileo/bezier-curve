from render.text import bufferize_font
from pygame import display
from render import render
from mouse import Mouse
from curve import Curve
import pygame
import theme


start_pos = end_pos = interact_vertex_index = None
vertexes = []

# Constants
ANCHOR = (800, 800)
SCALE_INTERVAL = 100
RADIUS = 7
WIDTH = 1

# Pygame stuff
pygame.init()

display.set_caption("Bezier curve")
display.set_mode(ANCHOR, pygame.RESIZABLE)

surface = display.get_surface()
clock = pygame.time.Clock()

bufferize_font(22)

mouse = Mouse()
curve = Curve(mouse)

while True:
    # Prerender
    mouse.prerender()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

        mouse.event(e)
        curve.event(e, SCALE_INTERVAL)

    curve.prerender(RADIUS * 2)

    # Render
    surface.fill(theme.BG_COLOR)

    render.grid(surface, theme.BG_ACCENT_COLOR, ANCHOR, display.get_window_size(), SCALE_INTERVAL, RADIUS)
    curve.render(surface, WIDTH, RADIUS)

    display.flip()
    clock.tick(60)
