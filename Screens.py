import pygame
from Units.BaseUnit import Teams

pygame.init()
font = pygame.font.SysFont(None, 32)
SCREEN_BACKGROUND = (60, 60, 60)

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
                                 current_active_team, team_wolf, team_barbarian, firing, current_selected_unit_info):
    screen.fill(SCREEN_BACKGROUND)
    draw_board(screen, board)
    end_turn_button.draw()
    if firing:
        fire_button.draw(new_text='MOVE [NOW FIRING]')
    else:
        fire_button.draw(new_text='FIRE [NOW MOVING]')
    if current_active_team.type == Teams.WOLF:
        resources_screen.display(
            text=f"WOLF: Turn: {team_wolf.turn_nr}; Gold: {team_wolf.calculate_resources()}, Resources: 50")
    elif current_active_team.type == Teams.BARBARIAN:
        resources_screen.display(
            text=f"Barbarians: Turn: {team_barbarian.turn_nr}; Gold: {team_barbarian.calculate_resources()}, Resources: 50")
    unit_info_screen.display(text=None, messages=current_selected_unit_info)

