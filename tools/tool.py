import pygame

from map import Map


class Tool:
    def process_keys(self, window) -> None:
        scroll_x = scroll_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            scroll_x -= window.scroll_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            scroll_x += window.scroll_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            scroll_y += window.scroll_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            scroll_y -= window.scroll_speed
        window.camera_x = max(min(window.camera_x + scroll_x, window.max_camera_x), window.min_camera_x)
        window.camera_y = min(max(window.camera_y - scroll_y, window.max_camera_y), window.min_camera_y)

    def process_keydown(self, window, key) -> None: ...
    def render(self, window) -> None: ...
    def process_mouse(self, window) -> None: ...
    def process_click(self, map: Map, cursor: tuple[int, int]) -> tuple[bool, dict | None]: ...
