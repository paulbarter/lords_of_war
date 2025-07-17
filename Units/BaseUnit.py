import pygame

from Attack import show_popup
from Units.Spaces import City
import uuid
BLUE = (0, 0, 255)

# duplicated class to avoid circular import issues
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
        self.movement = 250
        self.initial_movement = 250
        self.position = (x, y)
        self.image = None
        self.rect = self.create_rect()
        self.stacked = False
        self.stack_clicked = False
        self.is_selected = False
        self.is_hovered = False
        self.is_valid_target = False
        self.is_invalid_target = False

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "team": self.team,
            "health": self.health,
            "can_shoot": self.can_shoot,
            "range": self.range,
            "fly": self.fly,
            "attack_power": self.attack_power,
            "defense_power": self.defense_power,
            "movement": self.movement,
            "initial_movement": self.initial_movement,
            "position": self.position
        }

    def from_dict(self, data):
        self.id = uuid.UUID(data["id"])
        self.name = data["name"]
        self.team = data["team"]
        self.health = data["health"]
        self.can_shoot = data["can_shoot"]
        self.range = data["range"]
        self.fly = data["fly"]
        self.attack_power = data["attack_power"]
        self.defense_power = data["defense_power"]
        self.movement = data["movement"]
        self.initial_movement = data["initial_movement"]
        self.position = tuple(data["position"])
        self.rect = self.create_rect()

    def clone_unit(self):
        if self.name == 'Soldier':
            new_unit = Soldier(self.position[0], self.position[1], self.team)
        elif self.name == 'Settler':
            new_unit = Settler(self.position[0], self.position[1], self.team)
        elif self.name == 'Archer':
            new_unit = Archer(self.position[0], self.position[1], self.team)
        new_unit.selected = False
        new_unit.stacked = False
        return new_unit

    def get_info(self, unit_stack):
        unit_stack_label = ""
        if unit_stack:
            unit_stack_label = [unit.name + ";" for unit in unit_stack]
        return [f"Name: {self.name}", f"Team: {self.team_name}", f"Health: {self.health}, " \
               f"Attack Power: {self.attack_power}", f"Defense Power: {self.defense_power}, " \
               f"Movement: {self.movement}", f"Unit Stack: {unit_stack_label}"]

    def draw_hovered_effect(self, screen):
        highlight_color = (255, 255, 0, 128)  # RGBA: Yellow with 50% opacity
        highlight_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        highlight_surface.fill(highlight_color)
        screen.blit(highlight_surface, self.rect)

    def draw_selected_effect(self, screen):
        highlight_color = (255, 0, 0, 100)  # RGBA: Yellow with 50% opacity
        highlight_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        highlight_surface.fill(highlight_color)
        screen.blit(highlight_surface, self.rect)

    def draw_stacked_effect(self, screen):
        overlay_image = pygame.image.load("images\\units\\stack.png").convert_alpha()  # Replace with your overlay image
        overlay_rect = overlay_image.get_rect(topleft=self.rect.topleft)
        screen.blit(overlay_image, overlay_rect)

    def draw_team_effect(self, screen):
        team_img = None
        if self.team == Teams.WOLF:
            team_img = pygame.image.load(f'images\\units\\wolf.png')
        elif self.team == Teams.BARBARIAN:
            team_img = pygame.image.load(f'images\\units\\barbarian.png')
        team_img.convert_alpha()
        overlay_rect = team_img.get_rect(topleft=self.rect.topleft)
        screen.blit(team_img, overlay_rect)

    def draw_target_effect(self, screen, valid_target=False):
        if valid_target:
            target_image = pygame.image.load(f'images\\target.png')
        else:
            target_image = pygame.image.load(f'images\\target-invalid.png')
        target_image.convert_alpha()
        overlay_rect = target_image.get_rect(centerx=self.rect.centerx, centery=self.rect.centery)
        screen.blit(target_image, overlay_rect)

    def draw(self, screen, hovered_unit=None):
        screen.blit(self.image, self.rect)
        if hovered_unit:
            self.draw_hovered_effect(screen)
        if self.stacked:
            self.draw_stacked_effect(screen)
        if self.is_valid_target:
            self.draw_target_effect(screen, valid_target=True)
        elif self.is_invalid_target:
            self.draw_target_effect(screen, valid_target=False)
        if self.is_selected:
            self.draw_selected_effect(screen)
        elif self.is_hovered:
            self.draw_hovered_effect(screen)
        self.draw_team_effect(screen)

    def create_rect(self, img=None):
        if img is None:
            base_img = pygame.image.load(f'images\\units\\{self.name}.png').convert()
        self.image = base_img
        # Draw rectangle around the image
        rect = base_img.get_rect()
        rect.center = self.position
        return rect

    def get_target_image(self):
        if self.team == Teams.WOLF:
            return pygame.image.load(f'images\\units\\{self.name}-wolf-hover-firing.png')
        elif self.team == Teams.BARBARIAN:
            return pygame.image.load(f'images\\units\\{self.name}-barbarian-hover-firing.png')

class Soldier(BaseUnit):
    def __init__(self, x, y, team):
        self.name = "Soldier"
        super().__init__(x, y, team)
        self.health = 100
        self.can_shoot = False
        self.gold_cost = 5
        self.attack_power = 30

class Archer(BaseUnit):
    def __init__(self, x, y, team):
        self.name = "Archer"
        super().__init__(x, y, team)
        self.health = 30
        self.can_shoot = True
        self.range = 200
        self.attack_power = 50
        self.defense_power = 5
        self.movement = 310
        self.initial_movement = 310
        self.gold_cost = 7

class Settler(BaseUnit):
    def __init__(self, x, y, team):
        self.name = "Settler"
        super().__init__(x, y, team)
        self.health = 5
        self.attack_power = 0
        self.defense_power = 0
        self.movement = 250
        self.initial_movement = 250
        self.gold_cost = 8

    def check_far_enough_from_city(self, current_space, board):
        # distance from any city, not just your own
        for space in board:
            if space.name == "City":
                if abs(space.rect.centerx - current_space.rect.centerx) < 300 and \
                   abs(space.rect.centery - current_space.rect.centery) < 300:
                    return False
        return True

    def settle(self, current_space, team, board, screen):
        if current_space.name != "City" and current_space.name != "River" and current_space.name != "Mountain":
            if self.check_far_enough_from_city(current_space, board):
                new_space = City(current_space.rect.centerx, current_space.rect.centery)
                new_space.owner = team
                new_space.units = [unit for unit in current_space.units if unit.id != self.id]
                number_on_board = 0
                for space in board:
                    if space.id == current_space.id:
                        break
                    number_on_board += 1
                board[number_on_board] = new_space
                team.owned_cities.append(new_space)
            else:
                show_popup(screen, "Too close to another city to settle")