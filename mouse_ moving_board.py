# Python program to move the image
# with the mouse

# Import the library pygame
import pygame
from pygame.locals import *

# Take colors input
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Construct the GUI game
pygame.init()

# Set dimensions of game GUI
w, h = 940, 750
screen = pygame.display.set_mode((w, h))

# Take image as input
img = pygame.image.load('images\\soldier.png')
img.convert()

# Draw rectangle around the image
rect = img.get_rect()
rect.center = w // 2, h // 2
space_height = rect.height
space_width = rect.width

# Set running and moving values
running = True
moving = False

# Setting what happens when game
# is in running state

class Space:
    def __init__(self, x, y, id):
        self.id = id
        self.x = x
        self.y = y
        self.is_snapped = False
        self.rect = pygame.Rect(x, y, space_width, space_height)

    def draw(self, screen):
        if self.id == 1:
            pygame.draw.rect(screen, BLUE, self.rect, 2)
        elif self.id == 2:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)
        elif self.id == 3:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        elif self.id == 4:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, 2)
        elif self.id == 5:
            pygame.draw.rect(screen, (0, 255, 255), self.rect, 2)
        elif self.id == 6:
            pygame.draw.rect(screen, (255, 0, 255), self.rect, 2)

space_1_1 = Space(space_width, -50 + space_height, 1)
space_1_2 = Space(space_width * 2, -50 + space_height, 2)
space_1_3 = Space(space_width * 3, -50 + space_height, 3)
space_2_1 = Space(space_width, -50 + space_height * 2, 4)
space_2_2 = Space(space_width * 2, -50 + space_height * 2, 5)
space_2_3 = Space(space_width * 3, -50 + space_height * 2, 6)

board = [space_1_1, space_1_2, space_1_3, space_2_1, space_2_2, space_2_3]
def draw_board():
    for space in board:
        space.draw(screen)

def snap_to_space(rect):

    # def unsnap_the_rest(current_space):
    #     for space in board:
    #         if current_space.id != space.id:
    #             space.is_snapped = False

    # Reset all spaces to unsnapped before checking
    for space in board:
        space.is_snapped = False

    for space in board:
        if not space.is_snapped:
            if (abs(rect.centerx - space.rect.centerx) < 7) and (abs(rect.centery - space.rect.centery) < 7):
                rect.x = space.x
                rect.y = space.y
                space.is_snapped = True
                break
        # if not space.is_snapped:
        #     if (rect.centerx - space.rect.centerx < 2) and (rect.centery - space.rect.centery < 2):
        #         rect.x = space.x
        #         rect.y = space.y
        #         space.is_snapped = True
        #         unsnap_the_rest(space)
        #         break
        # else:
        #     if not (rect.centerx - space.rect.centerx < 2) or not (rect.centery - space.rect.centery < 2):
        #         is_snapped = False
        #         break


while running:

    for event in pygame.event.get():

        # Close if the user quits the
        # game
        if event.type == QUIT:
            running = False

        # Making the image move
        elif event.type == MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                moving = True

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
            rect.move_ip(event.rel)
            snap_to_space(rect)

    # Set screen color and image on screen
    screen.fill(YELLOW)
    screen.blit(img, rect)

    # Construct the border to the image
    pygame.draw.rect(screen, BLUE, rect, 2)

    draw_board()

    # Update the GUI pygame
    pygame.display.update()



# Quit the GUI game
pygame.quit()
