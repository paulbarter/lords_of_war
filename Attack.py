import pygame
from sounds.Sounds import play_sound

pygame.init()
font = pygame.font.SysFont(None, 32)

def show_popup(screen, message, font=None):
    if not font:
        font = pygame.font.SysFont(None, 32)

    # Draw semi-transparent overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Black with alpha
    screen.blit(overlay, (0, 0))

    # Draw popup rectangle
    popup_rect = pygame.Rect(0, 0, 600, 200)
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

class Attack():
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.attack_power = attacker.attack_power
        self.defense_power = defender.defense_power

    def calculate_damage(self):
        # Simple damage calculation: attack power minus defense power
        import random
        damage = max(0, int(round((self.attack_power - self.defense_power) * random.random(), 0)))
        return damage

    def execute(self):
        damage = self.calculate_damage()
        self.defender.health -= damage
        self.attacker.movement = 0  # Attacker cannot move after attacking
        if self.defender.health <= 0:
            play_sound('sounds\\explosion.wav')
            play_sound('sounds\\die.wav')
            show_popup(pygame.display.get_surface(), f"{self.defender.name} has been defeated!", font)
            return True  # Defender is defeated
        else:
            play_sound('sounds\\explosion.wav')
            show_popup(pygame.display.get_surface(), f"{self.defender.name} takes {damage} damage!"
                                                     f" health left: {self.defender.health}", font)
            return False  # Defender survives