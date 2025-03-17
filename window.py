import math
import sys
from config import config
from loguru import logger

from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

from map import Map
from tools import ToolBelt


class window:
    def __init__(self, title: str, map: Map) -> None:
        self.map = map
        self.tool_belt = ToolBelt()
        self.zoom_level = config.zoom_level
        self.window_width, self.window_height = config.window_x, config.window_y

        pygame.init()

        ICON_SIZE = 32
        pygame.display.set_icon(self._create_magnifying_glass(ICON_SIZE, filled=True))

        CURSOR_SIZE = 24
        cursor_surface = self._create_magnifying_glass(CURSOR_SIZE)
        cursor = pygame.cursors.Cursor((CURSOR_SIZE // 2, CURSOR_SIZE // 2), cursor_surface)
        pygame.mouse.set_cursor(cursor)

        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

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

    def _draw_new_tilemap_surface(self) -> None:
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

    def _update_map_dimensions(self, change: int) -> bool:
        old_zoom = self.zoom_level
        self.zoom_level = max(1, min(4, self.zoom_level + change))  # Increased zoom factor
        if old_zoom == self.zoom_level:
            return False
        logger.debug(f"Updating dimensions - Current zoom: {self.zoom_level}")
        self.tilemap_width = self.cols * self.zoom_level
        self.tilemap_height = self.rows * self.zoom_level
        return True

    def _update_camera(self, amount: int) -> None:
        y_offset = self.window_height // 2
        x_offset = self.window_width // 2

        old_zoom = self.zoom_level - amount

        self.camera_y = (self.camera_y + y_offset) // (old_zoom) * self.zoom_level - y_offset
        self.camera_x = (self.camera_x + x_offset) // (old_zoom) * self.zoom_level - x_offset

    def _process_zoom(self, amount: int):
        if self._update_map_dimensions(amount):
            self.draw_loading_overlay()
            self._draw_new_tilemap_surface()
            self._calculate_camera_borders()
            self._update_camera(amount)

    def render(self):
        running = True
        clock = pygame.time.Clock()

        self.draw_loading_overlay()
        self._draw_new_tilemap_surface()

        while running:
            pygame.event.pump()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                    case pygame.VIDEORESIZE:
                        self.window_width, self.window_height = event.size
                        self._calculate_camera_borders()
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE | pygame.K_q:
                                running = False
                                break
                            case pygame.K_PLUS | pygame.K_KP_PLUS | pygame.K_EQUALS:
                                logger.debug(f"Debug: Attempting to zoom in from {self.zoom_level}")
                                self._process_zoom(1)
                                logger.debug(f"Debug: New zoom level: {self.zoom_level}")
                            case pygame.K_MINUS | pygame.K_KP_MINUS:
                                logger.debug(f"Debug: Attempting to zoom out from {self.zoom_level}")
                                self._process_zoom(-1)
                                logger.debug(f"Debug: New zoom level: {self.zoom_level}")
                            case _:
                                self.tool_belt.process_keydown(self, event.key)
                    case _:
                        self.tool_belt.handle_event(self, event)

            self.tool_belt.process_keys(self)

            self.screen.fill((0, 0, 0))
            self.screen.blit(
                self.tilemap_surface,
                (0, 0),
                area=pygame.Rect(self.camera_x, self.camera_y, self.window_width, self.window_height),
            )

            self.tool_belt.render(self)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()
