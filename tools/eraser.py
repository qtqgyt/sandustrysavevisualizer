from loguru import logger
from pygame.event import Event

from tools.tool import Tool

SQUARE = 1
CIRCLE = 2

SIMPLE = []


class Eraser(Tool):
    def __init__(self) -> None:
        self.size = 1
        self.shape = SQUARE
        super().__init__()

    def process_keys(self, window) -> None:
        super().process_keys(window)

    def process_keydown(self, window, key) -> None: ...
    def render(self, window) -> None:
        super().render(window)

    def process_mouse(self, window) -> None: ...

    def process_mouse_down(self, window, event: Event) -> tuple[bool, dict]:
        logger.debug(f"Moused clicked at: {event.dict}")
        mouse_x, mouse_y = event.pos
        x = (window.camera_x + mouse_x) // window.zoom_level
        y = (window.camera_y + mouse_y) // window.zoom_level
        tile = window.map.get_tile(x, y)
        logger.debug(tile)
        return (False, {})

    def __str__(self) -> str:
        return "Eraser"
