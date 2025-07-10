
from Teams import WolfTeam, BarbarianTeam
from Units.BaseUnit import BaseUnit, Jet, Teams
from Units.Spaces import BaseSpace, SpaceTypes

team_wolf = WolfTeam()
team_barbarian = BarbarianTeam()

def get_board(space_width, space_height):
    space_1_1 = BaseSpace(space_width, -50 + space_height, SpaceTypes.ROAD)
    space_1_2 = BaseSpace(space_width * 2, -50 + space_height, SpaceTypes.CITY)
    space_1_3 = BaseSpace(space_width * 3, -50 + space_height, SpaceTypes.ROAD)
    space_1_4 = BaseSpace(space_width * 4, -50 + space_height, SpaceTypes.ROAD)
    space_1_5 = BaseSpace(space_width * 5, -50 + space_height, SpaceTypes.ROAD)
    space_1_6 = BaseSpace(space_width * 6, -50 + space_height, SpaceTypes.ROAD)
    space_1_7 = BaseSpace(space_width * 7, -50 + space_height, SpaceTypes.ROAD)
    space_1_8 = BaseSpace(space_width * 8, -50 + space_height, SpaceTypes.ROAD)
    space_1_9 = BaseSpace(space_width * 9, -50 + space_height, SpaceTypes.ROAD)
    space_2_1 = BaseSpace(space_width, -50 + space_height * 2, SpaceTypes.ROAD)
    space_2_2 = BaseSpace(space_width * 2, -50 + space_height * 2, SpaceTypes.ROAD)
    space_2_3 = BaseSpace(space_width * 3, -50 + space_height * 2, SpaceTypes.ROAD)
    space_2_4 = BaseSpace(space_width * 4, -50 + space_height * 2, SpaceTypes.ROAD)
    space_2_5 = BaseSpace(space_width * 5, -50 + space_height * 2, SpaceTypes.ROAD)
    space_2_6 = BaseSpace(space_width * 6, -50 + space_height * 2, SpaceTypes.PLAIN)
    space_2_7 = BaseSpace(space_width * 7, -50 + space_height * 2, SpaceTypes.PLAIN)
    space_2_8 = BaseSpace(space_width * 8, -50 + space_height * 2, SpaceTypes.PLAIN)
    space_2_9 = BaseSpace(space_width * 9, -50 + space_height * 2, SpaceTypes.PLAIN)
    space_3_1 = BaseSpace(space_width, -50 + space_height * 3, SpaceTypes.PLAIN)
    space_3_2 = BaseSpace(space_width * 2, -50 + space_height * 3, SpaceTypes.ROAD)
    space_3_3 = BaseSpace(space_width * 3, -50 + space_height * 3, SpaceTypes.RIVER)
    space_3_4 = BaseSpace(space_width * 4, -50 + space_height * 3, SpaceTypes.ROAD)
    space_3_5 = BaseSpace(space_width * 5, -50 + space_height * 3, SpaceTypes.RIVER)
    space_3_6 = BaseSpace(space_width * 6, -50 + space_height * 3, SpaceTypes.MOUNTAIN)
    space_3_7 = BaseSpace(space_width * 7, -50 + space_height * 3, SpaceTypes.MOUNTAIN)
    space_3_8 = BaseSpace(space_width * 8, -50 + space_height * 3, SpaceTypes.MOUNTAIN)
    space_3_9 = BaseSpace(space_width * 9, -50 + space_height * 3, SpaceTypes.MOUNTAIN)

    space_1_1.add_unit(BaseUnit(1, 2, Teams.WOLF))
    space_2_2.add_unit(BaseUnit(1, 2, Teams.BARBARIAN))
    space_2_2.add_unit(Jet(1, 2, Teams.BARBARIAN))
    space_2_3.add_unit(Jet(1, 2, Teams.WOLF))
    space_3_6.add_unit(Jet(1, 2, Teams.WOLF))

    return [space_1_1, space_1_2, space_1_3, space_1_4, space_1_5, space_1_6, space_1_7, space_1_8, space_1_9,
             space_2_1, space_2_2, space_2_3, space_2_4, space_2_5, space_2_6, space_2_7, space_2_8, space_2_9,
             space_3_1, space_3_2, space_3_3, space_3_4, space_3_5, space_3_6, space_3_7, space_3_8, space_3_9]
