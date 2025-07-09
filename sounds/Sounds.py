import pygame
pygame.init()
pygame.mixer.init()

def play_sound(sound_file):
    try:
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 500))  # Wait for the sound to finish
    except pygame.error as e:
        print(f"Error playing sound {sound_file}: {e}")