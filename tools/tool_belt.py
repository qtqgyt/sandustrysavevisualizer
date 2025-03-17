from tools.tool import Tool

from .cursor import Cursor


class ToolBelt:
    def __init__(self) -> None:
        self.tools: dict[str, Tool] = {
            "cursor": Cursor(),
        }
        self.current = self.tools["cursor"]

    def process_keys(self, window):
        self.current.process_keys(window)

    def process_keydown(self, window, key):
        self.current.process_keydown(window, key)

    def render(self, window):
        self.current.render(window)
