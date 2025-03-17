import math
import sys

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

from map import Map


class window:
    def __init__(self, title: str, map: Map) -> None:
        self.map = map
        self.zoom_level = 3
        # self.window_width, self.window_height = 800, 600
        self.window_width, self.window_height = 1920, 1380

        pygame.init()

        ICON_SIZE = 32
        pygame.display.set_icon(self._create_magnifying_glass(ICON_SIZE, filled=True))

        CURSOR_SIZE = 24
        cursor_surface = self._create_magnifying_glass(CURSOR_SIZE)
        cursor = pygame.cursors.Cursor((CURSOR_SIZE // 2, CURSOR_SIZE // 2), cursor_surface)
        pygame.mouse.set_cursor(cursor)

        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.rows = len(self.map.world)
        self.cols = max(len(row) for row in self.map.world)
        self.tilemap_width = self.cols * self.zoom_level
        self.tilemap_height = self.rows * self.zoom_level

        # Pre-create a font for HUD text
        self.font = pygame.font.SysFont(None, 24)

        self.scroll_speed = 10
        self.camera_x = (self.tilemap_width - self.window_width) // 2
        self.camera_y = (self.tilemap_height - self.window_height) // 2
        self._calculate_camera_borders()

    def _create_magnifying_glass(self, size: int, filled: bool = False) -> pygame.Surface:
        magnifying_glass = pygame.Surface((size, size), pygame.SRCALPHA)
        magnifying_glass.fill((0, 0, 0, 0))

        circle_radius = size // 3
        circle_center = (size // 2, size // 2)

        handle_offset = math.floor((circle_radius) / math.sqrt(2))
        handle_start = (circle_center[0] + handle_offset, circle_center[1] + handle_offset)
        handle_end = (size - 2, size - 2)

        pygame.draw.line(magnifying_glass, (64, 64, 64), handle_start, handle_end, 4)
        pygame.draw.circle(magnifying_glass, (128, 128, 128), circle_center, circle_radius, 2)
        if filled:
            pygame.draw.circle(magnifying_glass, (173, 216, 230, 128), circle_center, circle_radius - 1, 0)
        return magnifying_glass

    def draw_loading_overlay(self):
        """Draw a loading text overlay in the center of the screen"""
        loading_text = self.font.render("LOADING...", True, (255, 255, 255))
        text_rect = loading_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # Draw semi-transparent background
        background = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(background, (0, 0, 0, 128), background.get_rect())
        self.screen.blit(background, (0, 0))
        self.screen.blit(loading_text, text_rect)
        pygame.display.flip()

    def draw_resources(self) -> pygame.Surface:
        gold_text = self.font.render(f"Gold: {self.map.gold}", True, (255, 215, 0))
        fluxite_text = self.font.render(f"Fluxite: {self.map.fluxite}", True, (175, 0, 224))
        artifacts_text = self.font.render(f"Artifacts: {self.map.artifacts}/2", True, (45, 197, 214))

        background_width = max(gold_text.get_width(), fluxite_text.get_width(), artifacts_text.get_width()) + 10
        resources_hud = pygame.Surface((background_width + 10, 100), pygame.SRCALPHA)
        resources_hud.fill((0, 0, 0, 0))

        pygame.draw.rect(resources_hud, (128, 128, 128, 128), pygame.Rect(5, 5, background_width, 90), 0, 5)
        resources_hud.blits(
            [
                (gold_text, (10, 10)),
                (fluxite_text, (10, 40)),
                (artifacts_text, (10, 70)),
            ]
        )
        return resources_hud

    def draw_hotbar(self):
        # Hotbar
        slot_width = 60
        margin = 10
        hotbar_height = slot_width + (margin * 2)
        screen_width = self.screen.get_width()
        hotbar_y = self.screen.get_height() - hotbar_height

        # Calculate actual hotbar background width to only cover slots
        TOTAL_SLOTS = 9
        total_width = TOTAL_SLOTS * slot_width + (TOTAL_SLOTS + 1) * margin
        start_x = (screen_width - total_width) // 2

        # Create hotbar background surface with transparency
        hotbar_surface = pygame.Surface((total_width, hotbar_height), pygame.SRCALPHA)
        # Draw rounded rectangle for hotbar background
        pygame.draw.rect(
            hotbar_surface, (50, 50, 50, 128), (0, 0, total_width, hotbar_height), border_radius=10
        )  # Add rounded corners

        # Blit hotbar background at calculated position
        self.screen.blit(hotbar_surface, (start_x, hotbar_y))

        for idx in range(TOTAL_SLOTS):
            slot_x = start_x + margin + idx * (slot_width + margin)
            color = (255, 215, 0) if idx == self.map.active_slot else (100, 100, 100)
            pygame.draw.rect(self.screen, color, (slot_x, hotbar_y + margin, slot_width, slot_width), 2)
            text_surface = self.font.render(str(idx), True, (255, 255, 255))
            # Position text in top-left corner with small offset
            text_x = slot_x + 4
            text_y = hotbar_y + margin + 4
            self.screen.blit(text_surface, (text_x, text_y))

    def draw_new_tilemap(self) -> None:
        self.draw_loading_overlay()
        self.tilemap_width = self.cols * self.zoom_level
        self.tilemap_height = self.rows * self.zoom_level
        print(f"Debug: New dimensions - width: {self.tilemap_width}, height: {self.tilemap_height}")
        # Recreate tilemap surface with new dimensions
        self.tilemap_surface = pygame.Surface((self.tilemap_width, self.tilemap_height))
        for y, row in enumerate(self.map.world):
            for x, tile in enumerate(row):
                if isinstance(tile, list):
                    tile = tile[0]
                tile_info = self.map.get_tile_info(tile)
                rect = pygame.Rect(x * self.zoom_level, y * self.zoom_level, self.zoom_level, self.zoom_level)
                pygame.draw.rect(self.tilemap_surface, tile_info.color, rect)
        # Draw player marker: green circle indicating player's position
        pygame.draw.circle(
            self.tilemap_surface,
            (0, 255, 0),
            (self.map.player_x * self.zoom_level, self.map.player_y * self.zoom_level),
            max(self.zoom_level // 2, 5),
        )

    def _calculate_camera_borders(self) -> None:
        if 0 < self.tilemap_width - self.window_width:
            self.min_camera_x = 0
            self.max_camera_x = self.tilemap_width - self.window_width
        else:
            self.min_camera_x = self.tilemap_width - self.window_width
            self.max_camera_x = 0
        if 0 < self.tilemap_height - self.window_height:
            self.min_camera_y = self.tilemap_height - self.window_height
            self.max_camera_y = 0
        else:
            self.min_camera_y = 0
            self.max_camera_y = self.tilemap_height - self.window_height

    def update_map_dimensions(self, change: int) -> None:
        old_zoom = self.zoom_level
        self.zoom_level = max(1, min(4, self.zoom_level + change))  # Increased zoom factor
        if old_zoom == self.zoom_level:
            return
        print(f"Debug: Updating dimensions - Current zoom: {self.zoom_level}")

        self.draw_new_tilemap()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_x = self.camera_x + mouse_x
        world_y = self.camera_y + mouse_y
        rel_x = world_x / self.tilemap_width if self.tilemap_width > 0 else 0.5
        rel_y = world_y / self.tilemap_height if self.tilemap_height > 0 else 0.5
        new_world_x = rel_x * self.tilemap_width
        new_world_y = rel_y * self.tilemap_height
        self.camera_x = int(new_world_x - mouse_x)
        self.camera_y = int(new_world_y - mouse_y)
        self._calculate_camera_borders()

    def render(self):
        running = True
        clock = pygame.time.Clock()

        self.draw_new_tilemap()

        while running:
            pygame.event.pump()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                running = False
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS]:
                        print(f"Debug: Attempting to zoom in from {self.zoom_level}")
                        self.update_map_dimensions(1)
                        print(f"Debug: New zoom level: {self.zoom_level}")
                    elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                        print(f"Debug: Attempting to zoom out from {self.zoom_level}")
                        self.update_map_dimensions(-1)
                        print(f"Debug: New zoom level: {self.zoom_level}")

            scroll_x = scroll_y = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                scroll_x -= self.scroll_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                scroll_x += self.scroll_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                scroll_y += self.scroll_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                scroll_y -= self.scroll_speed
            self.camera_x = max(min(self.camera_x + scroll_x, self.max_camera_x), self.min_camera_x)
            self.camera_y = min(max(self.camera_y - scroll_y, self.max_camera_y), self.min_camera_y)

            self.screen.fill((0, 0, 0))
            self.screen.blit(
                self.tilemap_surface,
                (0, 0),
                area=pygame.Rect(self.camera_x, self.camera_y, self.window_width, self.window_height),
            )
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_x = self.camera_x + mouse_x
            world_y = self.camera_y + mouse_y
            tile_x = world_x // self.zoom_level
            tile_y = world_y // self.zoom_level
            if 0 <= tile_y < self.rows and 0 <= tile_x < self.cols:
                tile = self.map.world[tile_y][tile_x]
                # If tile is an array, use its first element.
                if isinstance(tile, list):
                    tile = tile[0]
                hover_rect = pygame.Rect(
                    tile_x * self.zoom_level - self.camera_x,
                    tile_y * self.zoom_level - self.camera_y,
                    self.zoom_level,
                    self.zoom_level,
                )
                pygame.draw.rect(self.screen, (255, 0, 0), hover_rect, 2)
                tile_info = self.map.get_tile_info(tile)
                text_surface = self.font.render(str(tile_info), True, (255, 255, 255))
                self.screen.blit(text_surface, (mouse_x + 10, mouse_y - text_surface.get_height() + 10))
            self.screen.blit(self.draw_resources(), (0, 0))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()
