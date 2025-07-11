import pygame
from Units.Spaces import City
import uuid
BLUE = (0, 0, 255)

class Teams():
    WOLF = 1
    BARBARIAN = 2

class BaseUnit():
    def __init__(self, x, y, team):
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

    def get_info(self, unit_stack):
        unit_stack_label = ""
        if unit_stack:
            unit_stack_label = [unit.name + ";" for unit in unit_stack]
        return [f"Name: {self.name}", f"Team: {self.team_name}", f"Health: {self.health}, " \
               f"Attack Power: {self.attack_power}", f"Defense Power: {self.defense_power}, " \
               f"Movement: {self.movement}", f"Unit Stack: {unit_stack_label}"]

    def draw(self, screen, hilight=False):
        if hilight:
            pygame.draw.rect(screen, BLUE, self.rect, 100, border_radius=100)
        else:
            pygame.draw.rect(screen, BLUE, self.rect, 2)
        screen.blit(self.image, self.rect)

    def create_rect(self):
        if self.team == Teams.WOLF:
            img = pygame.image.load(f'images\\units\\{self.name}-wolf.png')
        elif self.team == Teams.BARBARIAN:
            img = pygame.image.load(f'images\\units\\{self.name}-barbarian.png')
        img.convert()
        self.image = img
        # Draw rectangle around the image
        rect = img.get_rect()
        rect.center = self.position
        return rect

    def get_target_image(self):
        if self.team == Teams.WOLF:
            return pygame.image.load(f'images\\units\\{self.name}-wolf-hover-firing.png')
        elif self.team == Teams.BARBARIAN:
            return pygame.image.load(f'images\\units\\{self.name}-barbarian-hover-firing.png')

    def get_hovered_image(self):
        if self.team == Teams.WOLF:
            return pygame.image.load(f'images\\units\\{self.name}-wolf-hover.png')
        elif self.team == Teams.BARBARIAN:
            return pygame.image.load(f'images\\units\\{self.name}-barbarian-hover.png')

    def get_unit_image(self):
        if self.team == Teams.WOLF:
            return pygame.image.load(f'images\\units\\{self.name}-wolf.png')
        elif self.team == Teams.BARBARIAN:
            return pygame.image.load(f'images\\units\\{self.name}-barbarian.png')

class Soldier(BaseUnit):
    def __init__(self, x, y, team):
        self.name = "Soldier"
        super().__init__(x, y, team)
        self.health = 100
        self.can_shoot = True
        self.range = 250

class Jet(BaseUnit):
    def __init__(self, x, y, team):
        self.name = "Jet"
        super().__init__(x, y, team)
        self.health = 100
        self.fly = True
        self.can_shoot = True
        self.range = 400
        self.attack_power = 50
        self.defense_power = 5
        self.movement = 710
        self.initial_movement = 710

class Settler(BaseUnit):
    def __init__(self, x, y, team):
        self.name = "Settler"
        super().__init__(x, y, team)
        self.health = 5
        self.attack_power = 0
        self.defense_power = 0
        self.movement = 200
        self.initial_movement = 100

    def settle(self, current_space, team, board):
        if current_space.name != "City" and current_space.name != "River" and current_space.name != "Mountain":
            new_space = City(current_space.rect.centerx, current_space.rect.centery)
            new_space.owner = team
            new_space.units = []
            number_on_board = 0
            for space in board:
                if space.id == current_space.id:
                    break
                number_on_board += 1
            board[number_on_board] = new_space
            team.owned_cities.append(new_space)