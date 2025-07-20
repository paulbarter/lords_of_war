import pygame

from Attack import show_popup
from Units.BaseUnit import Settler, Archer, Wolf, Barbarian
from Teams import Teams
from Units.Spaces import SpaceTypes, Road
from Utils import handle_end_turn, save_game
from sounds.Sounds import play_sound

pygame.init()
default_font = pygame.font.SysFont(None, 32)
SCREEN_BACKGROUND = (60, 60, 60)

def toggle_button(button1, button2):
    if button1.pressed:
        button1.pressed = False
        button2.pressed = True
    else:
        button2.pressed = True
        button1.pressed = False

def handle_buttons(event, board, screen, fire_button, buy_settler_button, end_turn_button, firing_is_active, active_space,
                   current_active_team, moving, current_active_unit, possible_dest_space_ids, team_wolf, team_barbarian,
                   settle_button, buy_soldier_button, save_game_button, research_road_button, research_archery_button,
                   move_button, search_ruins_button):
    if fire_button.rect.collidepoint(event.pos):
        firing_is_active = not firing_is_active
        toggle_button(fire_button, move_button)
    if move_button.rect.collidepoint(event.pos):
        firing_is_active = False
        toggle_button(move_button, fire_button)
    if buy_settler_button.rect.collidepoint(event.pos):
        if active_space and active_space.type == SpaceTypes.CITY and active_space.owner == current_active_team:
            current_active_team.buy_unit(active_space, Settler(1, 2, current_active_team.type))
    if end_turn_button.rect.collidepoint(event.pos):
        (current_active_team, moving, current_active_unit, active_space, possible_dest_space_ids, team_wolf,
         team_barbarian) = handle_end_turn(board, screen, current_active_team, moving, current_active_unit,
                                           active_space,
                                           possible_dest_space_ids, team_wolf, team_barbarian)
    if settle_button.rect.collidepoint(event.pos):
        if (current_active_unit and current_active_unit.name == 'Settler' and active_space and active_space.name != "City" and
                active_space.name != "River" and active_space.name != "Mountain" and current_active_unit in active_space.units):
            current_active_unit.settle(active_space, current_active_team, board, screen)
    if buy_soldier_button.rect.collidepoint(event.pos):
        buy_soldier(screen, current_active_team, active_space)
    if save_game_button.rect.collidepoint(event.pos):
        save_game(board, current_active_team, team_wolf, team_barbarian)
    if research_archery_button.rect.collidepoint(event.pos):
        research_archery(screen, current_active_team, active_space)
    if research_road_button.rect.collidepoint(event.pos):
        research_road(screen, current_active_team, active_space, board)
    if search_ruins_button.rect.collidepoint(event.pos):
        current_active_unit.search_ruins(screen, active_space, board, current_active_team)
    return (firing_is_active, current_active_team, moving, current_active_unit, active_space, possible_dest_space_ids, team_wolf,
            team_barbarian)

def is_adjacent_city_or_road(current_space, board, current_active_team):
    # next to any city or road you own
    for space in board:
        if space.name in ["City", "Road"]:
            if abs(space.rect.centerx - current_space.rect.centerx) < 150 and \
               abs(space.rect.centery - current_space.rect.centery) < 150 and space.owner == current_active_team:
                return True
    return False

def buy_soldier(screen, current_active_team, active_space):
    if active_space and active_space.type == SpaceTypes.CITY and active_space.owner == current_active_team:
        if current_active_team.total_gold >= 5:
            if current_active_team.name == 'Wolf':
                current_active_team.buy_unit(active_space, Wolf(1, 2, current_active_team.type))
            else:
                current_active_team.buy_unit(active_space, Barbarian(1, 2, current_active_team.type))
        else:
            show_popup(screen, "Not enough gold, 5 needed", default_font)

