from .text import render_base_text, get_buffered_font
from pygame.draw import line as draw_line
from pygame.surface import SurfaceType
from color import colorValue
from typing import Sequence
from math import ceil


def grid(
        surface: SurfaceType,
        color: colorValue,
        anchor: Sequence,
        size: Sequence,
        scale_interval: float | int,
        text_margin: float | int
):
    for _x in range(1, ceil(size[0] / scale_interval) + 1):
        x = _x * scale_interval
        y = size[1]
        draw_line(surface, color, (x, 0), (x, y))

        text = float(_x - 1).__str__()
        font_size = get_buffered_font().size(text)

        render_base_text(
            surface,
            text,
            color,
            (x - font_size[0] - text_margin, y - font_size[1])
        )

    for _y in range(1, ceil(size[1] / scale_interval) + 1):
        y = _y * scale_interval
        draw_line(surface, color, (0, y), (size[0], y))

        font = get_buffered_font()

        render_base_text(
            surface,
            float(-_y + ceil(anchor[1] / scale_interval) - 1).__str__(),
            color,
            (text_margin, y - font.get_height() - text_margin)
        )


__all__ = 'grid',
