from loguru import logger
import pygame
from pygame.event import Event

from tools.tool import Tool

MAX_SIZE = 10

SQUARE = 1
CIRCLE = 2

SIMPLE = []


class Eraser(Tool):
    def __init__(self) -> None:
        self.size = 1
        self.shape = SQUARE
        super().__init__()

    def render(self, window) -> None:
        logger.info(f"Eraser size: {self.size}")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = (window.camera_x + mouse_x) // window.zoom_level
        y = (window.camera_y + mouse_y) // window.zoom_level
        if 0 <= y < window.rows and 0 <= x < window.cols:
            hover_rect = pygame.Rect(
                x * window.zoom_level - window.camera_x,
                y * window.zoom_level - window.camera_y,
                window.zoom_level * self.size,
                window.zoom_level * self.size,
            )
            pygame.draw.rect(window.screen, (255, 0, 0), hover_rect)
        tool_name = window.font.render(str(self), True, (255, 255, 255), (50, 50, 50, 50))
        window.screen.blit(tool_name, (10, window.window_height - tool_name.get_height() - 10))

    def handle_event(self, window, event: Event) -> tuple[bool, dict]:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                return self.process_mouse_down(window, event)
            case _:
                return (False, {})

    def process_mouse_down(self, window, event: Event) -> tuple[bool, dict]:
        if event.button == 4:
            if self.size < MAX_SIZE:
                self.size += 1
            return (False, {})
        if event.button == 5:
            if self.size > 1:
                self.size -= 1
            return (False, {})
        logger.debug(f"Moused clicked at: {event.dict}")
        mouse_x, mouse_y = event.pos
        x = (window.camera_x + mouse_x) // window.zoom_level
        y = (window.camera_y + mouse_y) // window.zoom_level
        tile_info = window.map.get_tile_info_at(x, y)
        if tile_info.is_particle():
            old = tile_info.id
            window.map.set_tile(x, y, 0)
            window._update_tilemap_surface(x, y, 1, 1)
            return (True, {"x": x, "y": y, "old": old, "new": 0, "size": self.size})
        return (False, {})

    def __str__(self) -> str:
        return "Eraser"
