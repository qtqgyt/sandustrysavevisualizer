from tools.tool import Tool


class Pencil(Tool):
    def __init__(self) -> None:
        super().__init__()

    def process_keys(self, window) -> None:
        super().process_keys(window)

    def process_keydown(self, window, key) -> None: ...
    def render(self, window) -> None:
        super().render(window)

    def process_mouse(self, window) -> None: ...
    def process_mouse_down(self, window, event) -> tuple[bool, dict | None]: ...

    def __str__(self) -> str:
        return "Pencil"
