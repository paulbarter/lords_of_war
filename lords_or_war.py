import pygame
from pygame.locals import *

from Units.BaseUnit import BaseUnit
from Units.Spaces import SpaceTypes, BaseSpace, get_current_active_space, get_current_active_unit

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
space_height = 154
space_width = 97

space_1_1 = BaseSpace(space_width, -50 + space_height, 1, SpaceTypes.CITY)
space_1_2 = BaseSpace(space_width * 2, -50 + space_height, 2, SpaceTypes.ROAD)
space_1_3 = BaseSpace(space_width * 3, -50 + space_height, 3, SpaceTypes.ROAD)
space_2_1 = BaseSpace(space_width, -50 + space_height * 2, 4, SpaceTypes.PLAIN)
space_2_2 = BaseSpace(space_width * 2, -50 + space_height * 2, 5, SpaceTypes.CITY)
space_2_3 = BaseSpace(space_width * 3, -50 + space_height * 2, 6, SpaceTypes.ROAD)

space_1_1.add_unit(BaseUnit(1, 2))
space_2_2.add_unit(BaseUnit(1, 2))

board = [space_1_1, space_1_2, space_1_3, space_2_1, space_2_2, space_2_3]
def draw_board(active_space: BaseSpace, current_active_unit):
    for space in board:
        space.draw(screen, active_space, current_active_unit)

def snap_to_space(unit, dragged_from_space: BaseSpace):
    for space in board:
        if (abs(unit.rect.centerx - space.rect.centerx) < 20) and (abs(unit.rect.centery - space.rect.centery) < 20):
            unit.rect.center = space.rect.center
            if dragged_from_space.id != space.id:
                # only move the unit if it is not the same space
                space.add_unit(unit)
                dragged_from_space.remove_unit(unit)
            break

current_active_unit = None
active_space = None

def show_popup(screen, message, font):
    # Draw semi-transparent overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Black with alpha
    screen.blit(overlay, (0, 0))

    # Draw popup rectangle
    popup_rect = pygame.Rect(0, 0, 400, 200)
    popup_rect.center = screen.get_rect().center
    pygame.draw.rect(screen, (255, 255, 255), popup_rect)
    pygame.draw.rect(screen, (0, 0, 0), popup_rect, 3)

    # Render message
    text_surface = font.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=popup_rect.center)
    screen.blit(text_surface, text_rect)

    pygame.display.update()

    # Wait for user to close popup
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.QUIT):
                waiting = False

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            current_active_unit, active_space = get_current_active_unit(event.pos[0], event.pos[1], board)
            if current_active_unit:
                moving = True
        elif event.type == MOUSEBUTTONUP:
            moving = False
            snap_to_space(current_active_unit, active_space)
            current_active_unit = None
            active_space = None
            # After snapping, check if the unit moved to a new space
            for space in board:
                if current_active_unit in space.units:
                    active_space = space
                    break

        # Make your image move continuously
        elif event.type == MOUSEMOTION and moving:
            # show_popup(screen, f"unit: {current_active_unit} space {active_space}", font)
            if current_active_unit and active_space:
                current_active_unit.rect.move_ip(event.rel)

    screen.fill(BROWN)
    draw_board(active_space, current_active_unit)
    if moving and current_active_unit:
        current_active_unit.draw(screen)
    pygame.display.update()
pygame.quit()
