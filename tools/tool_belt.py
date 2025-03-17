import pygame
from loguru import logger
from pygame.event import Event

from tools import Eraser, Pencil, Tool

from .cursor import Cursor


class ToolBelt:
    def __init__(self) -> None:
        self.all_tools: dict[int, Tool] = {
            pygame.K_c: Cursor(),
            pygame.K_p: Pencil(),
            pygame.K_e: Eraser(),
        }
        self.current = self.all_tools[pygame.K_c]

    def process_keys(self, window):
        self.current.process_keys(window)

    def process_keydown(self, window, key):
        if (pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]) and key in [
            *self.all_tools
        ]:
            self.current = self.all_tools[key]
            logger.debug(f"Set tool to {str(self.current)}")
            return
        self.current.process_keydown(window, key)

    def handle_event(self, window, event: Event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                self.current.process_mouse_down(window, event)
            case _:
                pass

    def render(self, window):
        self.current.render(window)
