from pygame import display, font, mouse, draw
from curve import generate_curve
from typing import Sequence
from math import dist
import pygame
import theme


def fix_end_vertexes(start_vertex: Sequence, end_vertex: Sequence, min_dist: float | int):
    if dist(start_vertex, end_vertex) < min_dist:
        new_start_vertex, new_end_vertex = [*start_vertex], [*end_vertex]

        if abs(start_vertex[0] - end_vertex[0]) < min_dist:
            if start_vertex[0] <= end_vertex[0]:
                new_end_vertex[0] = start_vertex[0] + min_dist
            else:
                new_start_vertex[0] = end_vertex[0] + min_dist

        return new_start_vertex, new_end_vertex

    return start_vertex, end_vertex


pygame.init()
font.init()

display.set_caption("ibCurves")
display.set_mode((800, 800), pygame.RESIZABLE)

surface = display.get_surface()
clock = pygame.time.Clock()
basefont = font.Font(None, 20)

# Other values
start_pos = end_pos = interact_vertex_index = None
vertexes = []

# Constants
SCALE_INTERVAL = 100
RADIUS = 7
WIDTH = 1

STATUS_NOT_PRESSED = 0
STATUS_DOWN = 1
STATUS_HOLD = 2
STATUS_UP = 3

# Value by constant
mouse_btn_left = STATUS_NOT_PRESSED

while True:
    # Prerender
    mouse_pos = mouse.get_pos()
    win_size = display.get_window_size()

    if mouse_btn_left == STATUS_DOWN:
        mouse_btn_left = STATUS_HOLD
    elif mouse_btn_left == STATUS_UP:
        mouse_btn_left = STATUS_NOT_PRESSED

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == pygame.BUTTON_LEFT:
            mouse_btn_left = STATUS_DOWN
        elif e.type == pygame.MOUSEBUTTONUP and e.button == pygame.BUTTON_LEFT:
            mouse_btn_left = STATUS_UP

    # Render
    surface.fill(theme.BG_COLOR)

    for y in range(1, win_size[0] // SCALE_INTERVAL):
        draw.line(surface, theme.BG_ACCENT_COLOR, (y * SCALE_INTERVAL, 0), (y * SCALE_INTERVAL, win_size[1]))

    for y in range(1, win_size[1] // SCALE_INTERVAL):
        draw.line(surface, theme.BG_ACCENT_COLOR, (0, y * SCALE_INTERVAL), (win_size[0], y * SCALE_INTERVAL))

    if not vertexes:
        if mouse_btn_left == STATUS_DOWN:
            start_pos = mouse_pos
        elif mouse_btn_left == STATUS_HOLD:
            end_pos = mouse_pos

        if mouse_btn_left == STATUS_HOLD:
            draw.line(surface, theme.ACCENT_COLOR, start_pos, end_pos)

        if mouse_btn_left == STATUS_UP:
            if dist(start_pos, end_pos) != 0:
                vertexes += fix_end_vertexes(start_pos, end_pos, RADIUS * 2)

            start_pos = end_pos = None
    elif mouse_btn_left == STATUS_DOWN:
        if interact_vertex_index is None:
            index = 0

            for vertex in vertexes:
                if dist(vertex, mouse_pos) < RADIUS:
                    interact_vertex_index = index
                    break

                index += 1
    elif mouse_btn_left == STATUS_HOLD and interact_vertex_index is not None:
        vertexes[interact_vertex_index] = mouse_pos
    elif mouse_btn_left == STATUS_UP:
        if interact_vertex_index is None:
            nearest_index = -1  # in that case -1 means 1 from the end, not invalid index
            index = 0

            for vertex in vertexes:
                calculated_dist = dist(vertex, mouse_pos)

                if dist(vertex, mouse_pos) < RADIUS:
                    break

                if index != 0 and index != len(vertexes) - 1 and calculated_dist < dist(vertexes[nearest_index], mouse_pos):
                    nearest_index = index

                index += 1
            else:
                vertexes.insert(nearest_index, mouse_pos)
        else:
            vertexes[0], vertexes[-1] = fix_end_vertexes(vertexes[0], vertexes[-1], RADIUS * 2)

        interact_vertex_index = None

    curve_points = vertexes if len(vertexes) <= 2 else generate_curve(vertexes, 300)

    if curve_points:
        if len(vertexes) > 2:
            if len(vertexes) == 4:
                draw.lines(surface, theme.NOT_ACCENT_COLOR, False, vertexes[:2], WIDTH)
                draw.lines(surface, theme.NOT_ACCENT_COLOR, False, vertexes[2:], WIDTH)
            else:
                draw.lines(surface, theme.NOT_ACCENT_COLOR, False, vertexes, WIDTH)

            index = 1
            for vertex in vertexes[index:-1]:
                draw.circle(
                    surface,
                    theme.INTERACTION_COLOR if index == interact_vertex_index else theme.NOT_ACCENT_COLOR,
                    vertex,
                    RADIUS,
                    WIDTH
                )
                index += 1

        draw.lines(surface, theme.ACCENT_COLOR, False, (vertexes[0], *curve_points, vertexes[-1]), WIDTH)

        draw.circle(
            surface,
            theme.INTERACTION_COLOR if interact_vertex_index == 0
            else theme.ACCENT_COLOR,
            vertexes[0],
            RADIUS,
            WIDTH
        )
        draw.circle(
            surface,
            theme.INTERACTION_COLOR if interact_vertex_index == len(vertexes) - 1
            else theme.ACCENT_COLOR,
            vertexes[-1],
            RADIUS,
            WIDTH
        )

    display.flip()
    clock.tick(60)
