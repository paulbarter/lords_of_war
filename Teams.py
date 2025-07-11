from Units.BaseUnit import Teams, BaseUnit, Settler

GOLD_PER_CITY = 1
RESOURCES_PER_CITY = 2
GOLD_FOR_SETTLER = 5

class BaseTeam():
    def __init__(self):
        self.name = ""
        self.points = 0
        self.turn_nr = 0
        self.owned_cities = []
        self.total_gold = 0
        self.total_resources = 0

    def calculate_resources(self):
        # TODO - add for farms etc... create city class
        self.total_gold += (GOLD_PER_CITY * len(self.owned_cities))
        self.total_resources += (RESOURCES_PER_CITY * len(self.owned_cities))

    def can_buy_settler(self):
        if self.total_gold >= GOLD_FOR_SETTLER:
            return True

    def buy_settler(self, city, current_active_team):
        self.total_gold -= GOLD_FOR_SETTLER
        city.add_unit(Settler(1, 2, current_active_team.type))

    def get_info(self):
        return [f"Name: {self.name}", f"Points: {self.points}", f"Turn: {self.turn_nr}",
                f"Gold: {self.total_gold}, Resources: {self.total_resources}"]

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