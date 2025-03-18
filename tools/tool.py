import pygame


class Tool:
    def process(self, window) -> None:
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

    def render(self, window) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = (window.camera_x + mouse_x) // window.zoom_level
        y = (window.camera_y + mouse_y) // window.zoom_level
        if 0 <= y < window.rows and 0 <= x < window.cols:
            hover_rect = pygame.Rect(
                x * window.zoom_level - window.camera_x,
                y * window.zoom_level - window.camera_y,
                window.zoom_level,
                window.zoom_level,
            )
            pygame.draw.rect(window.screen, (255, 0, 0), hover_rect, 2)
        tool_name = window.font.render(str(self), True, (255, 255, 255), (50, 50, 50, 50))
        window.screen.blit(tool_name, (10, window.window_height - tool_name.get_height() - 10))

    def handle_event(self, window, event) -> tuple[bool, dict]:
        return (False, {})

    def activate(self, window) -> None: ...
    def deactivate(self, window) -> None: ...

    def __str__(self) -> str:
        return "Unknown"
