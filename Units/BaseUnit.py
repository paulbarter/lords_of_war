import pygame

BLUE = (0, 0, 255)

class BaseUnit():
    def __init__(self, x, y):
        self.name = "BaseUnit"
        self.health = 100
        self.attack_power = 10
        self.defense_power = 5
        self.position = (x, y)
        self.image = None
        self.rect = self.create_rect()

    def create_rect(self):
        img = pygame.image.load('images\\soldier.png')
        img.convert()
        self.image = img
        # Draw rectangle around the image
        rect = img.get_rect()
        rect.center = self.position
        return rect

    def draw(self, screen, x, y):
        self.rect.center = x, y
        pygame.draw.rect(screen, BLUE, self.rect, 2)
        screen.blit(self.image, self.rect)