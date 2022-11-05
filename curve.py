from pygame import (
    KEYDOWN, KEYUP, K_TAB, K_ESCAPE, K_DELETE, K_BACKSPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_LCTRL, K_RCTRL
)
from pygame.draw import line as draw_line, lines as draw_lines, circle as draw_circle
from pygame.surface import SurfaceType
from pygame.event import Event
from typing import Sequence
from mouse import Mouse
from math import dist
import theme


class Curve:
    def __init__(self, mouse: Mouse):
        self._start_pos = self._end_pos = self._interact_vertex_index = None
        self._need_regenerate_curve = self._ctrl_hold = False
        self._curve_points = []
        self._mouse = mouse

        self.vertexes = []

    def event(self, e: Event, scale_interval: float | int, step: float | int = 10):
        if e.type == KEYDOWN and e.key in (K_LCTRL, K_RCTRL):
            self._ctrl_hold = True
            return

        if e.type == KEYUP:
            if e.key in (K_LCTRL, K_RCTRL):
                self._ctrl_hold = False
                return

            if e.key == K_TAB and self.vertexes:
                if self._interact_vertex_index is None or self._interact_vertex_index == len(self.vertexes) - 1:
                    self._interact_vertex_index = 0
                    return

                self._interact_vertex_index += 1
                return

            if self._interact_vertex_index is not None:
                if e.key in (K_DELETE, K_BACKSPACE) and self.vertexes:
                    if self._interact_vertex_index == 0 or self._interact_vertex_index == len(self.vertexes) - 1:
                        self.vertexes = []
                        self._curve_points = []
                        self._interact_vertex_index = None
                        return

                    del self.vertexes[self._interact_vertex_index]
                    self._need_regenerate_curve = True
                    return

                _x, _y = self.vertexes[self._interact_vertex_index]
                _step = step

                if self._ctrl_hold:
                    _x = (_x // scale_interval) * scale_interval
                    _y = (_y // scale_interval) * scale_interval
                    _step = scale_interval

                if e.key == K_LEFT:
                    self.vertexes[self._interact_vertex_index] = (_x - _step, _y)
                    return

                if e.key == K_RIGHT:
                    self.vertexes[self._interact_vertex_index] = (_x + _step, _y)
                    return

                if e.key == K_UP:
                    self.vertexes[self._interact_vertex_index] = (_x, _y - _step)
                    return

                if e.key == K_DOWN:
                    self.vertexes[self._interact_vertex_index] = (_x, _y + _step)
                    return

            if e.key == K_ESCAPE:
                self._interact_vertex_index = None
                return

    def prerender(self, min_dist: float | int):
        mouse_pos = self._mouse.get_pos()

        if not self.vertexes:
            if self._mouse.left_btn == Mouse.BUTTON_DOWN:
                self._start_pos = mouse_pos
            elif self._mouse.left_btn == Mouse.BUTTON_HOLD:
                self._end_pos = mouse_pos

            if self._mouse.left_btn == Mouse.BUTTON_UP:
                if dist(self._start_pos, self._end_pos) != 0:
                    self.vertexes += fix_end_vertexes(self._start_pos, self._end_pos, min_dist)
                    self._interact_vertex_index = 1
                    self._need_regenerate_curve = True

                self._start_pos = self._end_pos = None
        elif self._mouse.left_btn == Mouse.BUTTON_DOWN:
            i = 0
            for vertex in self.vertexes:
                if dist(vertex, mouse_pos) < min_dist / 2:
                    self._interact_vertex_index = i
                    break

                i += 1
            else:
                if self._interact_vertex_index is not None:
                    self._interact_vertex_index = None
                    return

                nearest_index = -1  # in that case -1 means 1 from the end, not invalid index
                i = 0

                for vertex in self.vertexes:
                    calculated_dist = dist(vertex, mouse_pos)

                    if calculated_dist < min_dist / 2:
                        break

                    if i != 0 and i != len(self.vertexes) - 1 and calculated_dist < dist(self.vertexes[nearest_index], mouse_pos):
                        nearest_index = i

                    i += 1
                else:
                    self.vertexes.insert(nearest_index, mouse_pos)
                    self._need_regenerate_curve = True
        elif self._mouse.left_btn == Mouse.BUTTON_HOLD and self._interact_vertex_index is not None \
                and self._mouse.get_rel() != (0, 0):
            self.vertexes[self._interact_vertex_index] = mouse_pos

            if len(self.vertexes) > 2:
                self._need_regenerate_curve = True
        elif self._mouse.left_btn == Mouse.BUTTON_UP:
            self.vertexes[0], self.vertexes[-1] = fix_end_vertexes(self.vertexes[0], self.vertexes[-1], min_dist)

        if self._need_regenerate_curve:
            self._curve_points = self.vertexes if len(self.vertexes) <= 2 else generate_curve(self.vertexes, 200)
            self._need_regenerate_curve = False

    def render(self, surface: SurfaceType, width: int, radius: float | int):
        if not self.vertexes and self._mouse.left_btn == Mouse.BUTTON_HOLD:
            draw_line(surface, theme.ACCENT_COLOR, self._start_pos, self._end_pos, width)

        if self._curve_points:
            if len(self.vertexes) > 2:
                if len(self.vertexes) == 4:
                    draw_line(surface, theme.NOT_ACCENT_COLOR, *self.vertexes[:2], width)
                    draw_line(surface, theme.NOT_ACCENT_COLOR, *self.vertexes[2:], width)
                else:
                    draw_lines(surface, theme.NOT_ACCENT_COLOR, False, self.vertexes, width)

                index = 1
                for vertex in self.vertexes[index:-1]:
                    draw_circle(
                        surface,
                        theme.INTERACTION_COLOR if index == self._interact_vertex_index else theme.NOT_ACCENT_COLOR,
                        vertex,
                        radius,
                        width
                    )
                    index += 1

            draw_lines(
                surface,
                theme.ACCENT_COLOR,
                False,
                (self.vertexes[0], *self._curve_points, self.vertexes[-1]),
                width
            )

            draw_circle(
                surface,
                theme.INTERACTION_COLOR if self._interact_vertex_index == 0
                else theme.ACCENT_COLOR,
                self.vertexes[0],
                radius,
                width
            )
            draw_circle(
                surface,
                theme.INTERACTION_COLOR if self._interact_vertex_index == len(self.vertexes) - 1
                else theme.ACCENT_COLOR,
                self.vertexes[-1],
                radius,
                width
            )


def interpolate(p1: Sequence, p2: Sequence, t: float):
    return [(1 - t) * p1[i] + t * p2[i] for i in range(2)]


def get_curve_point(vertexes: Sequence, r: int, i: int, t: float):
    if r == 0:
        return vertexes[i]

    return interpolate(get_curve_point(vertexes, r - 1, i, t), get_curve_point(vertexes, r - 1, i + 1, t), t)


def generate_curve(vertexes: Sequence, density=100):
    points = []

    if len(vertexes) <= 1:
        return points

    for i in range(density):
        points.append(get_curve_point(vertexes, len(vertexes) - 1, 0, i / density))

    return points


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


__all__ = 'Curve', 'interpolate', 'get_curve_point', 'generate_curve', 'fix_end_vertexes'
