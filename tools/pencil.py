from map import Map
from tools.tool import Tool


class Pencil(Tool):
    def __init__(self) -> None:
        super().__init__()

    def process_keys(self, window) -> None:
        super()

    def process_keydown(self, window, key) -> None: ...
    def render(self, window) -> None: ...
    def process_mouse(self, window) -> None: ...
    def process_click(self, map: Map, cursor: tuple[int, int]) -> tuple[bool, dict | None]: ...

    def __str__(self) -> str:
        return "Pencil"
