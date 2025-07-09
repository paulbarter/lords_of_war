import pygame
import uuid
BLUE = (0, 0, 255)

class Teams():
    WOLF = 1
    BARBARIAN = 2

class BaseUnit():
    def __init__(self, x, y, team):
        self.name = "Soldier"
        self.team = team
        if team == Teams.WOLF:
            self.team_name = "Wolf"
        elif team == Teams.BARBARIAN:
            self.team_name = "Barbarian"
        self.id = uuid.uuid4()
        self.can_shoot = False
        self.range = 0
        self.health = 20
        self.fly = False
        self.attack_power = 10
        self.defense_power = 5
        self.movement = 200
        self.initial_movement = 200
        self.position = (x, y)
        self.image = None
        self.rect = self.create_rect()

    def get_info(self):
        return [f"Name: {self.name}", f"Team: {self.team_name}", f"Health: {self.health}, " \
               f"Attack Power: {self.attack_power}", f"Defense Power: {self.defense_power}, " \
               f"Movement: {self.movement}"]

    def create_rect(self):
        if self.team == Teams.WOLF:
            img = pygame.image.load('images\\units\\soldier-wolf.png')
        elif self.team == Teams.BARBARIAN:
            img = pygame.image.load('images\\units\\soldier-barbarian.png')
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

    def get_target_image(self):
        if self.team == Teams.WOLF:
            return pygame.image.load('images\\units\\soldier-wolf-hover-firing.png')
        elif self.team == Teams.BARBARIAN:
            return pygame.image.load('images\\units\\soldier-barbarian-hover-firing.png')

class Jet(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.name = "Jet"
        self.id = uuid.uuid4()
        self.health = 100
        self.fly = True
        self.can_shoot = True
        self.range = 400
        self.attack_power = 50
        self.defense_power = 5
        self.movement = 710
        self.initial_movement = 710
        self.position = (x, y)
        self.image = None
        self.rect = self.create_rect()

    def create_rect(self):
        if self.team == Teams.WOLF:
            img = pygame.image.load('images\\units\\jet-wolf.png')
        elif self.team == Teams.BARBARIAN:
            img = pygame.image.load('images\\units\\jet-barbarian.png')
        img.convert()
        self.image = img
        # Draw rectangle around the image
        rect = img.get_rect()
        rect.center = self.position
        return rect

    def get_target_image(self):
        if self.team == Teams.WOLF:
            return pygame.image.load('images\\units\\jet-target-wolf.png')