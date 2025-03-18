from tools.tool import Tool


class Pencil(Tool):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Pencil"
