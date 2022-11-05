from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.mouse import get_pos, get_rel
from pygame.event import Event


class Mouse:
    BUTTON_NOT_PRESSED = 0
    BUTTON_DOWN = 1
    BUTTON_HOLD = 2
    BUTTON_UP = 3

    def __init__(self):
        self.button_statuses = [Mouse.BUTTON_NOT_PRESSED] * 3
        self.get_pos = get_pos
        self.get_rel = get_rel

    @property
    def left_btn(self):
        return self.button_statuses[0]

    @property
    def middle_btn(self):
        return self.button_statuses[1]

    @property
    def right_btn(self):
        return self.button_statuses[2]

    def event(self, e: Event):
        event_types = (MOUSEBUTTONDOWN, MOUSEBUTTONUP)
        statuses = (Mouse.BUTTON_DOWN, Mouse.BUTTON_UP)

        for i in range(2):
            if e.type == event_types[i]:
                for k in range(len(self.button_statuses)):
                    if e.button == k + 1:
                        self.button_statuses[k] = statuses[i]

    def prerender(self):
        for i in range(len(self.button_statuses)):
            if self.button_statuses[i] == Mouse.BUTTON_DOWN:
                self.button_statuses[i] = Mouse.BUTTON_HOLD
            elif self.button_statuses[i] == Mouse.BUTTON_UP:
                self.button_statuses[i] = Mouse.BUTTON_NOT_PRESSED


__all__ = 'Mouse',
