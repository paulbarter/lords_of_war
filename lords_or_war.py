import pygame
pygame.init()
from pygame.locals import *

from Screens import BaseScreen, BaseButton, display_screen_and_resources, handle_buttons
from Units.Spaces import get_current_active_unit, \
    snap_to_space, remove_movement_hilights, snap_back_to_start, check_hover_unit, \
    remove_all_unit_hilights, shoot_at_space, handle_hover

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

w, h = 1550, 795
screen = pygame.display.set_mode((w, h))
space_width = 75
space_height = 75
from Board import get_board, make_random_board
from Teams import team_wolf, team_barbarian
# board = get_board(space_width, space_height)
board = make_random_board( 14, 9, space_width, space_height, percentage_road=0.0)
current_active_team = team_wolf

from Utils import load_game
# board, current_active_team, team_wolf, team_barbarian = load_game("saved_games\\20250714_001130_game.json")

# boards for info
resources_screen = BaseScreen(screen, 1100, 20, 400, 200)
unit_info_screen = BaseScreen(screen, 1100, 250, 400, 150)
end_turn_button = BaseButton(screen, 'END TURN', 20, 720, 150, 50)
fire_button = BaseButton(screen, 'FIRE', 250, 720, 250, 50)
buy_settler_button = BaseButton(screen, 'Buy settler', 530, 720, 200, 50)
settle_button = BaseButton(screen, 'SETTLE', 750, 720, 200, 50)
buy_soldier_button = BaseButton(screen, 'Buy Soldier', 1000, 720, 200, 50)
save_game_button = BaseButton(screen, 'Save Game', 1250, 720, 200, 50)
research_road_button = BaseButton(screen, 'Research Road', 1090, 450, 80, 18)
research_archery_button = BaseButton(screen, 'Research Archery', 1090, 500, 80, 18)

# Initialising variables
running = True
moving = False
current_active_unit = None
previously_active_unit = None
current_hovered_space = None
firing_is_active = False
active_space = None
possible_dest_space_ids = []
hovered_unit = None
current_selected_unit_info = []
unit_stack = []


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            (firing_is_active, current_active_team, moving, current_active_unit, active_space, possible_dest_space_ids, team_wolf,
            team_barbarian) = (
                handle_buttons(event, board, screen, fire_button, buy_settler_button, end_turn_button, firing_is_active,
                               active_space, current_active_team, moving, current_active_unit, possible_dest_space_ids,
                               team_wolf, team_barbarian, settle_button, buy_soldier_button, save_game_button, research_road_button,
                               research_archery_button))
            current_active_unit, active_space, unit_stack = get_current_active_unit(previously_active_unit, current_active_team,
                                                                                    event.pos[0], event.pos[1], board)
            if current_active_unit:
                moving = True
                current_selected_unit_info = current_active_unit.get_info(unit_stack)
            else:
                remove_all_unit_hilights(board, screen)
                if active_space:
                    current_selected_unit_info = active_space.get_info()

        elif event.type == MOUSEBUTTONUP:
            moving = False
            ###############
            # ACTUALLY MOVE
            if current_active_unit:
                if possible_dest_space_ids and len(possible_dest_space_ids) > 0:
                    if firing_is_active:
                        shoot_at_space(board, current_active_unit, event.pos)
                    else:
                        inactive_team = team_wolf if current_active_team.name == "Barbarian" else team_barbarian
                        snap_to_space(current_active_team, inactive_team, board, possible_dest_space_ids, current_active_unit, active_space)
                    current_selected_unit_info = current_active_unit.get_info(unit_stack)
                else:
                    snap_back_to_start(current_active_unit, active_space)
                possible_dest_space_ids = []
                remove_movement_hilights(board, screen)
                previously_active_unit = current_active_unit
        elif event.type == MOUSEMOTION:
            ##################################
            # CHECKING WHERE CAN MOVE OR SHOOT
            if moving or firing_is_active:
                current_hovered_space, possible_dest_space_ids = handle_hover(board, screen, current_active_unit, active_space,
                                                              current_active_team, event, firing_is_active)
            else:
                hovered_unit = check_hover_unit(current_active_team, screen, board, event.pos)
            remove_movement_hilights(board, screen, exclude=current_hovered_space)

    display_screen_and_resources(screen, board, end_turn_button, fire_button, resources_screen, unit_info_screen,
                                 current_active_team, team_wolf, team_barbarian, firing_is_active, current_selected_unit_info,
                                 buy_settler_button, settle_button, buy_soldier_button, hovered_unit, research_road_button,
                                 research_archery_button, save_game_button)
    if moving and current_active_unit:
        current_active_unit.draw(screen)
    pygame.display.update()
pygame.quit()
