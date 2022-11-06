from pygame.font import FontType, get_init, init, Font
from color import colorValue, optimize_alpha_color
from pygame.surface import SurfaceType
from typing import Sequence


_buffered_font: FontType | None = None
_buffered_font_size = -1


def render_base_text(
        surface: SurfaceType,
        text,
        alpha_color: colorValue,
        pos: Sequence,
        font_or_size: FontType | int = None,
        antialias=True
):
    if not get_init():
        init()

    font = font_or_size

    if isinstance(font_or_size, int):
        bufferize_font(font_or_size)

        font = _buffered_font
    elif font_or_size is None:
        if _buffered_font is None:
            bufferize_font(12)

        font = _buffered_font

    surface.blit(font.render(text, antialias, optimize_alpha_color(alpha_color)), pos)


def bufferize_font(size: int):
    if not get_init():
        init()

    global _buffered_font, _buffered_font_size

    if _buffered_font_size != size:
        _buffered_font_size = size
        _buffered_font = Font(None, size)


def get_buffered_font():
    return _buffered_font


__all__ = 'render_base_text', 'bufferize_font', 'get_buffered_font'
