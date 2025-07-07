import pygame
from pygame.locals import *

from Units.BaseUnit import BaseUnit
from Units.Spaces import SpaceTypes, BaseSpace, get_current_active_space

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (100, 100, 100)

pygame.init()
w, h = 940, 750
screen = pygame.display.set_mode((w, h))

# img = pygame.image.load('images\\soldier.png')
# img.convert()
# # Draw rectangle around the image
# rect = img.get_rect()
# rect.center = w // 2, h // 2
space_height = 127
space_width = 74

# Set running and moving values
running = True
moving = False

space_1_1 = BaseSpace(space_width, -50 + space_height, 1, SpaceTypes.CITY)
space_1_2 = BaseSpace(space_width * 2, -50 + space_height, 2, SpaceTypes.ROAD)
space_1_3 = BaseSpace(space_width * 3, -50 + space_height, 3, SpaceTypes.ROAD)
space_2_1 = BaseSpace(space_width, -50 + space_height * 2, 4, SpaceTypes.PLAIN)
space_2_2 = BaseSpace(space_width * 2, -50 + space_height * 2, 5, SpaceTypes.CITY)
space_2_3 = BaseSpace(space_width * 3, -50 + space_height * 2, 6, SpaceTypes.ROAD)

space_1_2.add_unit(BaseUnit(1, 2))
space_2_2.add_unit(BaseUnit(1, 2))

board = [space_1_1, space_1_2, space_1_3, space_2_1, space_2_2, space_2_3]
def draw_board():
    for space in board:
        space.draw(screen)

def snap_to_space(unit, dragged_from_space: BaseSpace):
    for space in board:
        if (abs(unit.rect.centerx - space.rect.centerx) < 7) and (abs(unit.rect.centery - space.rect.centery) < 7):
            unit.rect.x = space.x
            unit.rect.y = space.y
            if dragged_from_space.id != space.id:
                # only move the unit if it is not the same space
                space.add_unit(unit)
                dragged_from_space.remove_unit(unit)
            break

current_active_space = None

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            current_active_space = get_current_active_space(event.pos[0], event.pos[1], board)
            if current_active_space:
                moving = True
        elif event.type == MOUSEBUTTONUP:
            moving = False

        # Make your image move continuously
        elif event.type == MOUSEMOTION and moving:
            if len(current_active_space.units) > 0:
                active_unit = current_active_space.units[0]
                active_unit.rect.move_ip(event.rel)
                active_unit.position = active_unit.rect.center
                snap_to_space(active_unit, current_active_space)

    screen.fill(BROWN)
    draw_board()
    pygame.display.update()
pygame.quit()
