import pygame

BLUE = (0, 0, 255)

class SpaceTypes:
    CITY = 0
    ROAD = 1
    FOREST = 2
    MOUNTAIN = 3
    RIVER = 4
    PLAIN = 5

def get_current_active_space(x, y, board):
    for space in board:
        if space.rect.collidepoint(x, y):
            if len(space.units) > 0:
                # If the space has units, return the space
                return space
    return None

class BaseSpace():
    def __init__(self, x, y, id, type):
        self.id = id
        self.x = x
        self.y = y
        self.units = []
        self.type = type
        self.rect = self.create_rect(type, x, y)

    def create_rect(self, type, x, y):
        if type == SpaceTypes.CITY:
            image = pygame.image.load('images\\city.png')
        elif type == SpaceTypes.PLAIN:
            image = pygame.image.load('images\\plain.png')
        else:
            image = pygame.image.load('images\\road.png')
        image.convert()
        self.image = image
        # Draw rectangle around the image
        rect = image.get_rect()
        rect.center = x, y
        return rect

    def add_unit(self, unit):
        self.units.append(unit)
        unit.position = (self.x, self.y)
        unit.rect.center = self.rect.center

    def draw_units(self, screen):
        for unit in self.units:
            unit.draw(screen, self.x, self.y)

    def draw(self, screen):
        if self.id == 1:
            pygame.draw.rect(screen, BLUE, self.rect, 2)
        elif self.id == 2:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)
        elif self.id == 3:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        elif self.id == 4:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, 2)
        elif self.id == 5:
            pygame.draw.rect(screen, (0, 255, 255), self.rect, 2)
        elif self.id == 6:
            pygame.draw.rect(screen, (255, 0, 255), self.rect, 2)
        screen.blit(self.image, self.rect)
        if len(self.units) > 0:
            self.draw_units(screen)
