from text import render_base_text, get_buffered_font
from pygame.draw import line as draw_line
from pygame.surface import SurfaceType
from color import colorValue
from typing import Sequence
from math import ceil


class Grid:
    def __init__(self, scale_interval: float | int, anchor: Sequence):
        self.scale_interval = scale_interval
        self.anchor = anchor

    def to_grid_x(self, x: float | int):
        return x / self.scale_interval - 1

    def to_grid_y(self, y: float | int):
        return (self.anchor[1] - y) / self.scale_interval - 1

    def to_grid_pos(self, pos: Sequence):
        return self.to_grid_x(pos[0]), self.to_grid_y(pos[1])

    def render(
            self,
            surface: SurfaceType,
            color: colorValue,
            size: Sequence,
            line_width: int,
            text_margin: float | int
    ):
        # Draw vertical lines
        for step in range(1, ceil(size[0] / self.scale_interval) + 1):
            x = step * self.scale_interval
            y = size[1]

            text = float(step - 1).__str__()
            text_size = get_buffered_font().size(text)
            text_pos = (x - text_size[0] - text_margin, y - text_size[1])

            draw_line(surface, color, (x, 0), (x, y), line_width)

            render_base_text(surface, text, color, text_pos)

        # Draw horizontal lines
        for step in range(1, ceil(size[1] / self.scale_interval) + 1):
            y = step * self.scale_interval

            text = float(ceil(self.anchor[1] / self.scale_interval) - step - 1).__str__()
            text_height = get_buffered_font().get_height()
            text_pos = (text_margin, y - text_height - text_margin)

            draw_line(surface, color, (0, y), (size[0], y), line_width)

            render_base_text(surface, text, color, text_pos)


__all__ = 'Grid',
