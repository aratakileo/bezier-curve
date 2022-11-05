from pygame import display, font, mouse
from math import sqrt
import pygame

import generator

pygame.init()
font.init()

display.set_caption("ibCurves")
display.set_mode((800, 800), pygame.RESIZABLE)

surface = display.get_surface()
clock = pygame.time.Clock()
basefont = font.Font(None, 20)

is_pressed = False
start, stop = 0, 113

colors = (0xf44336, 0x3f51b5, 0xffc107)
is_num_pressed = [False, False, False]
coefficients = [(2.1, 0.15), (None, None), (2.1, 0.15)]

vertexes = [(0, 0), (0, 200), (350, 900), (600, 100), (600, 700)]

while True:
    mouse_pos = mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == pygame.BUTTON_MIDDLE:
            is_pressed = True
        elif e.type == pygame.MOUSEBUTTONUP and e.button == pygame.BUTTON_MIDDLE:
            is_pressed = False

            if True in is_num_pressed:
                print(mouse_pos)
        elif e.type == pygame.KEYDOWN:
            is_num_pressed = [e.key == key for key in (pygame.K_1, pygame.K_2, pygame.K_3)]
        elif e.type == pygame.KEYUP:
            # if e.key == pygame.K_F1:
            #     kx, ky = float(input('kx = ')), float(input('ky = '))
            if True in [e.key == key for key in (pygame.K_1, pygame.K_2, pygame.K_3)]:
                is_num_pressed = [False, False, False]

    if is_pressed:
        if True not in is_num_pressed:
            coefficients[0] = coefficients[2] = mouse_pos[0] / stop, sqrt(mouse_pos[1]) / stop
            coefficients[1] = sqrt(mouse_pos[0]) / stop, mouse_pos[1] / stop
        else:
            index = is_num_pressed.index(True)

            coefficients[index] = (
                mouse_pos[0] / stop, sqrt(mouse_pos[1]) / stop
            ) if index in (0, 2) else (
                sqrt(mouse_pos[0]) / stop, mouse_pos[1] / stop
            )

    point_groups = [[], [], []]
    super_points = []

    for k in range(start, stop + 1):
        kx, ky = coefficients[0]
        point_groups[0].append((k * kx, (k * ky) ** 2))
        if k < stop / 1.2555 and k % 2 == 0:
            super_points.append((k * kx / 2, (k * ky) ** 2))

    right_bottom = point_groups[0][-1]

    if coefficients[1][0] is None:
        coefficients[1] = sqrt(right_bottom[0]) / stop, right_bottom[1] / stop

    for k in range(start, stop + 1):
        point_groups[1].append(((k * coefficients[1][0]) ** 2, k * coefficients[1][1]))

    points = []

    for k in range(start, stop + 1):
        points.append((k * coefficients[2][0], (k * coefficients[2][1]) ** 2))

    for point in points[::-1]:
        point_groups[2].append((points[-1][-2] - point[0], points[-1][-1] - point[1]))

    surface.fill(0xffffff)

    # pygame.draw.line(surface, 0x4caf50, (0, right_bottom[-1]), right_bottom, 3)
    # pygame.draw.line(surface, 0x4caf50, (right_bottom[-2], 0), right_bottom, 3)
    # pygame.draw.line(surface, 0x4caf50, (0, 0), right_bottom, 3)
    #
    # text_lines = 0
    # for i in range(len(colors)):
    #     pygame.draw.lines(surface, colors[i], False, point_groups[i], 3)
    #
    #     surface.blit(basefont.render(f'pos({i}): {point_groups[i][-1]}', True, 0x000000), (right_bottom[-2], right_bottom[-1] + basefont.get_height() * text_lines))
    #     text_lines += 1
    #
    #     surface.blit(basefont.render(f'coef({i}): {coefficients[i]}', True, 0x000000), (right_bottom[-2], right_bottom[-1] + basefont.get_height() * text_lines))
    #     text_lines += 1

    # pygame.draw.lines(surface, 0x795548, False, super_points, 3)

    pygame.draw.lines(surface, 0x4caf50, False, generator.generate_curve(vertexes, 300), 5)

    for vertex in vertexes:
        pygame.draw.circle(surface, 0xffc107, vertex, 10)

    display.flip()
    clock.tick(60)
