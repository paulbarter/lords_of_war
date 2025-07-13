import pygame
import uuid

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
    def __init__(self, x, y, type):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.owner = None  # The team that owns the space, if any
        self.units = []
        self.type = type
        self.rect = self.create_rect(x, y)
        self.move_penalty = 0

    def to_dict(self):
        return {
            'id': str(self.id),
            'x': self.x,
            'y': self.y,
            'type': self.type,
            'name': getattr(self, 'name', None),
            'owner': self.owner.name if self.owner else None,
            'units': [unit.to_dict() for unit in self.units],
            'move_penalty': self.move_penalty
        }

    def get_unit_object_by_name(self, unit_name, x, y, team):
        from Units.BaseUnit import Soldier, Settler, Jet
        if unit_name == "Soldier":
            return Soldier(x, y, team)
        elif unit_name == "Settler":
            return Settler(x, y, team)
        elif unit_name == "Jet":
            return Jet(x, y, team)

    def from_dict(self, data, team_wolf, team_barbarian):
        self.id = uuid.UUID(data['id'])
        self.x = data['x']
        self.y = data['y']
        self.type = data['type']
        self.name = data.get('name', None)
        owner_name = data.get('owner', None)
        if owner_name:
            if owner_name == 'Wolf':
                self.owner = team_wolf
            else:
                self.owner = team_barbarian
        else:
            self.owner = None
        self.units = []
        for unit in data['units']:
            unit_object = self.get_unit_object_by_name(unit['name'], unit['position'][0], unit['position'][1], unit['team'])
            self.units.append(unit_object)
        self.move_penalty = data.get('move_penalty', 0)

    def get_info(self):
        return [f"Type: {self.name}"]

    def create_rect(self, x, y):
        image = get_image_for_space(self)
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

    def draw_units(self, screen, hovered_unit=None):
        for unit in self.units:
            unit.stacked = False  # Reset stacked state for all units
            unit.draw(screen)
        # only draw the first unit in the stack because that is the only unit available for selection
        if self.units:
            if len(self.units) > 1:
                self.units[0].stacked = True
            if hovered_unit and self.units[0].id == hovered_unit.id:
                self.units[0].draw(screen, hovered_unit=hovered_unit)
            else:
                self.units[0].draw(screen)

    def draw(self, screen, hovered_unit=None):
        if self.type == SpaceTypes.CITY and self.owner:
            new_image = get_image_for_space(self, hover=False, owner=self.owner)
            new_image.convert()
            self.image = new_image
            self.rect = new_image.get_rect()
            self.rect.center = self.x, self.y
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(self.image, self.rect)
        if len(self.units) > 0:
            self.draw_units(screen, hovered_unit=hovered_unit)

    def get_hover_firing_image(self, enemy, valid):
        if enemy and valid:
            return pygame.image.load(f'images\\{self.name}-hover-enemy-firing.png').convert()
        if valid:
            return pygame.image.load(f'images\\{self.name}-hover-firing.png').convert()
        else:
            return pygame.image.load(f'images\\{self.name}-hover-invalid.png').convert()

    def get_hover_image(self):
        return pygame.image.load(f'images\\{self.name}-hover.png').convert()

    def get_moving_image_hover(self, valid, enemy):
        if not valid:
            return pygame.image.load(f'images\\{self.name}-hover-invalid.png').convert()
        if enemy:
            return pygame.image.load(f'images\\{self.name}-hover-enemy.png').convert()
        else:
            return pygame.image.load(f'images\\{self.name}-hover.png').convert()

    def get_owner_image(self, owner):
        if owner.name == 'Wolf':
            return pygame.image.load(f'images\\{self.name}-wolf.png').convert()
        elif owner.name == 'Barbarian':
            return pygame.image.load(f'images\\{self.name}-barbarian.png').convert()

    def get_regular_image(self):
        return pygame.image.load(f'images\\{self.name}.png').convert()

class Plain(BaseSpace):
    def __init__(self, x, y):
        self.name = 'Plain'
        super().__init__(x, y, SpaceTypes.PLAIN)
        self.move_penalty = 50

class Road(BaseSpace):
    def __init__(self, x, y):
        self.name = 'Road'
        super().__init__(x, y, SpaceTypes.ROAD)
        self.move_penalty = 0

class Forest(BaseSpace):
    def __init__(self, x, y):
        self.name = 'Forest'
        super().__init__(x, y, SpaceTypes.FOREST)

class Mountain(BaseSpace):
    def __init__(self, x, y):
        self.name = 'Mountain'
        super().__init__(x, y, SpaceTypes.MOUNTAIN)
        self.move_penalty = 300

