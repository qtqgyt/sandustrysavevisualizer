from asyncio.subprocess import Process
from math import ceil, floor
from loguru import logger
import pygame
from pygame.event import Event

from tools.tool import Tool

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from window import window

MAX_SIZE = 50

SQUARE = 1
CIRCLE = 2

SIMPLE = []


class Eraser(Tool):
    def __init__(self) -> None:
        self.size_inc = 0
        self.shape = SQUARE
        super().__init__()

    def render(self, window) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = (window.camera_x + mouse_x) // window.zoom_level - self.size_inc // 2
        y = (window.camera_y + mouse_y) // window.zoom_level - self.size_inc // 2
        hover_rect = pygame.Rect(
            (x * window.zoom_level - window.camera_x),
            (y * window.zoom_level - window.camera_y),
            window.zoom_level * (self.size_inc + 1),
            window.zoom_level * (self.size_inc + 1),
        )
        pygame.draw.rect(window.screen, (255, 0, 0), hover_rect)
        tool_name = window.font.render(str(self), True, (255, 255, 255), (50, 50, 50, 50))
        window.screen.blit(tool_name, (10, window.window_height - tool_name.get_height() - 10))

    def handle_event(self, window, event: Event) -> tuple[bool, dict]:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                return self.process_mouse_down(window, event)
            case pygame.MOUSEMOTION:
                return self.process_mouse_move(window, event)
            case _:
                return (False, {})

    def process_mouse_move(self, window: "window", event: Event) -> tuple[bool, dict]:
        if event.buttons[0]:
            event.button = 1
            return self.process_mouse_down(window, event)
        return (False, {})

    def process_mouse_down(self, window: "window", event: Event) -> tuple[bool, dict]:
        if event.button == 4:
            if self.size_inc < MAX_SIZE:
                self.size_inc += 1
            return (False, {})
        if event.button == 5:
            if self.size_inc > 0:
                self.size_inc -= 1
            return (False, {})
        if not event.button == 1:
            return (False, {})
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = (window.camera_x + mouse_x) // window.zoom_level - self.size_inc // 2
        y = (window.camera_y + mouse_y) // window.zoom_level - self.size_inc // 2
        changed = False
        old = [[0] * (self.size_inc + 1)] * (self.size_inc + 1)
        x_pos = 0
        for c in range(max(0, x), min(window.cols - 1, x + (self.size_inc + 1))):
            y_pos = 0
            for r in range(max(0, y), min(window.rows - 1, y + (self.size_inc + 1))):
                tile_info = window.map.get_tile_info_at(c, r)
                if tile_info.is_particle():
                    old[x_pos][y_pos] = tile_info.id
                    window.map.set_tile(c, r, 0)
                    changed = True
        if changed:
            logger.debug(
                f"{max(0, x)} - {max(0, y)} - {min(window.cols, x + self.size_inc)} - {min(window.rows, y + self.size_inc)}"
            )
            window._update_tilemap_surface(max(0, x), max(0, y), self.size_inc + 1, self.size_inc + 1)
        return (changed, {"x": x, "y": y, "old": old, "new": 0, "size": self.size_inc})

    def activate(self, window) -> None:
        pygame.mouse.set_visible(False)

    def deactivate(self, window) -> None:
        pygame.mouse.set_visible(True)

    def __str__(self) -> str:
        return "Eraser"
