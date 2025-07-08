from Units.BaseUnit import Teams

GOLD_PER_CITY = 1
RESOURCES_PER_CITY = 2

class BaseTeam():
    def __init__(self):
        self.name = ""
        self.points = 0
        self.turn_nr = 0
        self.owned_cities = []

    def calculate_resources(self):
        total_gold = 0
        total_resources = 0
        for city in self.owned_cities:
            # TODO - add for farms etc... create city class
            total_gold += GOLD_PER_CITY
            total_resources += RESOURCES_PER_CITY
        return total_gold, total_resources

class WolfTeam(BaseTeam):
    def __init__(self):
        super().__init__()
        self.name = "Wolf"
        self.type = Teams.WOLF

class BarbarianTeam(BaseTeam):
    def __init__(self):
        super().__init__()
        self.name = "Barbarian"
        self.type = Teams.BARBARIAN