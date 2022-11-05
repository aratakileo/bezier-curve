from pygame import color as pygame_color
from typing import Sequence


colorValue = pygame_color.Color | int | str | Sequence


def has_alpha(color: int):
    """

    :param color: alpha format `#ff000000`
    :return:
    """
    return color > 0xffffff


def optimize_alpha_color(color: colorValue):
    """

    :param color: alpha format `#ff000000`
    :return:
    """
    if isinstance(color, int):
        if has_alpha(color):
            return (color & ~0xff000000) << 8 | color >> 24  # converting alpha format from `#ff000000` to `#000000ff`

        return color << 8 | 0xff                             # converting alpha format from `#000000` to `#000000ff`

    return color


__all__ = 'colorValue', 'has_alpha', 'optimize_alpha_color'
