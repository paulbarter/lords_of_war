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

    def display(self, message):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))  # Black with alpha
        self.screen.blit(overlay, (0, 0))

        # Draw popup rectangle
        popup_rect = pygame.Rect(self.left, self.top, self.width, self.height)
        # popup_rect.center = self.screen.get_rect().center
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), popup_rect, 3)

        # Render message
        text_surface = font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=popup_rect.center)
        self.screen.blit(text_surface, text_rect)
        # pygame.display.update()


class ResourcesScreen(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.name = "ResourcesScreen"

    def display(self):
        super().display()
        print("Displaying resources information.")