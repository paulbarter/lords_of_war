import pygame

BLUE = (0, 0, 255)

class SpaceTypes:
    CITY = 0
    ROAD = 1
    FOREST = 2
    MOUNTAIN = 3
    RIVER = 4
    PLAIN = 5

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

    def remove_unit(self, unit_to_remove):
        new_units = []
        for unit in self.units:
            if unit.id == unit_to_remove.id:
                continue
            else:
                new_units.append(unit)
        self.units = new_units

    def draw_units(self, screen):
        for unit in self.units:
            unit.draw(screen)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(self.image, self.rect)
        if len(self.units) > 0:
            self.draw_units(screen)

def get_current_active_space(x, y, board):
    for space in board:
        if space.rect.collidepoint(x, y):
            if len(space.units) > 0:
                # If the space has units, return the space
                return space
    return None

def get_current_active_unit(x, y, board):
    for space in board:
        for unit in space.units:
            # check that the mouse is hovering over the unit within the space
            if unit.rect.collidepoint(x, y):
                # If the unit is found, return the unit
                return unit, space
    return None, None

def snap_to_space(board, unit, dragged_from_space: BaseSpace):
    for space in board:
        if (abs(unit.rect.centerx - space.rect.centerx) < 40) and (abs(unit.rect.centery - space.rect.centery) < 40):
            unit.rect.center = space.rect.center
            if dragged_from_space.id != space.id:
                # only move the unit if it is not the same space
                space.add_unit(unit)
                dragged_from_space.remove_unit(unit)
            break

def hover_space(board, screen, active_space, x, y):
    for space in board:
        if space.rect.collidepoint(x, y) and space.id != active_space.id:
            centre_active_space = (active_space.rect.centerx, active_space.rect.centery)
            distance = pygame.math.Vector2(centre_active_space).distance_to((x, y))
            if distance > 150:
                new_image = pygame.image.load('images\\road-hover-invalid.png').convert()
            else:
                new_image = pygame.image.load('images\\road-hover-valid.png').convert()
            space.image = new_image
            space.draw(screen)

