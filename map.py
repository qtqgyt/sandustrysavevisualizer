import json
from pprint import pprint


class TileInfo:
    def __init__(self, id: int, color: tuple[int, int, int], name: str, hex_code: str):
        self.id = id
        self.color = color
        self.name = name
        self.hex_code = hex_code

    def is_particle(self):
        return self.id > 100

    def __str__(self) -> str:
        return f"Tile: {self.id} - {self.name}"


default_tile = TileInfo(-1, (255, 192, 203), "Unknown", "#FFC0CB")

tile_colors: dict[int, TileInfo] = {
    0: TileInfo(0, (68, 68, 68), "air", "#000000"),
    2: TileInfo(2, (186, 127, 46), "Soil", "#ba7f2e"),
    3: TileInfo(3, (119, 147, 37), "Sporemound", "#779325"),
    4: TileInfo(4, (0, 0, 0), "Fog", "#000000"),
    5: TileInfo(5, (255, 0, 0), "Artifact Number Block", "#ff0000"),
    6: TileInfo(6, (112, 168, 236), "Undiscovered Water", "#70a8ec"),
    7: TileInfo(7, (238, 246, 246), "Frostbed", "#eef6f6"),
    8: TileInfo(8, (255, 128, 0), "Sealing Block", "#ff8000"),
    9: TileInfo(9, (115, 177, 67), "Grass", "#73b143"),
    10: TileInfo(10, (91, 206, 34), "Moss", "#5bce22"),
    11: TileInfo(11, (250, 250, 2), "Solid Gold", "#ff6600"),
    12: TileInfo(12, (139, 105, 218), "Solid Amethelis", "#ff6600"),
    13: TileInfo(13, (255, 102, 0), "Undiscovered Lava", "#ff6600"),
    14: TileInfo(14, (175, 0, 224), "Fluxite", "#af00e0"),
    15: TileInfo(15, (217, 157, 14), "Block", "#d99d0e"),
    16: TileInfo(16, (217, 157, 14), "SlidingBlock", "#d99d0e"),
    17: TileInfo(17, (217, 157, 14), "SlidingBlockLeft", "#d99d0e"),
    18: TileInfo(18, (217, 157, 14), "SlidingBlockRight", "#d99d0e"),
    19: TileInfo(19, (217, 157, 14), "ConveyorLeft", "#d99d0e"),
    20: TileInfo(20, (217, 157, 14), "ConveyorRight", "#d99d0e"),
    21: TileInfo(21, (217, 157, 14), "ShakerLeft", "#d99d0e"),
    22: TileInfo(22, (217, 157, 14), "ShakerRight", "#d99d0e"),
    23: TileInfo(23, (170, 170, 170), "Bedrock", "#aaaaaa"),
    24: TileInfo(24, (217, 157, 14), "Kinetic Slag Press", "#d99d0e"),
    25: TileInfo(25, (102, 204, 255), "Ice", "#66ccff"),
    28: TileInfo(28, (163, 0, 0), "Redsoil", "#a30000"),
    29: TileInfo(29, (103, 27, 0), "Scoria", "#671b00"),
    30: TileInfo(30, (224, 211, 184), "Crackstone", "#e0d3b8"),
    101: TileInfo(101, (218, 171, 105), "Sand", "#daab69"),
    103: TileInfo(103, (112, 168, 236), "Water", "#70a8ec"),
    104: TileInfo(104, (210, 154, 76), "Wet Sand", "#d29a4c"),
    105: TileInfo(105, (163, 0, 0), "Redsand", "#a30000"),
    106: TileInfo(106, (171, 171, 171), "Slag", "#ababab"),
    107: TileInfo(107, (250, 250, 2), "Gold", "#fafa02"),
    108: TileInfo(108, (96, 36, 108), "Voidbloom", "#60246c"),
    110: TileInfo(110, (172, 196, 229), "Steam", "#acc4e5"),
    111: TileInfo(111, (255, 174, 11), "Fire", "#ffae0b"),
    112: TileInfo(112, (238, 246, 246), "Snow", "#eef6f6"),
    113: TileInfo(113, (255, 174, 11), "Flame", "#ffae0b"),
    114: TileInfo(114, (99, 99, 99), "Burnt Slag", "#636363"),
    115: TileInfo(115, (190, 218, 105), "Spore", "#beda69"),
    116: TileInfo(116, (150, 186, 46), "Wet Spore", "#96ba2e"),
    117: TileInfo(117, (70, 153, 26), "Seed", "#46991a"),
    118: TileInfo(118, (139, 105, 218), "Amethelis", "#8b69da"),
    119: TileInfo(119, (255, 174, 11), "Lava", "#ffae0b"),
    120: TileInfo(120, (117, 10, 0), "Cinder", "#750a00"),
}


class Map:
    def __init__(self, path) -> None:
        self.path = path
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as file:
                contents = file.read()
            self.data = [json.loads(s.strip()) for s in contents.splitlines()]
            # Extract gold, fluxite, and artifacts from the first JSON segment at path resources.gold, fluxite, artifacts
            resources = self.data[0].get("resources", {}) if self.data else {}
            self.gold = resources.get("gold", 0)
            self.fluxite = resources.get("fluxite", 0)
            self.artifacts = resources.get("artifacts", 0)

            found = False
            for obj in self.data:
                if "world" in obj and "matrix" in obj["world"]:
                    found = True
                    self.world = obj["world"]["matrix"]
                    break
            if not found:
                raise RuntimeError("Could not find world.matrix in save file.")
            if not (isinstance(self.world, list) and all(isinstance(row, list) for row in self.world)):
                raise RuntimeError("world.matrix is not a valid tilemap.")
            player_data = self.data[1].get("player", {}) if len(self.data) > 1 else {}
            self.player_x = player_data.get("x", 0) / 4
            self.player_y = player_data.get("y", 0) / 4
            self.active_slot = player_data.get("activeslotindex", 0)
        except Exception as e:
            raise e

    def get_tile(self, x: int, y: int):
        return self.world[y][x]

    def set_tile(self, x: int, y: int, tile) -> None:
        self.world[y][x] = tile

    def get_tile_info(self, tile) -> TileInfo:
        tileInfo = default_tile
        if isinstance(tile, int):
            tileInfo = tile_colors.get(tile, default_tile)
        if isinstance(tile, dict) and "element" in tile and "type" in tile["element"]:
            tileInfo = tile_colors.get(tile["element"]["type"] + 100, default_tile)
        if tileInfo == default_tile:
            pprint(tile)
        return tileInfo
