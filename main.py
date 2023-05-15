from pygame.constants import K_F1, K_F11
from curve import Curve
from grid import Grid
from pygex import *
import theme


# Constants
ANCHOR = (800, 800)
RADIUS = 7
WIDTH = 1

window = Window(ANCHOR, 'Bezier curve', fps_limit=60, vsync=True)
window.bg_color = theme.BG_COLOR

fullscreen_toast = Toast('To exit full screen press [F11]')
debug_panel = DebugPanel()
curve = Curve(RADIUS, WIDTH)
grid = Grid(
    curve,
    70,
    ANCHOR,
    theme.BG_ACCENT_COLOR,
    theme.BG_NOT_ACCENT_COLOR,
    WIDTH,
    RADIUS
)

window.remove_renderable(curve.hint)
window.add_flippable(grid)
window.add_renderable(grid)
window.add_flippable(curve)
window.add_renderable(curve)
window.add_renderable(curve.hint)

debug_panel.apply_on_screen()

while window.is_running:
    window.render_views()

    if window.input.is_up(K_F1):
        window.take_screenshot()
    elif window.input.is_up(K_F11):
        window.fullscreen = not window.fullscreen

        if window.fullscreen:
            fullscreen_toast.show()
        else:
            fullscreen_toast.cancel()

    window.flip()
