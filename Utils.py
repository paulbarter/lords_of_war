from Units.Spaces import restore_movement_units, remove_movement_hilights


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
        if team_barbarian.turn_nr != 0:
            team_barbarian.turn_nr += 1

    return current_active_team, moving, current_active_unit, active_space, possible_dest_space_ids, team_wolf, team_barbarian