
from Teams import WolfTeam, BarbarianTeam
from Units.BaseUnit import Jet, Teams, Soldier, Settler
from Units.Spaces import River, Road, Mountain, Plain, City

team_wolf = WolfTeam()
team_barbarian = BarbarianTeam()

def get_board(space_width, space_height):
    space_1_1 = Road(space_width, -50 + space_height)
    space_1_2 = City(space_width * 2, -50 + space_height)
    space_1_3 = Road(space_width * 3, -50 + space_height)
    space_1_4 = City(space_width * 4, -50 + space_height)
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
    space_3_6 = Mountain(space_width * 6, -50 + space_height * 3)
    space_3_7 = Mountain(space_width * 7, -50 + space_height * 3)
    space_3_8 = Mountain(space_width * 8, -50 + space_height * 3)
    space_3_9 = Mountain(space_width * 9, -50 + space_height * 3)

    space_1_1.add_unit(Soldier(1, 2, Teams.WOLF))
    space_2_1.add_unit(Settler(1, 2, Teams.BARBARIAN))
    space_2_2.add_unit(Jet(1, 2, Teams.BARBARIAN))
    space_2_3.add_unit(Jet(1, 2, Teams.WOLF))
    space_3_6.add_unit(Jet(1, 2, Teams.WOLF))

    return [space_1_1, space_1_2, space_1_3, space_1_4, space_1_5, space_1_6, space_1_7, space_1_8, space_1_9,
             space_2_1, space_2_2, space_2_3, space_2_4, space_2_5, space_2_6, space_2_7, space_2_8, space_2_9,
             space_3_1, space_3_2, space_3_3, space_3_4, space_3_5, space_3_6, space_3_7, space_3_8, space_3_9]