class City(BaseSpace):
    def __init__(self, x, y):
        self.name = 'City'
        super().__init__(x, y, SpaceTypes.CITY)
        self.move_penalty = 50
        self.owner = None  # The team that owns the city
        self.units = []  # Units stationed in the city

    def get_info(self):
        return [f"Type: {self.name}", f"Owner: {self.owner.name if self.owner else 'None'}",]

class River(BaseSpace):
    def __init__(self, x, y):
        self.name = 'River'
        super().__init__(x, y, SpaceTypes.RIVER)
        self.move_penalty = 99999  # Cannot cross river without a boat or flying unit

def calculate_city_occupied(active_team, inactive_team, city):
    if city.owner and city.owner != active_team:
        active_team.owned_cities.append(city)
        inactive_team.owned_cities.remove(city)
    elif not city.owner:
        active_team.owned_cities.append(city)
    city.owner = active_team

def get_current_active_unit(previously_active_unit, active_team, x, y, board):
    active_unit = None
    active_space = None
    unit_stack = []
    get_bottom_of_stack = False
    for space in board:
        if space.rect.collidepoint(x, y):
            active_space = space
        for unit in space.units:
            # check that the mouse is hovering over the unit within the space
            if unit.rect.collidepoint(x, y) and unit.team == active_team.type:
                active_unit = unit
                if len(space.units) > 1:
                    unit_stack = space.units
                    if unit.stack_clicked:  # allow one click in the stack before changing the order
                        # If the previously active unit is the same as the current unit, get bottom unit, to allow selecting different unit
                        get_bottom_of_stack = True
                        unit.stack_clicked = False
                        break
                    else:
                        unit.stack_clicked = True
                        break
                else:
                    # If the unit is found, return the unit
                    active_unit = unit
                    break
    if get_bottom_of_stack:
        # start with last element
        new_stack = [unit_stack[len(unit_stack)-1]]
        count = 0
        for unit in unit_stack:
            new_stack.append(unit)
            count += 1
        # shave off the last element because it was added twice
        new_stack = new_stack[:-1]  # Reverse the stack to have the bottom unit first
        active_space.units = new_stack
        unit_stack = new_stack
        active_unit = new_stack[0]
    return active_unit, active_space, unit_stack

def restore_movement_units(board, active_team):
    for space in board:
        for unit in space.units:
            if unit.team == active_team.type:
                unit.movement = unit.initial_movement  # Reset movement for the unit

def shoot_at_space(board, unit, mouse_position):
    if unit.movement <= 0 or not unit.can_shoot:
        return
    for space in board:
        if space.rect.collidepoint(mouse_position):
            if len(space.units) > 0 and space.units[0].team != unit.team:
                unit.movement = 0  # Reset movement after firing
                defeated = Attack(unit, space.units[0]).execute()
                if defeated:
                    space.remove_unit(space.units[0])

def snap_to_space(active_team, inactive_team, board, possible_dest_spaces, unit, dragged_from_space: BaseSpace):
    for space in board:
        if (abs(unit.rect.centerx - space.rect.centerx) < 45) and (abs(unit.rect.centery - space.rect.centery) < 45):
            unit.rect.center = space.rect.center
            if space.id in possible_dest_spaces:
                centre_active_space = (dragged_from_space.rect.centerx, dragged_from_space.rect.centery)
                centre_current_space = (space.rect.centerx, space.rect.centery)
                unit.movement -= total_terrain_move_penalty(unit, centre_active_space, centre_current_space, board)
                if len(space.units) > 0 and space.units[0].team != unit.team:
                    defeated = Attack(unit, space.units[0]).execute()
                    if defeated:
                        space.remove_unit(space.units[0])
                    else:
                        # If the attack did not defeat the defender, snap back to start
                        # TODO make sure don't snap back if unit moved from further than 1 space away (dont allow moving
                        # right into another unit unless adjacent)
                        snap_back_to_start(unit, dragged_from_space)
                        break
                else:
                    space.add_unit(unit)
                if space.type == SpaceTypes.CITY:
                    calculate_city_occupied(active_team, inactive_team, space)
                dragged_from_space.remove_unit(unit)
            break

def snap_back_to_start(current_active_unit, active_space):
    current_active_unit.rect.center = active_space.rect.center

def remove_movement_hilights(board, screen, exclude=None):
    for space in board:
        if exclude and space.id == exclude.id:
            continue
        new_image = get_image_for_space(space)
        space.image = new_image
        space.draw(screen)
        space.draw_units(screen)

