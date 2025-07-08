import pygame
import uuid

from Attack import Attack
from Units.BaseUnit import Teams

BLUE = (0, 0, 255)

class SpaceTypes:
    CITY = 0
    ROAD = 1
    FOREST = 2
    MOUNTAIN = 3
    RIVER = 4
    PLAIN = 5

class BaseSpace():
    def __init__(self, x, y, type):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.units = []
        self.type = type
        if (type == SpaceTypes.CITY or type == SpaceTypes.PLAIN):
            self.move_penalty = 50
            if (type == SpaceTypes.CITY):
                self.name = 'City'
            else:
                self.name = 'Plain'
        elif type == SpaceTypes.ROAD:
            self.move_penalty = 50
            self.name = 'Road'
        elif type == SpaceTypes.FOREST:
            self.name = 'Forest'
            self.move_penalty = 150
        elif type == SpaceTypes.MOUNTAIN:
            self.name = 'Mountain'
            self.move_penalty = 300
        elif type == SpaceTypes.RIVER:
            self.name = 'River'
            self.move_penalty = 99999
        self.rect = self.create_rect(type, x, y)

    def get_info(self):
        return [f"Type: {self.name}"]

    def create_rect(self, type, x, y):
        image = get_image_for_space_type(type)
        image.convert()
        self.image = image
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

def get_current_active_unit(active_team, x, y, board):
    active_unit = None
    active_space = None
    for space in board:
        if space.rect.collidepoint(x, y):
            active_space = space
        for unit in space.units:
            # check that the mouse is hovering over the unit within the space
            if unit.rect.collidepoint(x, y) and unit.team == active_team.type:
                # If the unit is found, return the unit
                active_unit = unit
                break
    return active_unit, active_space

def restore_movement_units(board, active_team):
    for space in board:
        for unit in space.units:
            if unit.team == active_team.type:
                unit.movement = unit.initial_movement  # Reset movement for the unit

def snap_to_space(active_team, board, possible_dest_spaces, unit, dragged_from_space: BaseSpace):
    for space in board:
        if (abs(unit.rect.centerx - space.rect.centerx) < 40) and (abs(unit.rect.centery - space.rect.centery) < 40):
            unit.rect.center = space.rect.center
            if space.id in possible_dest_spaces:
                centre_active_space = (dragged_from_space.rect.centerx, dragged_from_space.rect.centery)
                centre_current_space = (space.rect.centerx, space.rect.centery)
                unit.movement -= total_terrain_move_penalty(unit, centre_active_space, centre_current_space, board)
                if len(space.units) > 0 and space.units[0].team != unit.team:
                    defeated = Attack(unit, space.units[0]).execute()
                    if not defeated:
                        # If the attack did not defeat the defender, snap back to start
                        snap_back_to_start(unit, dragged_from_space)
                        break
                    else:
                        space.remove_unit(space.units[0])
                        space.add_unit(unit)
                        if space.type == SpaceTypes.CITY:
                            active_team.owned_cities.append(space)
                else:
                    space.add_unit(unit)
                    if space.type == SpaceTypes.CITY:
                        active_team.owned_cities.append(space)
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

def remove_all_unit_hilights(board, screen, exclude=None):
    for space in board:
        for unit in space.units:
            if exclude and unit.id == exclude.id:
                continue
            if unit.image is not None:
                original_unit_position = unit.position
                if unit.team == Teams.WOLF:
                    if unit.name == 'Soldier':
                        original_unit_image = pygame.image.load('images\\units\\soldier-wolf.png')
                    else:
                        original_unit_image = pygame.image.load('images\\units\\jet-wolf.png')
                elif unit.team == Teams.BARBARIAN:
                    if unit.name == 'Soldier':
                        original_unit_image = pygame.image.load('images\\units\\soldier-barbarian.png')
                    else:
                        original_unit_image = pygame.image.load('images\\units\\jet-barbarian.png')
                original_unit_image.convert()
                unit.image = original_unit_image
                unit.rect = original_unit_image.get_rect()
                unit.rect.center = original_unit_position
                screen.blit(original_unit_image, unit.rect)

def check_hover_unit(active_team, screen, board, mouse_position):
    for space in board:
        for unit in space.units:
            if unit.rect.collidepoint(mouse_position) and unit.team == active_team.type:
                original_unit_position = unit.position
                if unit.team == Teams.WOLF:
                    if unit.name == 'Soldier':
                        hovered_unit_image = pygame.image.load('images\\units\\soldier-wolf-hover.png')
                    else:
                        hovered_unit_image = pygame.image.load('images\\units\\jet-wolf-hover.png')
                elif unit.team == Teams.BARBARIAN:
                    if unit.name == 'Soldier':
                        hovered_unit_image = pygame.image.load('images\\units\\soldier-barbarian-hover.png')
                    else:
                        hovered_unit_image = pygame.image.load('images\\units\\jet-barbarian-hover.png')
                hovered_unit_image.convert()
                unit.image = hovered_unit_image
                unit.rect = hovered_unit_image.get_rect()
                unit.rect.center = original_unit_position
                screen.blit(hovered_unit_image, unit.rect)
                remove_all_unit_hilights(board, screen, exclude=unit)
                return unit

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

