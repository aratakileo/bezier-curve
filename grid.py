from pygex.text import render_text, get_buffered_font
from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN
from pygame.draw import line as draw_line
from pygex.input import get_input, Input
from pygame.surface import SurfaceType
from pygex.color import colorValue
from pygex.mouse import get_mouse
from typing import Sequence
from math import ceil


class Grid:
    def __init__(self, curve, scale_interval: float | int, anchor: Sequence):
        global _active_grid
        _active_grid = self

        self._anchor = anchor
        self._curve = curve

        self.scale_interval = scale_interval
        self.pos = [0, 0]

    def to_intervalized_x(self, x: float | int):
        return (self.pos[0] + x) / self.scale_interval - 1

    def to_intervalized_y(self, y: float | int):
        return (self._anchor[1] - self.pos[1] - y) / self.scale_interval - 1

    def to_intervalized_pos(self, pos: Sequence):
        return self.to_intervalized_x(pos[0]), self.to_intervalized_y(pos[1])

    def to_grid_x(self, x: float | int):
        return self.pos[0] + x

    def to_grid_y(self, y: float | int):
        return self.pos[1] + y

    def to_grid_pos(self, pos: Sequence):
        return self.to_grid_x(pos[0]), self.to_grid_y(pos[1])

    def from_grid_x(self, x: float | int):
        return x - self.pos[0]

    def from_grid_y(self, y: float | int):
        return y - self.pos[1]

    def from_grid_pos(self, pos: Sequence):
        return self.from_grid_x(pos[0]), self.from_grid_y(pos[1])

    def from_grid_points(self, points: Sequence):
        new_points = ()

        for point in points:
            new_points = *new_points, self.from_grid_pos(point)

        return new_points

    def prerender(self):
        if get_mouse().middle_is_hold and get_mouse().is_moved:
            self.pos[0] += get_mouse().rel[0]
            self.pos[1] += get_mouse().rel[1]

        if self._curve._interact_vertex_index is None and get_input().any_is_applying(
                K_LEFT, K_RIGHT, K_UP, K_DOWN, no_reset=True
        ):
                _x, _y = self.pos
                _step = 10

                if get_input().is_hold(Input.GK_CTRL):
                    scale_interval = get_grid().scale_interval

                    _x = (_x // scale_interval) * scale_interval
                    _y = (_y // scale_interval) * scale_interval

                    _step = scale_interval

                if get_input().is_applying(K_LEFT):
                    self.pos = [_x - _step, _y]
                elif get_input().is_applying(K_RIGHT):
                    self.pos = [_x + _step, _y]
                elif get_input().is_applying(K_UP):
                    self.pos = [_x, _y - _step]
                elif get_input().is_applying(K_DOWN):
                    self.pos = [_x, _y + _step]

    def render(
            self,
            surface: SurfaceType,
            color: colorValue,
            size: Sequence,
            line_width: int,
            text_margin: float | int
    ):
        intervalized_start_x = ceil(self.pos[0] / self.scale_interval)

        # Draw vertical lines
        for step in range(intervalized_start_x, ceil(size[0] / self.scale_interval) + intervalized_start_x + 1):
            x = step * self.scale_interval - self.pos[0]

            text = float(step - 1).__str__()
            text_size = get_buffered_font().size(text)
            text_pos = (x - text_size[0] - text_margin, size[1] - text_size[1])

            draw_line(surface, color, (x, 0), (x, size[1]), line_width)

            surface.blit(render_text(text, color), text_pos)

        intervalized_start_y = ceil(self.pos[1] / self.scale_interval)

        # Draw horizontal lines
        for step in range(intervalized_start_y, ceil(size[1] / self.scale_interval) + intervalized_start_y + 1):
            y = step * self.scale_interval - self.pos[1]

            text = float(ceil(self._anchor[1] / self.scale_interval) - step - 1).__str__()
            text_height = get_buffered_font().get_height()
            text_pos = (text_margin, y - text_height - text_margin)

            draw_line(surface, color, (0, y), (size[0], y), line_width)

            surface.blit(render_text(text, color), text_pos)


_active_grid: Grid | None = None


def get_grid():
    return _active_grid


__all__ = 'Grid', 'get_grid'
