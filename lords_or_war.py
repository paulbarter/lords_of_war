import pygame
from pygame.locals import *

from Board import team_wolf, team_barbarian, get_board
from Screens import BaseScreen, BaseButton
from Units.BaseUnit import Teams
from Units.Spaces import get_current_active_unit, hover_space, \
    snap_to_space, remove_movement_hilights, snap_back_to_start, check_hover_unit, restore_movement_units, \
    remove_all_unit_hilights

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (60, 60, 60)

pygame.init()
font = pygame.font.SysFont(None, 32)
w, h = 1550, 795
screen = pygame.display.set_mode((w, h))
space_width = 100
space_height = 100
board = get_board(space_width, space_height)

def draw_board():
    for space in board:
        space.draw(screen)

# Initialising variables
running = True
moving = False
current_active_unit = None
firing_is_active = False
active_space = None
possible_dest_space_ids = []
possible_firing_dest_space_ids = []
hovered_unit = None
current_selected_unit_info = []
current_active_team = team_wolf

# boards for info
resources_screen = BaseScreen(screen, 100, 400, 600, 200)
unit_info_screen = BaseScreen(screen, 100, 600, 400, 150)
end_turn_button = BaseButton(screen, 'END TURN', 100, 320, 150, 50)
fire_button = BaseButton(screen, 'FIRE', 300, 320, 150, 50)

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

            # TODO = check firing: possible_firing_dest_space_ids

            if current_active_unit:
                if len(possible_dest_space_ids) > 0:
                    snap_to_space(current_active_team, board, possible_dest_space_ids, current_active_unit, active_space)
                    current_selected_unit_info = current_active_unit.get_info()
                    # After snapping, check if the unit moved to a new space
                    for space in board:
                        if current_active_unit in space.units:
                            active_space = space
                            break
                else:
                    snap_back_to_start(current_active_unit, active_space)
                possible_dest_space_ids = []
                possible_firing_dest_space_ids = []
                remove_movement_hilights(board, screen)
                current_active_unit = None
                active_space = None

        # Make your image move continuously
        elif event.type == MOUSEMOTION:
            if moving or firing_is_active:
                if current_active_unit and active_space:
                    if not firing_is_active:
                        current_active_unit.rect.move_ip(event.rel)
                        possible_dest_space_ids = hover_space(board, screen, current_active_unit, active_space,
                                                              event.pos[0], event.pos[1], firing=False)
                    else:
                        possible_firing_dest_space_ids = \
                            hover_space(board, screen, current_active_unit, active_space,
                                                          event.pos[0], event.pos[1], firing=firing_is_active)
            else:
                hovered_unit = check_hover_unit(current_active_team, screen, board, event.pos)

    screen.fill(BROWN)
    draw_board()
    end_turn_button.draw()
    if firing_is_active:
        fire_button.draw(new_text='STOP FIRING')
    else:
        fire_button.draw(new_text='FIRE')
    if current_active_team.type == Teams.WOLF:
        resources_screen.display(text=f"WOLF: Turn: {team_wolf.turn_nr}; Gold: {team_wolf.calculate_resources()}, Resources: 50")
    elif current_active_team.type == Teams.BARBARIAN:
        resources_screen.display(text=f"Barbarians: Turn: {team_barbarian.turn_nr}; Gold: {team_barbarian.calculate_resources()}, Resources: 50")

    unit_info_screen.display(text=None, messages=current_selected_unit_info)
    if moving and current_active_unit:
        current_active_unit.draw(screen)
    pygame.display.update()
pygame.quit()
