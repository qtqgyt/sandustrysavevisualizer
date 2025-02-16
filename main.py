import json
import os
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys

default_color = (255, 192, 203)  # default color (pink)

tile_colors: dict[int, tuple[int, int, int]] = {
    0: (0, 0, 0),  # Air (black)
    2: (186, 127, 46),  # Soil is #ba7f2e
    3: (119, 147, 37),  # Sporemound is #779325
    4: (0, 0, 0),  # Fog (black)
    5: (255, 0, 0),  # Artifact Number Block is #ff0000
    6: (112, 168, 236),  # Undiscovered Water is #70a8ec
    7: (238, 246, 246),  # Frostbed is #eef6f6
    8: (255, 128, 0),  # Sealing Block? is #ff8000
    9: (115, 177, 67),  # Grass is #73b143
    10: (91, 206, 34),  # Moss is #5bce22
    13: (255, 102, 0),  # Undiscovered Lava is #ff6600
    14: (175, 0, 224),  # Fluxite is #af00e0
    15: (217, 157, 14),  # Block is #d99d0e (factory tiles)
    16: (217, 157, 14),  # tile 16 is #d99d0e (factory tiles)
    17: (217, 157, 14),  # tile 17 is #d99d0e (factory tiles)
    18: (217, 157, 14),  # tile 18 is #d99d0e (factory tiles)
    19: (217, 157, 14),  # tile 19 is #d99d0e (factory tiles)
    20: (217, 157, 14),  # tile 20 is #d99d0e (factory tiles)
    21: (217, 157, 14),  # tile 21 is #d99d0e (factory tiles)
    22: (217, 157, 14),  # tile 22 is #d99d0e (factory tiles)
    23: (170, 170, 170),  # Bedrock (#aaaaaa)
    24: (217, 157, 14),  # Kinetic Slag Press (factory tiles)
    25: (102, 204, 255),  # Ice is #66ccff
    28: (163, 0, 0),  # Redsoil is #a30000
    29: (103, 27, 0),  # Scoria is #671b00
    30: (224, 211, 184),  # Crackstone is #e0d3b8
    101: (218, 171, 105),  # Sand is #daab69
    103: (112, 168, 236),  # Water is #70a8ec
    104: (210, 154, 76),  # Wet Sand is #d29a4c
    105: (163, 0, 0),  # tile 105 is #a30000
    106: (171, 171, 171),  # Slag is #ababab
    107: (250, 250, 2),  # Gold is #fafa02
    108: (96, 36, 108),  # Voidbloom is #60246c
    110: (172, 196, 229),  # Steam is #acc4e5
    111: (255, 174, 11),  # Fire is #ffae0b
    112: (238, 246, 246),  # Snow is #eef6f6
    113: (255, 174, 11),  # Flame is #ffae0b
    114: (99, 99, 99),  # Burnt Slag is #636363
    115: (190, 218, 105),  # Spore is #beda69
    116: (150, 186, 46),  # Wet Spore is #96ba2e
    117: (70, 153, 26),  # Seed is #46991a
    118: (139, 105, 218),  # Amethelis is #8b69da
    119: (255, 174, 11),  # Lava is #ffae0b
    120: (117, 10, 0),  # Cinder #750a00
}
tile_names: dict[int, str] = {
    0: "Air",
    2: "Soil",
    3: "Sporemound",
    4: "Fog",
    5: "Artifact/Cat Block",
    6: "Undiscovered Water",
    7: "Frostbed",
    8: "Sealing Block",
    9: "Grass",
    10: "Moss",
    13: "Undiscovered Lava",
    14: "Fluxite",
    15: "Factory Tile",
    16: "Factory Tile",
    17: "Factory Tile",
    18: "Factory Tile",
    19: "Factory Tile",
    20: "Factory Tile",
    21: "Factory Tile",
    22: "Factory Tile",
    23: "Bedrock",
    24: "Kinetic Slag Press",
    25: "Ice",
    28: "Redsoil",
    29: "Scoria",
    30: "Crackstone",
    101: "Sand",
    103: "Water",
    104: "Wet Sand",
    105: "Tile 105",
    106: "Slag",
    107: "Gold",
    108: "Voidbloom",
    110: "Steam",
    111: "Fire",
    112: "Snow",
    113: "Flame",
    114: "Burnt Slag",
    115: "Spore",
    116: "Wet Spore",
    117: "Seed",
    118: "Amethelis",
    119: "Lava",
    120: "Cinder",
}


