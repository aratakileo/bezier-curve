from pygame.event import EventType
from pygame.rect import RectType
from pygame import mouse


class Button:
    rect: RectType

    def __init__(self, _rect: RectType):
        self.rect = _rect
        self._strict_focused = True

    def __prerender(self, _event: EventType):
        pass

    def is_focused(self):
        return self._strict_focused and self.rect.collidepoint(*mouse.get_pos())


__all__ = (
    'Button',
)
