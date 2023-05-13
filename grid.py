from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN
from pygex.broker import get_input, get_mouse, get_window
from pygex.text import render_text, get_pygame_font
from pygex.interface import Flippable, Renderable
from pygex.draw import grid as draw_grid
from pygame.surface import SurfaceType
from pygex.mouse import F_NO_BORDERS
from pygex.color import TYPE_COLOR
from pygex.input import GK_CTRL
from typing import Sequence
from math import ceil


class Grid(Flippable, Renderable):
    def __init__(
            self,
            curve,
            scale_interval: float | int,
            anchor: Sequence,
            color: TYPE_COLOR,
            subcolor: TYPE_COLOR,
            line_width: int,
            text_margin: int
    ):
        global _active_grid
        _active_grid = self

        self._anchor = anchor
        self._curve = curve

        self.scale_interval = scale_interval
        self.pos = [0, 0]
        self.scale = 10.0
        self.scaling_density = 10
        self.color, self.subcolor = color, subcolor
        self.line_width, self.text_margin = line_width, text_margin

    def to_intervalized_x(self, x: float | int):
        return (self.pos[0] + x) * 10 / self.scale_interval / self.scale - 1

    def to_intervalized_y(self, y: float | int):
        return self._anchor[1] / self.scale_interval - (self.pos[1] + y) * 10 / self.scale_interval / self.scale

    def to_intervalized_pos(self, pos: Sequence):
        return self.to_intervalized_x(pos[0]), self.to_intervalized_y(pos[1])

    def to_grid_x(self, x: float | int):
        return (self.pos[0] + x) / self.scale

    def to_grid_y(self, y: float | int):
        return (self.pos[1] + y) / self.scale

    def to_grid_pos(self, pos: Sequence):
        return self.to_grid_x(pos[0]), self.to_grid_y(pos[1])

    def from_grid_x(self, x: float | int):
        return x * self.scale - self.pos[0]

    def from_grid_y(self, y: float | int):
        return y * self.scale - self.pos[1]

    def from_grid_pos(self, pos: Sequence):
        return self.from_grid_x(pos[0]), self.from_grid_y(pos[1])

    def from_grid_points(self, points: Sequence):
        new_points = ()

        for point in points:
            new_points = *new_points, self.from_grid_pos(point)

        return new_points

    def flip(self):
        if get_mouse().is_wheel:
            new_scale = round(self.scale + get_mouse().wheel[1] / self.scaling_density, self.scaling_density)
            self.scale = self.scale if new_scale < 1 or new_scale > 20 else new_scale

        get_mouse().remove_flags(F_NO_BORDERS)

        if get_mouse().right_is_hold and get_mouse().is_moved:
            self.pos[0] += get_mouse().relx
            self.pos[1] += get_mouse().rely

            get_mouse().add_flags(F_NO_BORDERS)

        if self._curve._interact_vertex_index is None and get_input().any_is_applying(
                K_LEFT, K_RIGHT, K_UP, K_DOWN, reset_data=False
        ):
                _x, _y = self.pos
                _step = 10

                if get_input().is_hold(GK_CTRL):
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

    def render(self, surface: SurfaceType):
        window = get_window()

        int_scale = int(self.scale)

        lim_scale = self.scale if self.scale < 2 else round(self.scale - int_scale + 1, self.scaling_density)
        lim_scaled_interval = self.scale_interval * lim_scale

        scaled_interval = self.scale_interval * self.scale

        x_step_off = (int(self.pos[0] / lim_scaled_interval) - self.pos[0] / lim_scaled_interval)
        y_step_off = (int(self.pos[1] / lim_scaled_interval) - self.pos[1] / lim_scaled_interval)

        x_poses = [
            (x_step - 1) * 10 / int_scale for x_step in range(
                ceil(self.pos[0] * 10 / scaled_interval),
                ceil((self.pos[0] + window.width) * 10 / scaled_interval) + 2
            )
        ]

        y_poses = [
            (self._anchor[1] * 10 / scaled_interval - y_step) * 10 / self.scale for y_step in range(
                ceil(self.pos[1] * 10 / scaled_interval),
                ceil((self.pos[1] + window.height) * 10 / scaled_interval) + 2
            )
        ]

        if lim_scale >= 1.5:
            draw_grid(
                surface,
                self.subcolor,
                lim_scaled_interval,
                (0, 0, *window.size),
                (self.pos[0] - lim_scaled_interval / 4, self.pos[1] - lim_scaled_interval / 4),
                self.line_width
            )
            draw_grid(
                surface,
                self.subcolor,
                lim_scaled_interval,
                (0, 0, *window.size),
                (self.pos[0] + lim_scaled_interval / 4, self.pos[1] + lim_scaled_interval / 4),
                self.line_width
            )

        draw_grid(
            surface,
            self.subcolor,
            lim_scaled_interval,
            (0, 0, *window.size),
            (self.pos[0] - lim_scaled_interval / 2, self.pos[1] - lim_scaled_interval / 2),
            self.line_width
        )

        draw_grid(
            surface,
            self.color,
            lim_scaled_interval,
            (0, 0, *window.size),
            self.pos,
            self.line_width
        )

        i = 0
        for x_step in range(-(self.pos[0] < 0), ceil(window.size[0] / lim_scaled_interval) + (self.pos[0] >= 0)):
            x = (x_step_off + x_step) * lim_scaled_interval

            if i < len(x_poses) and x >= 0:
                text = f'{x_poses[i]:.1f}'
                text_size = get_pygame_font().size(text)
                text_pos = (x - text_size[0] - self.text_margin, window.height - text_size[1])

                surface.blit(render_text(text, self.color), text_pos)

                i += 1

        i = 0
        for y_step in range(-(self.pos[1] < 0), ceil(window.height / lim_scaled_interval) + (self.pos[1] >= 0)):
            y = (y_step_off + y_step) * lim_scaled_interval

            if i < len(y_poses) and y >= 0:
                text = f'{y_poses[i]:.1f}'
                text_size = get_pygame_font().size(text)
                text_pos = (self.text_margin, y - text_size[1] - self.text_margin)

                surface.blit(render_text(text, self.color), text_pos)

                i += 1


_active_grid: Grid | None = None


def get_grid():
    return _active_grid


__all__ = 'Grid', 'get_grid'
