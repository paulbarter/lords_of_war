from Attack import show_popup
from Teams import BaseTeam, WolfTeam, BarbarianTeam
from Units.Spaces import restore_movement_units, Plain, City, Mountain, Forest, Road, River
import random
import pygame
import json
import datetime

from sounds.Sounds import play_sound

pygame.init()
font = pygame.font.SysFont(None, 32)

def save_game(board, current_active_team, team_wolf, team_barbarian):
    import json
    game_data = {
        'board': [space.to_dict() for space in board],
        'current_active_team': current_active_team.name,
        'team_wolf': team_wolf.to_dict(),
        'team_barbarian': team_barbarian.to_dict()
    }
    with open(f"saved_games\\{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_game.json", "w") as f:
        json.dump(game_data, f)
    show_popup(pygame.display.get_surface(), "Game saved successfully!", font)

def get_space_object_by_name(space_name, x, y):
    if space_name == "Plain":
        return Plain(x, y)
    elif space_name == "City":
        return City(x, y)
    elif space_name == "Mountain":
        return Mountain(x, y)
    elif space_name == "Forest":
        return Forest(x, y)
    elif space_name == "Road":
        return Road(x, y)
    elif space_name == "River":
        return River(x, y)

def load_game(file_path):
    with open(file_path, "r") as f:
        game_data = json.load(f)
    active_team_name = game_data['current_active_team']
    team_wolf = WolfTeam()
    team_wolf.from_dict(game_data['team_wolf'])
    team_barbarian = BarbarianTeam()
    team_barbarian.from_dict(game_data['team_barbarian'])
    if active_team_name == "Wolf":
        current_active_team = team_wolf
    else:
        current_active_team = team_barbarian
    board = []
    for space_data in game_data['board']:
        space = get_space_object_by_name(space_data['name'], space_data['x'], space_data['y'])
        space.from_dict(space_data, team_wolf, team_barbarian)
        board.append(space)
    return board, current_active_team, team_wolf, team_barbarian

def handle_end_turn(board, screen, current_active_team, moving, current_active_unit, active_space,
                                possible_dest_space_ids, team_wolf, team_barbarian):
    # show_popup(screen, f"Ending turn for team {current_turn}", font)
    restore_movement_units(board, current_active_team)
    current_active_team = team_barbarian if current_active_team.name == 'Wolf' else team_wolf
    moving = False
    current_active_unit = None
    active_space = None
    possible_dest_space_ids = []
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
