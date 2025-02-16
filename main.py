import json
import os
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys

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
    tile_size = min(32, 1280 // cols, 1280 // rows)
    tilemap_width = cols * tile_size
    tilemap_height = rows * tile_size

    pygame.init()
    window_width, window_height = 800, 600
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Sandustry Save visualizer")

    tilemap_surface = pygame.Surface((tilemap_width, tilemap_height))
    for y, row in enumerate(data):
        for x, tile in enumerate(row):
            # If tile is an array, use its first element.
            if isinstance(tile, list):
                tile = tile[0]
            if tile == 0:
                color = (0, 0, 0)        # air (black)
            elif tile == 23:
                color = (170, 170, 170)  # bedrock (#aaaaaa)
            elif tile == 2:
                color = (186, 127, 46)   # tile 2 is #ba7f2e
            elif tile == 3:
                color = (119,147,37)     # tile 3 is #779325
            elif tile == 4:
                color = (0, 0, 0)        # fog #000000
            elif tile == 10:
                color = (91, 206, 34)    # tile 10 is #5bce22
            elif tile == 14:
                color = (175, 0, 224)    # tile 14 is #af00e0
            elif tile == 13:
                color = (255, 102, 0)    # tile 13 is #ff6600
            elif tile == 30:
                color = (224, 211, 184)  # tile 30 is #e0d3b8
            elif tile == 28:
                color = (163, 0, 0)      # tile 28 is #a30000
            elif tile == 103:
                color = (112, 168, 236)  # tile 103 is #70a8ec
            elif tile == 6:
                color = (112, 168, 236)  # tile 6 is #70a8ec
            elif tile == 104:
                color = (210, 154, 76)   # tile 104 is #d29a4c
            elif tile == 101:
                color = (218, 171, 105)  # tile 101 is #daab69
            elif tile == 9:
                color = (115, 177, 67)   # tile 9 is #73b143
            elif tile == 7:
                color = (238, 246, 246)  # tile 7 is #eef6f6
            elif tile == 112:
                color = (238, 246, 246)  # tile 7 is #eef6f6
            elif tile == 25:
                color = (102, 204, 255)  # tile 25 is #66ccff
            elif tile == 105:
                color = (163, 0, 0)      # tile 28 is #a30000
            elif tile == 110:
                color = (175, 175, 175)  # tile 110 is #afafaf
            elif tile == 8:
                color = (255, 128, 0)    # tile 8 is #ff8000
            elif tile == 116:
                color = (150, 186, 46)   # tile 116 is #96ba2e
            elif tile in [15,16,17,18,19,20,21,22,24]: #factory tiles
                color = (217, 157, 14)   # tile 15 is #d99d0e
            elif tile == 118:
                color = (139, 105, 218)  # tile 118 is #8b69da
            elif tile == 108:
                color = (96, 36, 108)    # tile 108 is #60246c
            elif tile == 115:
                color = (190, 218, 105)  # tile 115 is #beda69
            elif tile == 120:
                color = (117, 10, 0)     # tile 120 is #750a00
            elif tile == 29:
                color = (103, 27, 0)     # tile 29 is #671b00
            elif tile == 119:
                color = (255, 174, 11)   # tile 119 is #ffae0b
            elif tile == 111:
                color = (255, 174, 11)   # tile 111 is #ffae0b
            elif tile == 107:
                color = (250, 250, 2)    # tile 107 is #fafa02
# add more factory tiles later
            else:
                color = (255, 192, 203)  # default color (pink)
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(tilemap_surface, color, rect)

    camera_x, camera_y = 0, 0
    scroll_speed = 10
    clock = pygame.time.Clock()
    running = True

    # Pre-create a font for HUD text
    font = pygame.font.SysFont(None, 24)

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
            text_surface = font.render(f"Tile: {tile_id}", True, (255, 255, 255))
            screen.blit(text_surface, (mouse_x + 5, mouse_y + 5))
        
        # Render gold, fluxite, and artifacts amounts on HUD
        gold_text = font.render(f"Gold: {gold}", True, (255, 215, 0))
        fluxite_text = font.render(f"Fluxite: {fluxite}", True, (175, 0, 224))
        artifacts_text = font.render(f"Artifacts: {artifacts}/2", True, (45, 197, 214))
        screen.blit(gold_text, (10, 10))
        screen.blit(fluxite_text, (10, 40))
        screen.blit(artifacts_text, (10, 70))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    render()
