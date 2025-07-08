import pygame
from pygame.locals import *

from Attack import show_popup
from Screens import BaseScreen
from Units.BaseUnit import BaseUnit, Jet, Teams
from Units.Spaces import SpaceTypes, BaseSpace, get_current_active_space, get_current_active_unit, hover_space, \
    snap_to_space, remove_movement_hilights, snap_back_to_start

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (100, 100, 100)

pygame.init()
font = pygame.font.SysFont(None, 32)
w, h = 940, 750
screen = pygame.display.set_mode((w, h))

# Set running and moving values
running = True
moving = False
space_height = 100
space_width = 100

space_1_1 = BaseSpace(space_width, -50 + space_height, 1, SpaceTypes.ROAD)
space_1_2 = BaseSpace(space_width * 2, -50 + space_height, 2, SpaceTypes.CITY)
space_1_3 = BaseSpace(space_width * 3, -50 + space_height, 3, SpaceTypes.ROAD)
space_1_4 = BaseSpace(space_width * 4, -50 + space_height, 4, SpaceTypes.ROAD)
space_1_5 = BaseSpace(space_width * 5, -50 + space_height, 5, SpaceTypes.ROAD)
space_1_6 = BaseSpace(space_width * 6, -50 + space_height, 6, SpaceTypes.ROAD)
space_2_1 = BaseSpace(space_width, -50 + space_height * 2, 7, SpaceTypes.ROAD)
space_2_2 = BaseSpace(space_width * 2, -50 + space_height * 2, 8, SpaceTypes.ROAD)
space_2_3 = BaseSpace(space_width * 3, -50 + space_height * 2, 9, SpaceTypes.ROAD)
space_2_4 = BaseSpace(space_width * 4, -50 + space_height * 2, 10, SpaceTypes.ROAD)
space_2_5 = BaseSpace(space_width * 5, -50 + space_height * 2, 11, SpaceTypes.ROAD)
space_2_6 = BaseSpace(space_width * 6, -50 + space_height * 2, 12, SpaceTypes.PLAIN)
space_3_1 = BaseSpace(space_width, -50 + space_height * 3, 13, SpaceTypes.PLAIN)
space_3_2 = BaseSpace(space_width * 2, -50 + space_height * 3, 14, SpaceTypes.ROAD)
space_3_3 = BaseSpace(space_width * 3, -50 + space_height * 3, 15, SpaceTypes.RIVER)
space_3_4 = BaseSpace(space_width * 4, -50 + space_height * 3, 16, SpaceTypes.ROAD)
space_3_5 = BaseSpace(space_width * 5, -50 + space_height * 3, 17, SpaceTypes.RIVER)
space_3_6 = BaseSpace(space_width * 6, -50 + space_height * 3, 18, SpaceTypes.MOUNTAIN)

space_1_1.add_unit(BaseUnit(1, 2, Teams.WOLF))
space_2_2.add_unit(BaseUnit(1, 2, Teams.BARBARIAN))
space_2_3.add_unit(Jet(1, 2, Teams.WOLF))

board = [space_1_1, space_1_2, space_1_3, space_1_4, space_1_5, space_1_6,
         space_2_1, space_2_2, space_2_3, space_2_4, space_2_5, space_2_6,
         space_3_1, space_3_2, space_3_3, space_3_4, space_3_5, space_3_6]

end_turn_image = pygame.image.load('images\\end_turn_button.png')
end_turn_image.convert()
end_turn_button = end_turn_image.get_rect()
end_turn_button.center = (300, 350)

def draw_board():
    for space in board:
        space.draw(screen)

current_active_unit = None
active_space = None
possible_dest_space_ids = []
current_turn = Teams.WOLF
resources_screen = BaseScreen(screen, 100, 400, 600, 200)
unit_info_screen = BaseScreen(screen, 100, 600, 400, 100)
hovered_unit = None

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            current_active_unit, active_space = get_current_active_unit(current_turn, event.pos[0], event.pos[1], board)
            if current_active_unit:
                moving = True
            if end_turn_button.collidepoint(event.pos):
                # End turn logic here
                show_popup(screen, f"Ending turn for team {current_turn}", font)
                restore_movement_units(board, current_turn)
                current_turn = Teams.BARBARIAN if current_turn == Teams.WOLF else Teams.WOLF
                moving = False
                current_active_unit = None
                active_space = None
                possible_dest_space_ids = []
                remove_movement_hilights(board, screen)
        elif event.type == MOUSEBUTTONUP:
            moving = False
            if current_active_unit:
                if len(possible_dest_space_ids) > 0:
                    snap_to_space(board, possible_dest_space_ids, current_active_unit, active_space)
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
                hovered_unit = check_hover_unit(current_turn, screen, board, event.pos)

    screen.fill(BROWN)
    draw_board()
    pygame.draw.rect(screen, BLUE, end_turn_button, 1)
    screen.blit(end_turn_image, end_turn_button)
    resources_screen.display(f"Gold: 100, Resources: 50")
    unit_info_screen.display(f"Unit info:")
    if moving and current_active_unit:
        current_active_unit.draw(screen)
    pygame.display.update()
pygame.quit()
