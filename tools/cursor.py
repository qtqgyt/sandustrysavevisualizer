import pygame

from tools.tool import Tool


class Cursor(Tool):
    def __init__(self) -> None:
        super().__init__()

    def process_keydown(self, window, key):
        pass

    def draw_resources(self, window) -> None:
        gold_text = window.font.render(f"Gold: {window.map.gold}", True, (255, 215, 0))
        fluxite_text = window.font.render(f"Fluxite: {window.map.fluxite}", True, (175, 0, 224))
        artifacts_text = window.font.render(f"Artifacts: {window.map.artifacts}/2", True, (45, 197, 214))

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
        window.screen.blit(resources_hud, (0, 0))

    def draw_hotbar(self, window):
        # Hotbar
        slot_width = 60
        margin = 10
        hotbar_height = slot_width + (margin * 2)
        screen_width = window.screen.get_width()
        hotbar_y = window.screen.get_height() - hotbar_height

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
        window.screen.blit(hotbar_surface, (start_x, hotbar_y))

        for idx in range(TOTAL_SLOTS):
            slot_x = start_x + margin + idx * (slot_width + margin)
            color = (255, 215, 0) if idx == window.map.active_slot else (100, 100, 100)
            pygame.draw.rect(window.screen, color, (slot_x, hotbar_y + margin, slot_width, slot_width), 2)
            text_surface = window.font.render(str(idx), True, (255, 255, 255))
            # Position text in top-left corner with small offset
            text_x = slot_x + 4
            text_y = hotbar_y + margin + 4
            window.screen.blit(text_surface, (text_x, text_y))

    def draw_tooltip(self, window) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = (window.camera_x + mouse_x) // window.zoom_level
        y = (window.camera_y + mouse_y) // window.zoom_level
        if 0 <= y < window.rows and 0 <= x < window.cols:
            tile = window.map.get_tile(x, y)
            tile_info = window.map.get_tile_info(tile)
            text_surface = window.font.render(str(tile_info), True, (255, 255, 255))
            window.screen.blit(text_surface, (mouse_x + 10, mouse_y - text_surface.get_height() + 10))

    def render(self, window):
        super().render(window)
        self.draw_resources(window)
        self.draw_tooltip(window)

    def __str__(self) -> str:
        return "Cursor"
