import pygame
from pygame.locals import *

from Board import team_wolf, team_barbarian, get_board
from Screens import BaseScreen
from Units.BaseUnit import Teams
from Units.Spaces import get_current_active_unit, hover_space, \
    snap_to_space, remove_movement_hilights, snap_back_to_start, check_hover_unit, restore_movement_units, \
    remove_all_unit_hilights

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (100, 100, 100)

pygame.init()
font = pygame.font.SysFont(None, 32)
w, h = 1550, 795
screen = pygame.display.set_mode((w, h))

running = True
moving = False

end_turn_image = pygame.image.load('images\\end_turn_button.png')
end_turn_image.convert()
end_turn_button = end_turn_image.get_rect()
end_turn_button.center = (300, 350)

space_width = 100
space_height = 100
board = get_board(space_width, space_height)

def draw_board():
    for space in board:
        space.draw(screen)

current_active_unit = None
active_space = None
possible_dest_space_ids = []
resources_screen = BaseScreen(screen, 100, 400, 600, 200)
unit_info_screen = BaseScreen(screen, 100, 600, 400, 150)
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
            if end_turn_button.collidepoint(event.pos):
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
                remove_movement_hilights(board, screen)
                current_active_unit = None
                active_space = None

        # Make your image move continuously
        elif event.type == MOUSEMOTION:
            if moving:
                if current_active_unit and active_space:
                    current_active_unit.rect.move_ip(event.rel)
                    possible_dest_space_ids = hover_space(board, screen, current_active_unit, active_space, event.pos[0], event.pos[1])
            else:
                hovered_unit = check_hover_unit(current_active_team, screen, board, event.pos)

    screen.fill(BROWN)
    draw_board()
    pygame.draw.rect(screen, BLUE, end_turn_button, 1)
    screen.blit(end_turn_image, end_turn_button)
    if current_active_team.type == Teams.WOLF:
        resources_screen.display(text=f"WOLF: Turn: {team_wolf.turn_nr}; Gold: {team_wolf.calculate_resources()}, Resources: 50")
    elif current_active_team.type == Teams.BARBARIAN:
        resources_screen.display(text=f"Barbarians: Turn: {team_barbarian.turn_nr}; Gold: {team_barbarian.calculate_resources()}, Resources: 50")

    unit_info_screen.display(text=None, messages=current_selected_unit_info)
    if moving and current_active_unit:
        current_active_unit.draw(screen)
    pygame.display.update()
pygame.quit()