def is_space_adjacent(space1, space2):
    # bug here when go from corner to corner to corner
    centre_space1 = (space1.rect.centerx, space1.rect.centery)
    centre_space2 = (space2.rect.centerx, space2.rect.centery)
    distance = pygame.math.Vector2(centre_space1).distance_to(centre_space2)
    return distance < 110  # Assuming spaces are close enough if within 100 pixels

def get_image_for_space(space, hover=False, valid=True, enemy=None, firing=False, owner=None):
    if hover:
        if firing:
            # valid here means in range
            return space.get_hover_firing_image(enemy, valid)
        else:
            return space.get_moving_image_hover(valid, enemy)
    if owner:
        return space.get_owner_image(owner)
    return space.get_regular_image()

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

def handle_hover(board, screen, current_active_unit, active_space, current_active_team, event, firing):
    current_hovered_space = possible_dest_space_ids = None
    if current_active_unit and active_space:
        if not firing:
            current_active_unit.rect.move_ip(event.rel)
            current_hovered_space, possible_dest_space_ids = hover_space(board, screen, current_active_unit,
                                                                         active_space,
                                                                         event.pos[0], event.pos[1], firing=False)
        else:
            current_hovered_space, possible_dest_space_ids = \
                hover_space(board, screen, current_active_unit, active_space,
                            event.pos[0], event.pos[1], firing=firing)
    hovered_unit = check_hover_unit(current_active_team, screen, board, event.pos, firing=True)
    return current_hovered_space, possible_dest_space_ids

def remove_all_unit_hilights(board, screen, exclude=None):
    for space in board:
        for unit in space.units:
            if exclude and unit.id == exclude.id:
                continue
            if unit.image is not None:
                original_unit_position = unit.rect.center
                original_unit_image = unit.get_unit_image()
                original_unit_image.convert()
                unit.image = original_unit_image
                unit.rect = original_unit_image.get_rect()
                unit.rect.center = original_unit_position
                screen.blit(original_unit_image, unit.rect)

def check_hover_unit(active_team, screen, board, mouse_position, firing=False):
    for space in board:
        for unit in space.units:
            if unit.rect.collidepoint(mouse_position) and unit.team == active_team.type:
                if firing and not unit.can_shoot:
                    continue
                original_unit_position = unit.position
                hovered_unit_image = unit.get_hovered_image()
                hovered_unit_image.convert()
                unit.image = hovered_unit_image
                unit.rect = hovered_unit_image.get_rect()
                unit.rect.center = original_unit_position
                screen.blit(hovered_unit_image, unit.rect)
                remove_all_unit_hilights(board, screen, exclude=unit)
                return unit

def handle_move(distance, unit, centre_active_space, centre_current_space, space, screen, board):
    possible_dest_space_ids = set()
    terrain_penalty = total_terrain_move_penalty(unit, centre_active_space, centre_current_space, board)
    if distance <= (unit.movement - terrain_penalty):
        enemy = None
        if space.units and space.units[0].team != unit.team:
            enemy = space.units[0]
        new_image = get_image_for_space(space, hover=True, enemy=enemy)
        possible_dest_space_ids.add(space.id)
    else:
        new_image = get_image_for_space(space, hover=True, valid=False)
    if new_image:
        space.image = new_image
        space.draw(screen)
    return list(possible_dest_space_ids)

def handle_shoot(distance, unit, centre_active_space, centre_current_space, space, screen, board):
    possible_dest_shooting_ids = set()
    new_image = None
    if distance <= (unit.range):
        enemy = None
        if space.units and space.units[0].team != unit.team:
            enemy = space.units[0]
            enemy.image = enemy.get_target_image()
        if unit.movement > 0:
            new_image = get_image_for_space(space, hover=True, enemy=enemy, firing=True)
            possible_dest_shooting_ids.add(space.id)
    else:
        new_image = get_image_for_space(space, hover=True, valid=False, firing=True)
    if new_image:
        space.image = new_image
        space.draw(screen)
    return list(possible_dest_shooting_ids)

def hover_space(board, screen, unit, active_space, x, y, firing=False):
    # Manage moving and shooting
    for space in board:
        if space.rect.collidepoint(x, y) and space.id != active_space.id:
            centre_active_space = (active_space.rect.centerx, active_space.rect.centery)
            centre_current_space = (space.rect.centerx, space.rect.centery)
            distance = pygame.math.Vector2(centre_active_space).distance_to(centre_current_space)
            if firing:
                return space, handle_shoot(distance, unit, centre_active_space, centre_current_space, space, screen, board)
            else:
                return space, handle_move(distance, unit, centre_active_space, centre_current_space, space, screen, board)

    return None, []

