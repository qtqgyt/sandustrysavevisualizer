class TileInfo:
    def __init__(self, color: tuple[int, int, int], name: str, hex_code: str):
        self.color = color
        self.name = name
        self.hex_code = hex_code


default_tile = TileInfo((255, 192, 203), "Unknown", "#FFC0CB")

tile_colors: dict[int, TileInfo] = {
    0: TileInfo((0, 0, 0), "air", "#000000"),
    2: TileInfo((186, 127, 46), "Soil", "#ba7f2e"),
    3: TileInfo((119, 147, 37), "Sporemound", "#779325"),
    4: TileInfo((0, 0, 0), "Fog", "#000000"),
    5: TileInfo((255, 0, 0), "Artifact Number Block", "#ff0000"),
    6: TileInfo((112, 168, 236), "Undiscovered Water", "#70a8ec"),
    7: TileInfo((238, 246, 246), "Frostbed", "#eef6f6"),
    8: TileInfo((255, 128, 0), "Sealing Block", "#ff8000"),
    9: TileInfo((115, 177, 67), "Grass", "#73b143"),
    10: TileInfo((91, 206, 34), "Moss", "#5bce22"),
    13: TileInfo((255, 102, 0), "Undiscovered Lava", "#ff6600"),
    14: TileInfo((175, 0, 224), "Fluxite", "#af00e0"),
    15: TileInfo((217, 157, 14), "Block", "#d99d0e"),
    16: TileInfo((217, 157, 14), "SlidingBlock", "#d99d0e"),
    17: TileInfo((217, 157, 14), "SlidingBlockLeft", "#d99d0e"),
    18: TileInfo((217, 157, 14), "SlidingBlockRight", "#d99d0e"),
    19: TileInfo((217, 157, 14), "ConveyorLeft", "#d99d0e"),
    20: TileInfo((217, 157, 14), "ConveyorRight", "#d99d0e"),
    21: TileInfo((217, 157, 14), "ShakerLeft", "#d99d0e"),
    22: TileInfo((217, 157, 14), "ShakerRight", "#d99d0e"),
    23: TileInfo((170, 170, 170), "Bedrock", "#aaaaaa"),
    24: TileInfo((217, 157, 14), "Kinetic Slag Press", "#d99d0e"),
    25: TileInfo((102, 204, 255), "Ice", "#66ccff"),
    28: TileInfo((163, 0, 0), "Redsoil", "#a30000"),
    29: TileInfo((103, 27, 0), "Scoria", "#671b00"),
    30: TileInfo((224, 211, 184), "Crackstone", "#e0d3b8"),
    101: TileInfo((218, 171, 105), "Sand", "#daab69"),
    103: TileInfo((112, 168, 236), "Water", "#70a8ec"),
    104: TileInfo((210, 154, 76), "Wet Sand", "#d29a4c"),
    105: TileInfo((163, 0, 0), "Redsand", "#a30000"),
    106: TileInfo((171, 171, 171), "Slag", "#ababab"),
    107: TileInfo((250, 250, 2), "Gold", "#fafa02"),
    108: TileInfo((96, 36, 108), "Voidbloom", "#60246c"),
    110: TileInfo((172, 196, 229), "Steam", "#acc4e5"),
    111: TileInfo((255, 174, 11), "Fire", "#ffae0b"),
    112: TileInfo((238, 246, 246), "Snow", "#eef6f6"),
    113: TileInfo((255, 174, 11), "Flame", "#ffae0b"),
    114: TileInfo((99, 99, 99), "Burnt Slag", "#636363"),
    115: TileInfo((190, 218, 105), "Spore", "#beda69"),
    116: TileInfo((150, 186, 46), "Wet Spore", "#96ba2e"),
    117: TileInfo((70, 153, 26), "Seed", "#46991a"),
    118: TileInfo((139, 105, 218), "Amethelis", "#8b69da"),
    119: TileInfo((255, 174, 11), "Lava", "#ffae0b"),
    120: TileInfo((117, 10, 0), "Cinder", "#750a00"),
}
