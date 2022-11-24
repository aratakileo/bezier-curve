from pygame.constants import K_TAB, K_ESCAPE, K_DELETE, K_BACKSPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.draw import line as draw_line, lines as draw_lines, circle as draw_circle
from pygame.display import get_window_size
from pygex.input import get_input, Input
from pygex.draw import hint as draw_hint
from pygame.surface import SurfaceType
from pygex.math import generate_curve
from pygex.mouse import get_mouse
from typing import Sequence
from grid import get_grid
from math import dist
import theme


class Curve:
    def __init__(self, vertex_radius: float | int):
        self._start_pos = self._end_pos = self._interact_vertex_index = None
        self._need_regenerate_curve = self._vertex_moved = self._new_vertex_quick_move = False
        self._curve_points = []
        self._vertex_radius = vertex_radius

        self.vertexes = []

    def is_not_line(self):
        return len(self.vertexes) > 2

    def is_tip(self, index: int):
        return self.vertexes and (index == 0 or index == len(self.vertexes) - 1)

    def prerender(self):
        mouse_pos = get_grid().to_grid_pos(get_mouse().pos)

        if self.vertexes:
            if get_input().is_applying(K_TAB):
                if self._interact_vertex_index is None or self._interact_vertex_index == len(self.vertexes) - 1:
                    self._interact_vertex_index = 0
                else:
                    self._interact_vertex_index += 1
            elif self._interact_vertex_index is not None:
                get_input().try_start_observing(Input.GK_CTRL)

                if get_input().is_up(K_ESCAPE):
                    self._interact_vertex_index = None
                elif get_input().any_is_up(K_DELETE, K_BACKSPACE):
                    if self.is_tip(self._interact_vertex_index):
                        self.vertexes = []
                        self._curve_points = []
                        self._interact_vertex_index = None
                    else:
                        del self.vertexes[self._interact_vertex_index]
                        self._need_regenerate_curve = True
                elif get_input().any_is_applying(K_LEFT, K_RIGHT, K_UP, K_DOWN, no_reset=True):
                    _x, _y = self.vertexes[self._interact_vertex_index]
                    _step = 10 / get_grid().scale

                    if get_input().is_hold(Input.GK_CTRL):
                        scale_interval = get_grid().scale_interval / get_grid().scale

                        _x = (_x // scale_interval) * scale_interval
                        _y = (_y // scale_interval) * scale_interval

                        _step = scale_interval

                    if get_input().is_applying(K_LEFT):
                        self.vertexes[self._interact_vertex_index] = (_x - _step, _y)
                    elif get_input().is_applying(K_RIGHT):
                        self.vertexes[self._interact_vertex_index] = (_x + _step, _y)
                    elif get_input().is_applying(K_UP):
                        self.vertexes[self._interact_vertex_index] = (_x, _y - _step)
                    elif get_input().is_applying(K_DOWN):
                        self.vertexes[self._interact_vertex_index] = (_x, _y + _step)

                    self._vertex_moved = True

                    if self.is_not_line():
                        self._need_regenerate_curve = True

        if not self.vertexes:
            if get_mouse().left_is_down:
                self._start_pos = mouse_pos
            elif get_mouse().left_is_hold:
                self._end_pos = mouse_pos

            if get_mouse().left_is_up:
                if dist(self._start_pos, self._end_pos) != 0:
                    self.vertexes += fix_vertexes_ends(self._start_pos, self._end_pos, self._vertex_radius * 2)
                    self._interact_vertex_index = 1
                    self._need_regenerate_curve = True

                self._start_pos = self._end_pos = None
        elif get_mouse().left_is_down:
            i = 0
            for vertex in self.vertexes:
                if dist(vertex, mouse_pos) < self._vertex_radius:
                    self._interact_vertex_index = i
                    break

                i += 1
            else:
                if self._interact_vertex_index is not None:
                    self._interact_vertex_index = None
                    return

                nearest_index = 1
                i = 0

                for vertex in self.vertexes:
                    calculated_dist = dist(vertex, mouse_pos)

                    if calculated_dist < self._vertex_radius:
                        break

                    if not self.is_tip(i) and calculated_dist < dist(
                            self.vertexes[nearest_index],
                            mouse_pos
                    ):
                        nearest_index = i

                    i += 1
                else:
                    self.vertexes.insert(nearest_index, mouse_pos)
                    self._need_regenerate_curve = self._new_vertex_quick_move = True
                    self._interact_vertex_index = nearest_index
        elif get_mouse().left_is_hold and self._interact_vertex_index is not None and get_mouse().is_moved:
            self.vertexes[self._interact_vertex_index] = mouse_pos

            if self.is_not_line():
                self._need_regenerate_curve = True
        elif get_mouse().left_is_up and self._interact_vertex_index is not None:
            self._vertex_moved = True

            if self._new_vertex_quick_move:
                self._new_vertex_quick_move = False

        if self._vertex_moved:
            if self.is_tip(self._interact_vertex_index):
                self.vertexes[0], self.vertexes[-1] = fix_vertexes_ends(
                    self.vertexes[0],
                    self.vertexes[-1],
                    self._vertex_radius * 2
                )
            self._vertex_moved = False

        if self._need_regenerate_curve:
            self._curve_points = self.vertexes if len(self.vertexes) <= 2 \
                else generate_curve(self.vertexes, 200, True)
            self._need_regenerate_curve = False

    def render(self, surface: SurfaceType, line_width: int):
        if not self.vertexes and get_mouse().left_is_hold:
            draw_line(
                surface,
                theme.ACCENT_COLOR,
                get_grid().from_grid_pos(self._start_pos),
                get_grid().from_grid_pos(self._end_pos),
                line_width
            )

        render_vertexes = get_grid().from_grid_points(self.vertexes)

        if self._curve_points:
            if self.is_not_line():
                if len(self.vertexes) == 4:
                    draw_line(surface, theme.NOT_ACCENT_COLOR, *render_vertexes[:2], line_width)
                    draw_line(surface, theme.NOT_ACCENT_COLOR, *render_vertexes[2:], line_width)
                else:
                    draw_lines(surface, theme.NOT_ACCENT_COLOR, False, render_vertexes, line_width)

                index = 1
                for vertex in render_vertexes[index:-1]:
                    draw_circle(
                        surface,
                        theme.INTERACTION_COLOR if index == self._interact_vertex_index else theme.NOT_ACCENT_COLOR,
                        vertex,
                        self._vertex_radius,
                        line_width
                    )
                    index += 1

            draw_lines(
                surface,
                theme.ACCENT_COLOR,
                False,
                get_grid().from_grid_points(self._curve_points),
                line_width
            )

            draw_circle(
                surface,
                theme.INTERACTION_COLOR if self._interact_vertex_index == 0
                else theme.ACCENT_COLOR,
                render_vertexes[0],
                self._vertex_radius,
                line_width
            )
            draw_circle(
                surface,
                theme.INTERACTION_COLOR if self._interact_vertex_index == len(self.vertexes) - 1
                else theme.ACCENT_COLOR,
                render_vertexes[-1],
                self._vertex_radius,
                line_width
            )

            if self.is_tip(self._interact_vertex_index):
                x, y = render_vertexes[self._interact_vertex_index]
                draw_hint(
                    surface,
                    f'{get_grid().to_intervalized_x(x):.3f}, {get_grid().to_intervalized_y(y):.3f}',
                    20,
                    (
                        x - self._vertex_radius,
                        y - self._vertex_radius,
                        self._vertex_radius * 2,
                        self._vertex_radius * 2
                    ),
                    (0, 0, *get_window_size()),
                    upper=True,
                    strict_fit_in=True
                )


def fix_vertexes_ends(start_vertex: Sequence, end_vertex: Sequence, min_dist: float | int):
    if dist(start_vertex, end_vertex) < min_dist:
        new_start_vertex, new_end_vertex = [*start_vertex], [*end_vertex]

        if abs(start_vertex[0] - end_vertex[0]) < min_dist:
            if start_vertex[0] <= end_vertex[0]:
                new_end_vertex[0] = start_vertex[0] + min_dist
            else:
                new_start_vertex[0] = end_vertex[0] + min_dist

        return new_start_vertex, new_end_vertex

    return start_vertex, end_vertex


__all__ = 'Curve',
