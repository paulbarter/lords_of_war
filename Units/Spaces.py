import pygame

from Attack import Attack

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
        if (type == SpaceTypes.CITY or type == SpaceTypes.PLAIN):
            self.move_penalty = 50
        elif type == SpaceTypes.ROAD:
            self.move_penalty = 50
        elif type == SpaceTypes.FOREST:
            self.move_penalty = 150
        elif type == SpaceTypes.MOUNTAIN:
            self.move_penalty = 300
        elif type == SpaceTypes.RIVER:
            self.move_penalty = 99999
        self.rect = self.create_rect(type, x, y)

    def create_rect(self, type, x, y):
        image = get_image_for_space_type(type)
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

def snap_to_space(board, possible_dest_spaces, unit, dragged_from_space: BaseSpace):
    for space in board:
        if (abs(unit.rect.centerx - space.rect.centerx) < 40) and (abs(unit.rect.centery - space.rect.centery) < 40):
            unit.rect.center = space.rect.center
            if space.id in possible_dest_spaces:
                if len(space.units) > 0 and space.units[0].team != unit.team:
                    defeated = Attack(unit, space.units[0]).execute()
                    if not defeated:
                        # If the attack did not defeat the defender, snap back to start
                        snap_back_to_start(unit, dragged_from_space)
                        break
                    else:
                        space.remove_unit(space.units[0])
                        space.add_unit(unit)
                else:
                    space.add_unit(unit)
                dragged_from_space.remove_unit(unit)
            break

def snap_back_to_start(current_active_unit, active_space):
    current_active_unit.rect.center = active_space.rect.center

def remove_movement_hilights(board, screen):
    for space in board:
        new_image = get_image_for_space_type(space.type)
        space.image = new_image
        space.draw(screen)
        space.draw_units(screen)

def is_space_adjacent(space1, space2):
    # bug here when go from corner to corner to corner
    centre_space1 = (space1.rect.centerx, space1.rect.centery)
    centre_space2 = (space2.rect.centerx, space2.rect.centery)
    distance = pygame.math.Vector2(centre_space1).distance_to(centre_space2)
    return distance < 110  # Assuming spaces are close enough if within 100 pixels

def get_image_for_space_type(space_type, hover=False, valid=True):
    if space_type == SpaceTypes.CITY:
        if hover:
            if not valid:
                return pygame.image.load('images\\city-hover-invalid.png').convert()
            return pygame.image.load('images\\city-hover.png').convert()
        return pygame.image.load('images\\city.png').convert()
    elif space_type == SpaceTypes.PLAIN:
        if hover:
            if not valid:
                return pygame.image.load('images\\plain-hover-invalid.png').convert()
            return pygame.image.load('images\\plain-hover.png').convert()
        return pygame.image.load('images\\plain.png').convert()
    elif space_type == SpaceTypes.ROAD:
        if hover:
            if not valid:
                return pygame.image.load('images\\road-hover-invalid.png').convert()
            return pygame.image.load('images\\road-hover.png').convert()
        return pygame.image.load('images\\road.png').convert()
    elif space_type == SpaceTypes.FOREST:
        if hover:
            if not valid:
                return pygame.image.load('images\\forest-hover-invalid.png').convert()
            return pygame.image.load('images\\forest-hover.png').convert()
        return pygame.image.load('images\\forest.png').convert()
    elif space_type == SpaceTypes.MOUNTAIN:
        if hover:
            if not valid:
                return pygame.image.load('images\\mountain-hover-invalid.png').convert()
            return pygame.image.load('images\\mountain-hover.png').convert()
        return pygame.image.load('images\\mountain.png').convert()
    elif space_type == SpaceTypes.RIVER:
        if hover:
            if not valid:
                return pygame.image.load('images\\river-hover-invalid.png').convert()
            return pygame.image.load('images\\river-hover.png').convert()
        return pygame.image.load('images\\river.png').convert()

def total_terrain_move_penalty(unit, start_point, end_point, board):
    # Calculate the move penalty based on the terrain type between two points
    total_move_penalty = 0
    for space in board:
        if space.rect.clipline(start_point, end_point):
            if unit.fly:
                total_move_penalty += 50
            else:
                total_move_penalty += space.move_penalty
    return total_move_penalty

def hover_space(board, screen, unit, active_space, x, y):
    possible_dest_space_ids = set()
    for space in board:
        if space.rect.collidepoint(x, y) and space.id != active_space.id:
            centre_active_space = (active_space.rect.centerx, active_space.rect.centery)
            centre_current_space = (space.rect.centerx, space.rect.centery)
            distance = pygame.math.Vector2(centre_active_space).distance_to(centre_current_space)
            terrain_penalty = total_terrain_move_penalty(unit, centre_active_space, centre_current_space, board)
            # show_popup(screen, f"distance {distance} penalty: {terrain_penalty}", font)
            if distance <= (unit.movement - terrain_penalty):
                new_image = get_image_for_space_type(space.type, hover=True)
                possible_dest_space_ids.add(space.id)
            else:
                new_image = get_image_for_space_type(space.type, hover=True, valid=False)
            space.image = new_image
            space.draw(screen)
    return list(possible_dest_space_ids)

