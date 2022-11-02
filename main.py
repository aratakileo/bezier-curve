from arcade import gui
import arcade as arc


class Window(arc.Window):
    def __init__(self):
        super().__init__(800, 800, 'Graphic value', resizable=True)
        self.background_color = arc.color.WHITE
        self.button = gui.UIFlatButton(text="Test", width=200)

        self.ui_manager = gui.UIManager()
        self.ui_manager.enable()
        self.ui_manager.add(
            gui.UIAnchorWidget(
                anchor_x='center_x',
                anchor_y='center_y',
                child=self.button
            )
        )

    def on_draw(self):
        arc.start_render()
        arc.draw_circle_outline(*self.get_center(), 400, arc.color.RED, num_segments=1000)
        self.ui_manager.draw()

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        def on_event(event):
            print(event)

        self.button.on_event = on_event

    def get_center_x(self):
        return self._width / 2

    def get_center_y(self):
        return self._height / 2

    def get_center(self):
        return self.get_center_x(), self.get_center_y()


app = Window()

arc.run()
