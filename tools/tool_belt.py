import pygame
from loguru import logger
from pygame.event import Event

from history import History
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
        self.history = History()

    def process(self, window):
        self.current.process(window)

    def process_keydown(self, window, key) -> bool:
        if (pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]) and key in [
            *self.all_tools
        ]:
            self.current.deactivate(window)
            self.current = self.all_tools[key]
            self.current.activate(window)
            return True
        return False

    def handle_event(self, window, event: Event):
        changed, data = (False, {})
        match event.type:
            case pygame.KEYDOWN:
                if not self.process_keydown(window, event.key):
                    changed, data = self.current.handle_event(window, event)
            case _:
                changed, data = self.current.handle_event(window, event)
        if changed:
            self.history.add(data)

    def render(self, window):
        self.current.render(window)
