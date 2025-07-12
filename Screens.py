import pygame
from Units.BaseUnit import Teams, Soldier, Settler
from Units.Spaces import SpaceTypes
from Utils import handle_end_turn

pygame.init()
font = pygame.font.SysFont(None, 32)
SCREEN_BACKGROUND = (60, 60, 60)

def handle_buttons(event, board, screen, fire_button, buy_settler_button, end_turn_button, firing_is_active, active_space,
                   current_active_team, moving, current_active_unit, possible_dest_space_ids, team_wolf, team_barbarian,
                   settle_button, buy_soldier_button):
    if fire_button.rect.collidepoint(event.pos):
        firing_is_active = not firing_is_active
    if buy_settler_button.rect.collidepoint(event.pos):
        if active_space and active_space.type == SpaceTypes.CITY:
            current_active_team.buy_unit(active_space, Settler(1, 2, current_active_team.type))
    if end_turn_button.rect.collidepoint(event.pos):
        (current_active_team, moving, current_active_unit, active_space, possible_dest_space_ids, team_wolf,
         team_barbarian) = handle_end_turn(board, screen, current_active_team, moving, current_active_unit,
                                           active_space,
                                           possible_dest_space_ids, team_wolf, team_barbarian)
    if settle_button.rect.collidepoint(event.pos):
        if (current_active_unit and current_active_unit.name == 'Settler' and active_space and active_space.name != "City" and
                active_space.name != "River" and active_space.name != "Mountain"):
            current_active_unit.settle(active_space, current_active_team, board)
    if buy_soldier_button.rect.collidepoint(event.pos):
        if active_space and active_space.type == SpaceTypes.CITY:
            current_active_team.buy_unit(active_space, Soldier(1, 2, current_active_team.type))
    return (firing_is_active, current_active_team, moving, current_active_unit, active_space, possible_dest_space_ids, team_wolf,
            team_barbarian)

class BaseScreen:
    def __init__(self, screen, left, top, width, height):
        self.name = "BaseScreen"
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def render_multiline_text(self, screen, font, messages, left, top, line_spacing=2):
        y = top
        for message in messages:
            text_surface = font.render(message, True, (0, 0, 0))
            screen.blit(text_surface, (left + 10, y + 10))
            y += text_surface.get_height() + line_spacing

    def display(self, text="", messages=[], add_overlay=False):
        if add_overlay:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 50))  # Black with alpha
            self.screen.blit(overlay, (0, 0))

        popup_rect = pygame.Rect(self.left, self.top, self.width, self.height)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), popup_rect, 3)
        if text:
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=popup_rect.center)
            self.screen.blit(text_surface, text_rect)
        else:
            self.render_multiline_text(self.screen, font, messages, self.left, self.top)

class ResourcesScreen(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.name = "ResourcesScreen"

    def display(self):
        super().display()
        print("Displaying resources information.")

class BaseButton:
    def __init__(self, screen, text, left, top, width, height):
        self.screen = screen
        self.rect = pygame.Rect(left, top, width, height)
        self.text_surface = font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, color=(150, 150, 150), new_text=""):
        if new_text:
            self.text_surface = font.render(new_text, True, (255, 255, 255))
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        pygame.draw.rect(self.screen, (150, 150, 150), self.rect)
        self.screen.blit(self.text_surface, self.text_rect)


def draw_board(screen, board):
    for space in board:
        space.draw(screen)

def display_screen_and_resources(screen, board, end_turn_button, fire_button, resources_screen, unit_info_screen,
                                 current_active_team, team_wolf, team_barbarian, firing, current_selected_unit_info,
                                 buy_button, settle_button, buy_soldier_button):
    screen.fill(SCREEN_BACKGROUND)
    draw_board(screen, board)
    end_turn_button.draw()
    if firing:
        fire_button.draw(new_text='MOVE [NOW FIRING]')
    else:
        fire_button.draw(new_text='FIRE [NOW MOVING]')
    if current_active_team.type == Teams.WOLF:
        resources_screen.display(messages=team_wolf.get_info())
    elif current_active_team.type == Teams.BARBARIAN:
        resources_screen.display(messages=team_barbarian.get_info())
    unit_info_screen.display(text=None, messages=current_selected_unit_info)
    buy_button.draw(new_text='BUY SETTLER')
    settle_button.draw(new_text='SETTLE')
    buy_soldier_button.draw(new_text='BUY SOLDIER')

