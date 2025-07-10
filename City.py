from Units.BaseUnit import Teams


def calculate_city_occupied(active_team, inactive_team, city):
    if city.owner and city.owner != active_team:
        active_team.owned_cities.append(city)
        inactive_team.owned_cities.remove(city)
    elif not city.owner:
        active_team.owned_cities.append(city)
    city.owner = active_team

class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.units = []
        self.owner = None

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        if unit in self.units:
            self.units.remove(unit)

    def set_owner(self, owner):
        self.owner = owner

    def set_is_occupied(self, owner):
        self.owner = owner

    def __repr__(self):
        return f"City({self.name}, {self.x}, {self.y})"