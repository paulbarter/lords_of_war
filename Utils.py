from Attack import show_popup
from Units.Spaces import restore_movement_units, remove_movement_hilights
import random
import pygame

from sounds.Sounds import play_sound

pygame.init()
font = pygame.font.SysFont(None, 32)


def handle_end_turn(board, screen, current_active_team, moving, current_active_unit, active_space,
                                possible_dest_space_ids, team_wolf, team_barbarian):
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
        team_barbarian.turn_nr += 1
    current_active_team.calculate_resources()
    handle_random_event(current_active_team, screen, team_wolf, team_barbarian, board)

    return current_active_team, moving, current_active_unit, active_space, possible_dest_space_ids, team_wolf, team_barbarian

def increase_random_unit_attack_strength(team, board):
    for space in board:
        if space.units:
            random_unit = random.choice(space.units)
            if random_unit.team == team.type and random_unit.name != 'Settler':
                random_unit.attack_power += 50
                return random_unit

def handle_random_event(current_active_team, screen, team_wolf, team_barbarian, board):
    if current_active_team.name == 'Wolf':
        # End of barbarian's turn is end of both turns
        random_choice = random.randint(1, 10)
        if random_choice > 6:
            play_sound('sounds\\random_event.mp3')
            random_team = random.randint(1, 2)
            event_team = team_wolf if random_team == 1 else team_barbarian
            random_event = random.randint(1, 3)
            if random_event == 1:
                inc_gold = random.randint(1, 5)
                event_team.total_gold += 5
                show_popup(screen, f"Random event for {event_team.name} team! Gain {inc_gold} Gold!", font)
            elif random_event == 2:
                inc_resources = random.randint(1, 5)
                show_popup(screen, f"Random event for {event_team.name} team! Gain {inc_resources} Resources!", font)
                event_team.total_resources += 5
            else:
                random_unit = increase_random_unit_attack_strength(event_team, board)
                show_popup(screen, f"Random event for {event_team.name} team! {random_unit.name} gains 50 attack strength!", font)
