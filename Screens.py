import pygame
pygame.init()
font = pygame.font.SysFont(None, 32)


class BaseScreen:
    def __init__(self, screen, left, top, width, height):
        self.name = "BaseScreen"
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def render_multiline_text(self, screen, font, messages, left, top, line_spacing=2):
        y = top
        for message in messages:
            text_surface = font.render(message, True, (0, 0, 0))
            screen.blit(text_surface, (left + 10, y + 10))
            y += text_surface.get_height() + line_spacing

    def display(self, text="", messages=[], add_overlay=False):
        if add_overlay:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 50))  # Black with alpha
            self.screen.blit(overlay, (0, 0))

        popup_rect = pygame.Rect(self.left, self.top, self.width, self.height)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), popup_rect, 3)
        if text:
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=popup_rect.center)
            self.screen.blit(text_surface, text_rect)
        else:
            self.render_multiline_text(self.screen, font, messages, self.left, self.top)

class ResourcesScreen(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.name = "ResourcesScreen"

    def display(self):
        super().display()
        print("Displaying resources information.")