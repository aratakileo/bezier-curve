from pygame import display
from math import sqrt
import pygame


def draw_parabola(_surface, _x, _y, _width, _height):
    points = []

    print(_width, _height)
    k = -1 if _height < 0 else 1
    # _width = abs(_width)
    # _height = abs(_height)

    for ix in range(0, _width * 2):
        iy = k * ((ix - _width / 2) / 15) ** 2

        if iy > _height:
            continue

        points += [(_x + ix, _y + iy)]

    print(points)
    if len(points) > 1:
        pygame.draw.lines(_surface, 0xf44336, False, points)

    pygame.draw.line(_surface, 0x4caf50, (_x, _y), (_x + _width, _y + _height))
    pygame.draw.line(_surface, 0x4caf50, (_x + _width / 2, _y), (_x + _width / 2, _y + _height))


pygame.init()
display.set_caption("Graphic value")
display.set_mode((800, 800), pygame.RESIZABLE)

surface = display.get_surface()
clock = pygame.time.Clock()

pos = [0, 200]
point = [400, 400]
point_r = 12
point_click = [False, False]

while True:
    mouse_point = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == pygame.BUTTON_LEFT:
            distance = sqrt((pos[0] + point[0] - mouse_point[0]) ** 2 + (pos[1] + point[1] - mouse_point[1]) ** 2)

            if distance > point_r and not point_click[1]:
                point_click[0] = True

            if distance <= point_r and not point_click[0]:
                point_click[1] = True
        elif e.type == pygame.MOUSEBUTTONUP and e.button == pygame.BUTTON_LEFT:
            point_click = [False, False]

    if point_click[1]:
        point = [mouse_point[0] - pos[0], mouse_point[1] - pos[1]]

    surface.fill(0xffffff)

    draw_parabola(surface, *pos, *point)

    pygame.draw.circle(surface, 0x4caf50, (pos[0] + point[0], pos[1] + point[1]), point_r)

    display.flip()
    clock.tick(60)