def research_road(screen, current_active_team, active_space, board):
    if current_active_team.total_resources < 5:
        show_popup(screen, "Not enough resources, 5 needed", default_font)
    else:
        if not current_active_team.researched_roads:
            current_active_team.researched_roads = True
            play_sound('sounds\\research.wav')
            show_popup(screen, "You researched the road, a straight line, well done! - what took you so long!?", default_font)
            current_active_team.total_resources -= 5
        elif (active_space and is_adjacent_city_or_road(active_space, board, current_active_team) and active_space.type != SpaceTypes.CITY and
              active_space.type != SpaceTypes.RIVER and active_space.type != SpaceTypes.MOUNTAIN and active_space.type != SpaceTypes.ROAD):
            new_space = Road(active_space.rect.centerx, active_space.rect.centery)
            new_space.owner = current_active_team
            new_space.units = active_space.units
            number_on_board = 0
            for space in board:
                if space.id == active_space.id:
                    break
                number_on_board += 1
            board[number_on_board] = new_space
            current_active_team.total_resources -= 5
        else:
            show_popup(screen, "Click on a plain or forrest next to a city or road you own", default_font)

def research_archery(screen, current_active_team, active_space):
    if current_active_team.total_resources < 7:
        show_popup(screen, "Not enough resources, 7 needed", default_font)
    else:
        if not current_active_team.researched_archery:
            current_active_team.researched_archery = True
            play_sound('sounds\\research.wav')
            show_popup(screen,
                       "Your noble race has researched the noble art of archery, nobly. You may now nobly buy archers.",
                       default_font)
            current_active_team.total_resources -= 7
        elif active_space and active_space.type == SpaceTypes.CITY and active_space.owner == current_active_team:
            if current_active_team.total_gold < 7:
                show_popup(screen, "Not enough gold, 7 needed", default_font)
            else:
                current_active_team.buy_unit(active_space, Archer(1, 2, current_active_team.type))
        else:
            show_popup(screen, "Click on a city first", default_font)

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
            text_surface = default_font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=popup_rect.center)
            self.screen.blit(text_surface, text_rect)
        else:
            self.render_multiline_text(self.screen, default_font, messages, self.left, self.top)

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
        self.text_surface = default_font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.pressed = False

    def draw(self, new_text="", font_type=None):
        font = default_font
        if font_type == 'small':
            font = pygame.font.SysFont(None, 24)
        if new_text:
            if self.pressed:
                self.text_surface = font.render(new_text, True, (100, 100, 100))
            else:
                self.text_surface = font.render(new_text, True, (255, 255, 255))
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        pygame.draw.rect(self.screen, (150, 150, 150), self.rect)
        self.screen.blit(self.text_surface, self.text_rect)


def draw_board(screen, board):
    for space in board:
        space.draw(screen)

def draw_selected_space(unit_info_screen, screen, current_active_unit, active_space):
    if current_active_unit:
        display_unit = current_active_unit.clone_unit()
        display_unit.rect.top = unit_info_screen.top + 170
        display_unit.rect.right = unit_info_screen.left + 80
    elif active_space:
        display_unit = active_space.clone_space()
        display_unit.rect.top = unit_info_screen.top + 140
        display_unit.rect.right = unit_info_screen.left + 100
    display_unit.draw(screen)

def display_screen_and_resources(screen, board, end_turn_button, fire_button, resources_screen, unit_info_screen,
                                 current_active_team, team_wolf, team_barbarian, current_selected_unit_info,
                                 buy_button, settle_button, buy_soldier_button, research_road_button,
                                 research_archery_button, save_game_button, move_button, current_active_unit, active_space,
                                 search_ruins_button):
    screen.fill(SCREEN_BACKGROUND)
    draw_board(screen, board)
    end_turn_button.draw()
    fire_button.draw(new_text='FIRE')
    move_button.draw(new_text='MOVE')
    if current_active_team.type == Teams.WOLF:
        resources_screen.display(messages=team_wolf.get_info())
    elif current_active_team.type == Teams.BARBARIAN:
        resources_screen.display(messages=team_barbarian.get_info())

    unit_info_screen.display(text=None, messages=current_selected_unit_info)
    if current_active_unit or active_space:
        draw_selected_space(unit_info_screen, screen, current_active_unit, active_space)
    buy_button.draw(new_text='BUY SETTLER [8]')
    settle_button.draw(new_text='SETTLE')
    buy_soldier_button.draw(new_text='BUY SOLDIER [5]')
    save_game_button.draw(new_text='SAVE GAME')
    research_road_button.draw(new_text='Road [5]', font_type='small')
    research_archery_button.draw(new_text='Archery [7]', font_type='small')
    if current_active_unit and current_active_unit.type == 'Hero':
        search_ruins_button.draw(new_text='Search Ruins', font_type='small')

