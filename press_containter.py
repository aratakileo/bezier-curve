from pygame.event import EventType


class PressContainer:
    def __init__(self):
        self._views = set()
        self._interaction_view = None
        self._miss_clicked = False

    def iterate(self, _event: EventType):
        for view in self._views:
            if self._interaction_view is None or self._interaction_view == view:
                view._strict_focused = True
                continue

            view._strict_focused = False

    def add_view(self, view):
        self._views.add(view)

    def remove_view(self, view):
        if view in self._views:
            self._views.remove(view)

