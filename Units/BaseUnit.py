import pygame
import uuid

BLUE = (0, 0, 255)

class BaseUnit():
    def __init__(self, x, y):
        self.name = "BaseUnit"
        self.id = uuid.uuid4()
        self.health = 20
        self.fly = False
        self.attack_power = 10
        self.defense_power = 5
        self.movement = 200
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

    def draw(self, screen, hilight=False):
        if hilight:
            pygame.draw.rect(screen, BLUE, self.rect, 100, border_radius=100)
        else:
            pygame.draw.rect(screen, BLUE, self.rect, 2)
        screen.blit(self.image, self.rect)

class Jet(BaseUnit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = "Jet"
        self.id = uuid.uuid4()
        self.health = 100
        self.fly = True
        self.attack_power = 10
        self.defense_power = 5
        self.movement = 710
        self.position = (x, y)
        self.image = None
        self.rect = self.create_rect()

    def create_rect(self):
        img = pygame.image.load('images\\jet.png')
        img.convert()
        self.image = img
        # Draw rectangle around the image
        rect = img.get_rect()
        rect.center = self.position
        return rect