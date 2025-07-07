import pygame
from pygame.locals import *

from Units.BaseUnit import BaseUnit
from Units.Spaces import SpaceTypes, BaseSpace, get_current_active_space

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (255, 0, 255)

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
space_2_2 = BaseSpace(space_width * 2, -50 + space_height * 2, 5, SpaceTypes.PLAIN)
space_2_3 = BaseSpace(space_width * 3, -50 + space_height * 2, 6, SpaceTypes.PLAIN)

space_1_2.add_unit(BaseUnit(1, 2))

board = [space_1_1, space_1_2, space_1_3, space_2_1, space_2_2, space_2_3]
def draw_board():
    for space in board:
        space.draw(screen)

def snap_to_space(rect):

    # Reset all spaces to unsnapped before checking
    # for space in board:
    #     space.is_snapped = False

    for space in board:
        # if not space.is_snapped:
        if (abs(rect.centerx - space.rect.centerx) < 7) and (abs(rect.centery - space.rect.centery) < 7):
            rect.x = space.x
            rect.y = space.y
            # space.is_snapped = True
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
            # if rect.collidepoint(event.pos):
            #     moving = True

        # Set moving as False if you want
        # to move the image only with the
        # mouse click
        # Set moving as True if you want
        # to move the image without the
        # mouse click
        elif event.type == MOUSEBUTTONUP:
            moving = False

        # Make your image move continuously
        elif event.type == MOUSEMOTION and moving:
            active_unit = current_active_space.units[0]
            active_unit.rect.move_ip(event.rel)
            # snap_to_space(active_unit.rect)
            screen.blit(active_unit.image, active_unit.rect)
            # rect.move_ip(event.rel)
            # snap_to_space(rect)

    # Set screen color and image on screen
    screen.fill(BROWN)
    # screen.blit(img, rect)

    # Construct the border to the image
    # pygame.draw.rect(screen, BLUE, rect, 2)
    draw_board()

    # Update the GUI pygame
    pygame.display.update()

# Quit the GUI game
pygame.quit()
