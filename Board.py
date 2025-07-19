
from Units.BaseUnit import Teams, Soldier, Settler, Archer, WolfHero, BarbarianHero
from Units.Spaces import River, Road, Mountain, Plain, City, Forest
import random

def get_board(space_width, space_height):
    space_1_1 = Road(space_width, -50 + space_height)
    space_1_2 = Road(space_width * 2, -50 + space_height)
    space_1_3 = Road(space_width * 3, -50 + space_height)
    space_1_4 = Road(space_width * 4, -50 + space_height)
    space_1_5 = Road(space_width * 5, -50 + space_height)
    space_1_6 = Road(space_width * 6, -50 + space_height)
    space_1_7 = Road(space_width * 7, -50 + space_height)
    space_1_8 = Plain(space_width * 8, -50 + space_height)
    space_1_9 = Plain(space_width * 9, -50 + space_height)
    space_2_1 = Plain(space_width, -50 + space_height * 2)
    space_2_2 = Road(space_width * 2, -50 + space_height * 2)
    space_2_3 = Road(space_width * 3, -50 + space_height * 2)
    space_2_4 = Plain(space_width * 4, -50 + space_height * 2)
    space_2_5 = Plain(space_width * 5, -50 + space_height * 2)
    space_2_6 = Plain(space_width * 6, -50 + space_height * 2)
    space_2_7 = Plain(space_width * 7, -50 + space_height * 2)
    space_2_8 = River(space_width * 8, -50 + space_height * 2)
    space_2_9 = River(space_width * 9, -50 + space_height * 2)
    space_3_1 = River(space_width, -50 + space_height * 3)
    space_3_2 = Road(space_width * 2, -50 + space_height * 3)
    space_3_3 = River(space_width * 3, -50 + space_height * 3)
    space_3_4 = Mountain(space_width * 4, -50 + space_height * 3)
    space_3_5 = Mountain(space_width * 5, -50 + space_height * 3)
    space_3_6 = Road(space_width * 6, -50 + space_height * 3)
    space_3_7 = Road(space_width * 7, -50 + space_height * 3)
    space_3_8 = Mountain(space_width * 8, -50 + space_height * 3)
    space_3_9 = Mountain(space_width * 9, -50 + space_height * 3)

    space_1_1.add_unit(Soldier(1, 2, Teams.WOLF))
    space_2_1.add_unit(Settler(1, 2, Teams.WOLF))
    space_2_2.add_unit(Jet(1, 2, Teams.WOLF))
    space_1_6.add_unit(Soldier(1, 2, Teams.BARBARIAN))
    space_2_6.add_unit(Settler(1, 2, Teams.BARBARIAN))
    space_2_6.add_unit(Jet(1, 2, Teams.BARBARIAN))

    return [space_1_1, space_1_2, space_1_3, space_1_4, space_1_5, space_1_6, space_1_7, space_1_8, space_1_9,
             space_2_1, space_2_2, space_2_3, space_2_4, space_2_5, space_2_6, space_2_7, space_2_8, space_2_9,
             space_3_1, space_3_2, space_3_3, space_3_4, space_3_5, space_3_6, space_3_7, space_3_8, space_3_9]

def make_random_board(width_units, height_units, space_width, space_height, percentage_road=0.3, percentage_river=0.1,
                      percentage_mountain=0.1, percentage_forrest=0.2):
    board = []
    wolf_start_squares = [(0, 0), (1, 0), (0, 1), (1, 1)]
    length = height_units
    breadth = width_units
    barbarian_start_squares = [(length-1, breadth-1), (length -2, breadth-1),
                               (length-1, breadth-2), (length-2, breadth-2)]
    for height_unit in range(height_units):
        for width_unit in range(width_units):
            space_type = Plain
            if (height_unit, width_unit) in wolf_start_squares:
                space_type = Plain
            elif (height_unit, width_unit) in barbarian_start_squares:
                space_type = Plain
            else:
                rand_value = random.random()
                if rand_value < percentage_road:
                    space_type = Road
                elif rand_value < percentage_road + percentage_river:
                    space_type = River
                elif rand_value < percentage_road + percentage_river + percentage_mountain:
                    space_type = Mountain
                elif rand_value < percentage_road + percentage_river + percentage_mountain + percentage_forrest:
                    space_type = Forest

            initialised_space = space_type(space_width * width_unit + 60, 50 + space_height * height_unit)
            board.append(initialised_space)
            if height_unit == 0 and width_unit == 0:
                initialised_space.add_unit(Soldier(1, 2, Teams.WOLF))
                initialised_space.add_unit(Settler(1, 2, Teams.WOLF))
                initialised_space.add_unit(Settler(1, 2, Teams.WOLF))
                initialised_space.add_unit(WolfHero(1, 2, Teams.WOLF))

            if height_unit == height_units -1 and width_unit == width_units -1:
                initialised_space.add_unit(Soldier(1, 2, Teams.BARBARIAN))
                initialised_space.add_unit(Settler(1, 2, Teams.BARBARIAN))
                initialised_space.add_unit(Settler(1, 2, Teams.BARBARIAN))
                initialised_space.add_unit(BarbarianHero(1, 2, Teams.BARBARIAN))
    return board

