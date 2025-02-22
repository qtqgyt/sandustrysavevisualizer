import json
from os import environ
import sys
import tkinter as tk
from tkinter import filedialog
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

zoom_level = 1.0

base_zoom_multiplier = zoom_level

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
    120: TileInfo((117, 10, 0), "Cinder", "#750a00")
}

def render():
    # Move zoom_level to top of function and remove duplicate declaration
    zoom_level = 1.0
    # Open file dialog to choose 
    pygame.init()
    pygame.display.set_icon(create_magnifying_glass_icon())
    pygame.mouse.set_cursor(create_cursor())
    window_width, window_height = 800, 600
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Sandustry Save Visualizer")
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    json_path = filedialog.askopenfilename(title="Select save file", filetypes=[("Save Files", "*.save")])
    root.destroy()
    if not json_path:
        print("No file selected.")
        return
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
        player_data = objects[1].get("player", {}) if len(objects) > 1 else {}
        player_x = player_data.get("x", 0) / 4
        player_y = player_data.get("y", 0) / 4
        active_slot = player_data.get("activeslotindex", 0)  # Get active slot
        player_x *= base_zoom_multiplier
        player_y *= base_zoom_multiplier
    except Exception as e:
        print(f"Error loading tilemap: {e}")
        return

    rows = len(data)
    cols = max(len(row) for row in data)
    base_tile_size = max(min(32, 1280 // cols, 1280 // rows), 1)
    tile_size = int(base_tile_size * base_zoom_multiplier)
    tilemap_width = cols * tile_size
    tilemap_height = rows * tile_size

    print("Contact @ qw000erty_71712 on discord for help.")

    tilemap_surface = pygame.Surface((tilemap_width, tilemap_height))
    for y, row in enumerate(data):
        for x, tile in enumerate(row):
            # If tile is an array, use its first element.
            if isinstance(tile, list):
                tile = tile[0]

            tile_info = tile_colors.get(tile, default_tile) if isinstance(tile, int) else default_tile
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(tilemap_surface, tile_info.color, rect)

    camera_x, camera_y = 0, 0
    scroll_speed = 10
    clock = pygame.time.Clock()
    running = True

    # Pre-create a font for HUD text
    font = pygame.font.SysFont(None, 24)
    # Set camera to middle on start
    camera_x = (tilemap_width - window_width) // 2
    camera_y = (tilemap_height - window_height) // 2

    def draw_loading_overlay(screen, font):
        """Draw a loading text overlay in the center of the screen"""
        loading_text = font.render("LOADING...", True, (255, 255, 255))
        text_rect = loading_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        
        # Draw semi-transparent background
        background = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(background, (0, 0, 0, 128), background.get_rect())
        screen.blit(background, (0, 0))
        screen.blit(loading_text, text_rect)
        pygame.display.flip()

    def update_map_dimensions():
        nonlocal tile_size, tilemap_width, tilemap_height, tilemap_surface, zoom_level
        print(f"Debug: Updating dimensions - Current zoom: {zoom_level}, Current tile size: {tile_size}")
        # Ensure tile_size is never less than 1
        new_tile_size = max(1, int(base_tile_size * zoom_level))
        print(f"Debug: New tile size would be: {new_tile_size} (base_tile_size: {base_tile_size})")
        if new_tile_size != tile_size:
            # Show loading overlay before starting update
            draw_loading_overlay(screen, font)
            
            tile_size = new_tile_size
            tilemap_width = cols * tile_size
            tilemap_height = rows * tile_size
            print(f"Debug: New dimensions - width: {tilemap_width}, height: {tilemap_height}")
            # Recreate tilemap surface with new dimensions
            tilemap_surface = pygame.Surface((tilemap_width, tilemap_height))
            for y, row in enumerate(data):
                for x, tile in enumerate(row):
                    if isinstance(tile, list):
                        tile = tile[0]
                    tile_info = tile_colors.get(tile, default_tile) if isinstance(tile, int) else default_tile
                    rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    pygame.draw.rect(tilemap_surface, tile_info.color, rect)
            return True
        return False

    update_map_dimensions()
    
    while running:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_x = camera_x + mouse_x
                world_y = camera_y + mouse_y
                
                # Store relative position before zoom
                rel_x = world_x / tilemap_width if tilemap_width > 0 else 0.5
                rel_y = world_y / tilemap_height if tilemap_height > 0 else 0.5
                
                old_zoom = zoom_level
                if event.key in [pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS]:
                    print(f"Debug: Attempting to zoom in from {zoom_level}")
                    zoom_level = min(4.0, zoom_level * 1.5)  # Increased zoom factor
                    print(f"Debug: New zoom level: {zoom_level}")
                elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                    print(f"Debug: Attempting to zoom out from {zoom_level}")
                    zoom_level = max(0.25, zoom_level / 1.5)  # Increased zoom factor
                    print(f"Debug: New zoom level: {zoom_level}")
                
                # Only update if zoom changed
                if old_zoom != zoom_level:
                    print(f"Debug: Zoom changed from {old_zoom} to {zoom_level}")
                    if update_map_dimensions():
                        print("Debug: Map dimensions updated successfully")
                    else:
                        print("Debug: No dimension update needed")
                    # Maintain focus point
                    new_world_x = rel_x * tilemap_width
                    new_world_y = rel_y * tilemap_height
                    camera_x = int(new_world_x - mouse_x)
                    camera_y = int(new_world_y - mouse_y)
                    camera_x = max(0, min(camera_x, tilemap_width - window_width))
                    camera_y = max(0, min(camera_y, tilemap_height - window_height))

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
        # Draw player marker: green circle indicating player's position
        pygame.draw.circle(screen, (0, 255, 0), (player_x - camera_x, player_y - camera_y), max(tile_size // 2, 5))
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
            tile_info = tile_colors.get(tile_id, default_tile) if isinstance(tile_id, int) else default_tile
            text_surface = font.render(f"Tile: {tile_id} - {tile_info.name}", True, (255, 255, 255))
            screen.blit(text_surface, (mouse_x + 10, mouse_y - text_surface.get_height() + 10))
        draw_hud(screen, artifacts, fluxite, font, gold, active_slot)  # Updated function call
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def draw_hud(screen, artifacts, fluxite, font, gold, active_slot: int):
    """Render gold, fluxite, artifacts amounts and hotbar on HUD"""
    # Resources HUD
    gold_text = font.render(f"Gold: {gold}", True, (255, 215, 0))
    fluxite_text = font.render(f"Fluxite: {fluxite}", True, (175, 0, 224))
    artifacts_text = font.render(f"Artifacts: {artifacts}/2", True, (45, 197, 214))
    background_width = max(gold_text.get_width(), fluxite_text.get_width(), artifacts_text.get_width()) + 10
    background_surface = pygame.Surface((background_width + 10, 100), pygame.SRCALPHA)
    background_surface.fill((0, 0, 0, 0))
    pygame.draw.rect(background_surface, (128, 128, 128, 128), pygame.Rect(5, 5, background_width, 90), 0, 5)
    screen.blit(background_surface, (0, 0))
    screen.blit(gold_text, (10, 10))
    screen.blit(fluxite_text, (10, 40))
    screen.blit(artifacts_text, (10, 70))

    # Hotbar
    slot_width = 60
    margin = 10
    hotbar_height = slot_width + (margin * 2)
    screen_width = screen.get_width()
    hotbar_y = screen.get_height() - hotbar_height
    
    # Calculate actual hotbar background width to only cover slots
    total_slots = 9
    total_width = total_slots * slot_width + (total_slots + 1) * margin
    start_x = (screen_width - total_width) // 2
    
    # Create hotbar background surface with transparency
    hotbar_surface = pygame.Surface((total_width, hotbar_height), pygame.SRCALPHA)
    # Draw rounded rectangle for hotbar background
    pygame.draw.rect(hotbar_surface, (50, 50, 50, 128), 
                    (0, 0, total_width, hotbar_height),
                    border_radius=10)  # Add rounded corners
    
    # Blit hotbar background at calculated position
    screen.blit(hotbar_surface, (start_x, hotbar_y))
    
    for idx in range(total_slots):
        slot_x = start_x + margin + idx * (slot_width + margin)
        color = (255, 215, 0) if idx == active_slot else (100, 100, 100)
        pygame.draw.rect(screen, color, (slot_x, hotbar_y + margin, slot_width, slot_width), 2)
        text_surface = font.render(str(idx), True, (255, 255, 255))
        # Position text in top-left corner with small offset
        text_x = slot_x + 4
        text_y = hotbar_y + margin + 4
        screen.blit(text_surface, (text_x, text_y))


def create_cursor() -> pygame.Cursor:
    size = 24
    cursor_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    cursor_surface.fill((0, 0, 0, 0))

    circle_radius = size // 3
    circle_center = (size // 2, size // 2)

    handle_start = (circle_center[0] + 5, circle_center[1] + 5)
    handle_end = (size, size)

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
