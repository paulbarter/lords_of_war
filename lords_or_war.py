import pygame
pygame.init()
from pygame.locals import *

from Board import team_wolf, team_barbarian, get_board
from Screens import BaseScreen, BaseButton, display_screen_and_resources
from Units.Spaces import get_current_active_unit, hover_space, \
    snap_to_space, remove_movement_hilights, snap_back_to_start, check_hover_unit, restore_movement_units, \
    remove_all_unit_hilights, shoot_at_space, handle_hover

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

w, h = 1550, 795
screen = pygame.display.set_mode((w, h))
space_width = 100
space_height = 100
board = get_board(space_width, space_height)

# boards for info
resources_screen = BaseScreen(screen, 100, 400, 600, 200)
unit_info_screen = BaseScreen(screen, 100, 600, 400, 150)
end_turn_button = BaseButton(screen, 'END TURN', 100, 320, 150, 50)
fire_button = BaseButton(screen, 'FIRE', 300, 320, 250, 50)

# Initialising variables
running = True
moving = False
current_active_unit = None
current_hovered_space = None
firing_is_active = False
active_space = None
possible_dest_space_ids = []
hovered_unit = None
current_selected_unit_info = []
current_active_team = team_wolf

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            current_active_unit, active_space = get_current_active_unit(current_active_team, event.pos[0], event.pos[1], board)
            if current_active_unit:
                moving = True
                current_selected_unit_info = current_active_unit.get_info()
            else:
                remove_all_unit_hilights(board, screen)
                if active_space:
                    current_selected_unit_info = active_space.get_info()
            if fire_button.rect.collidepoint(event.pos):
                firing_is_active = not firing_is_active
            if end_turn_button.rect.collidepoint(event.pos):
                # show_popup(screen, f"Ending turn for team {current_turn}", font)
                restore_movement_units(board, current_active_team)
                current_active_team = team_barbarian if current_active_team.name == 'Wolf' else team_wolf
                moving = False
                current_active_unit = None
                active_space = None
                possible_dest_space_ids = []
                remove_movement_hilights(board, screen)
                if current_active_team.name == 'Wolf':
                    team_wolf.turn_nr += 1
                else:
                    if team_barbarian.turn_nr != 0:
                        team_barbarian.turn_nr += 1
        elif event.type == MOUSEBUTTONUP:
            moving = False
            if current_active_unit:
                if possible_dest_space_ids and len(possible_dest_space_ids) > 0:
                    if firing_is_active:
                        shoot_at_space(board, current_active_unit, event.pos)
                    else:
                        snap_to_space(current_active_team, board, possible_dest_space_ids, current_active_unit, active_space)
                    current_selected_unit_info = current_active_unit.get_info()
                else:
                    snap_back_to_start(current_active_unit, active_space)
                possible_dest_space_ids = []
                remove_movement_hilights(board, screen)
                current_active_unit = None
                active_space = None
        elif event.type == MOUSEMOTION:
            if moving or firing_is_active:
                current_hovered_space, possible_dest_space_ids = handle_hover(board, screen, current_active_unit, active_space,
                                                              current_active_team, event, firing_is_active)
            else:
                hovered_unit = check_hover_unit(current_active_team, screen, board, event.pos)
            remove_movement_hilights(board, screen, exclude=current_hovered_space)

    display_screen_and_resources(screen, board, end_turn_button, fire_button, resources_screen, unit_info_screen,
                                 current_active_team, team_wolf, team_barbarian, firing_is_active, current_selected_unit_info)
    if moving and current_active_unit:
        current_active_unit.draw(screen)
    pygame.display.update()
pygame.quit()