def render():
    json_path = os.path.join(os.path.dirname(__file__), "autosave.save")
    try:
        with open(json_path, 'r', encoding="utf-8", errors="replace") as file:
            contents = file.read()
        json_strings = [s for s in contents.splitlines() if s.strip()]
        objects = []
        for s in json_strings:
            try:
                obj = json.loads(s)
                objects.append(obj)
            except Exception as ee:
                print("Error parsing a JSON segment:", ee)
        # Extract gold, fluxite, and artifacts from the first JSON segment at path resources.gold, fluxite, artifacts
        resources = objects[0].get("resources", {}) if objects else {}
        gold = resources.get("gold", 0)
        fluxite = resources.get("fluxite", 0)
        artifacts = resources.get("artifacts", 0)

        data = None
        for obj in objects:
            if "world" in obj and "matrix" in obj["world"]:
                data = obj["world"]["matrix"]
                break
        if data is None:
            print("Could not find world.matrix in save file.")
            return
        if not (isinstance(data, list) and all(isinstance(row, list) for row in data)):
            print("world.matrix is not a valid tilemap.")
            return
    except Exception as e:
        print(f"Error loading tilemap: {e}")
        return

    rows = len(data)
    cols = max(len(row) for row in data)
    tile_size = max(min(32, 1280 // cols, 1280 // rows), 1)
    tilemap_width = cols * tile_size
    tilemap_height = rows * tile_size

    pygame.init()
    pygame.display.set_icon(create_magnifying_glass_icon())
    pygame.mouse.set_cursor(create_cursor())
    window_width, window_height = 800, 600
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Sandustry Save Visualizer")

    tilemap_surface = pygame.Surface((tilemap_width, tilemap_height))
    for y, row in enumerate(data):
        for x, tile in enumerate(row):
            # If tile is an array, use its first element.
            if isinstance(tile, list):
                tile = tile[0]

            color = tile_colors.get(tile, default_color) if isinstance(tile, int) else default_color
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(tilemap_surface, color, rect)

    camera_x, camera_y = 0, 0
    scroll_speed = 10
    clock = pygame.time.Clock()
    running = True

    # Pre-create a font for HUD text
    font = pygame.font.SysFont(None, 24)
    # Set camera to middle on start
    camera_x = (tilemap_width - window_width) // 2
    camera_y = (tilemap_height - window_height) // 2
    while running:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camera_x = max(camera_x - scroll_speed, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            camera_x = min(camera_x + scroll_speed, tilemap_width - window_width)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            camera_y = max(camera_y - scroll_speed, 0)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            camera_y = min(camera_y + scroll_speed, tilemap_height - window_height)
        if keys[pygame.K_ESCAPE]:
            running = False

        screen.fill((0, 0, 0))
        screen.blit(tilemap_surface, (0, 0), area=pygame.Rect(camera_x, camera_y, window_width, window_height))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_x = camera_x + mouse_x
        world_y = camera_y + mouse_y
        tile_x = world_x // tile_size
        tile_y = world_y // tile_size
        if 0 <= tile_y < rows and 0 <= tile_x < cols:
            tile_id = data[tile_y][tile_x]
            # If tile_id is an array, use its first element.
            if isinstance(tile_id, list):
                tile_id = tile_id[0]
            hover_rect = pygame.Rect(tile_x * tile_size - camera_x, tile_y * tile_size - camera_y, tile_size, tile_size)
            pygame.draw.rect(screen, (255, 0, 0), hover_rect, 2)
            if isinstance(tile_id, int):
                tile_name = tile_names.get(tile_id, "Unknown")
            else:
                tile_name = "Unknown"
            text_surface = font.render(f"Tile: {tile_id} - {tile_name}", True, (255, 255, 255))
            screen.blit(text_surface, (mouse_x + 10, mouse_y - text_surface.get_height() + 10))
        draw_hud(screen, artifacts, fluxite, font, gold)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def draw_hud(screen, artifacts, fluxite, font, gold):
    """Render gold, fluxite, and artifacts amounts on HUD"""
    gold_text = font.render(f"Gold: {gold}", True, (255, 215, 0))
    fluxite_text = font.render(f"Fluxite: {fluxite}", True, (175, 0, 224))
    artifacts_text = font.render(f"Artifacts: {artifacts}/2", True, (45, 197, 214))
    background_width = max(gold_text.get_width(), fluxite_text.get_width(), artifacts_text.get_width()) + 10
    background_surface = pygame.Surface((background_width+10, 100), pygame.SRCALPHA)
    background_surface.fill((0,0,0,0))
    pygame.draw.rect(background_surface, (128, 128, 128, 128), pygame.Rect(5, 5, background_width, 90), 0, 5)
    screen.blit(background_surface, (0, 0))
    screen.blit(gold_text, (10, 10))
    screen.blit(fluxite_text, (10, 40))
    screen.blit(artifacts_text, (10, 70))


def create_cursor() -> pygame.Cursor:
    size = 24
    cursor_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    cursor_surface.fill((0, 0, 0, 0))

    circle_radius = size // 3
    circle_center = (size // 2, size // 2)

    handle_start = (circle_center[0] + 5, circle_center[1] + 5)
    handle_end = (size, size)
    pygame.draw.line(cursor_surface, (139, 69, 19), handle_start, handle_end, 3)

    pygame.draw.circle(cursor_surface, (128, 128, 128), circle_center, circle_radius, 2)

    return pygame.cursors.Cursor(circle_center, cursor_surface)


def create_magnifying_glass_icon() -> pygame.Surface:
    size = 32
    icon = pygame.Surface((size, size), pygame.SRCALPHA)
    icon.fill((0, 0, 0, 0))

    circle_radius = size // 3
    circle_center = (size // 2, size // 2)

    handle_start = (circle_center[0] + 3, circle_center[1] + 3)
    handle_end = (size - 2, size - 2)
    pygame.draw.line(icon, (64, 64, 64), handle_start, handle_end, 4)

    pygame.draw.circle(icon, (128, 128, 128), circle_center, circle_radius, 2)
    pygame.draw.circle(icon, (173, 216, 230, 128), circle_center, circle_radius - 1, 0)

    return icon


if __name__ == '__main__':
    render()
