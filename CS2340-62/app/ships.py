import app.entities as entities


class Ship(object):
    type = ""
    max_cargo = 0
    cargo_space = []
    capacity = 0
    fuel_cap = 0
    current_fuel = 0
    max_health = 0
    current_health = 0

    fuel_cost = 0

    def __init__(self, type, max_cargo, fuel_cap, max_health):
        self.type = type
        self.max_cargo = max_cargo
        self.fuel_cap = fuel_cap
        self.current_fuel = fuel_cap
        self.max_health = max_health
        self.current_health = max_health
        if self.cargo_space != []:
            self.cargo_space = []

    def get_current_fuel(self):
        return self.current_fuel

    def add_cargo(self, name, amount, price):
        if self.capacity + amount > self.max_cargo:
            return False
        else:
            # type = lower(type)
            # if(self.cargo_space.get(item) is None):
            #     self.cargo_space[item] = amount
            # else:
            #     self.cargo_space[item] += amount
            if len(self.cargo_space) > 0:
                for element in self.cargo_space:
                    if element.get_name() == name:
                        element.set_cargo_space(element.get_cargo_space() + amount)
                        self.capacity += amount
                        return True
        self.cargo_space.append(entities.Item(name, amount, price))
        self.capacity += amount
        return True

    def remove_cargo(self, name, amount):
        if len(self.cargo_space) > 0:
            for element in self.cargo_space:
                if element.get_name() == name:
                    element.set_cargo_space(element.get_cargo_space() - amount)
                    self.capacity -= amount;
                    if element.get_cargo_space() == 0:
                        self.cargo_space.remove(element)
                    break

    def get_cargo_space(self):
        return len(self.cargo_space)

    def get_cargo(self):
        return self.cargo_space

    def remove_all_cargo(self):
        self.cargo_space.clear()

    def use_fuel(self, amount):
        amount = float(amount)
        if self.current_fuel - amount < 0:
            return False
        else:
            self.current_fuel -= amount
            return True

    def fill_tank(self, amount):
        self.current_fuel = amount

    def take_damage(self, amount):
        if self.current_health - amount < 0:
            return False
        else:
            self.current_health -= amount
            return True

    def repair(self, amount):
        if self.current_health + amount >= self.max_health:
            self.current_health = self.max_health
        else:
            self.current_health += amount

    def get_current_cargo(self):
        return self.cargo_space

    def get_capacity(self):
        return self.capacity

    def get_max_cargo(self):
        return self.max_cargo

    def get_current_fuel(self):
        return self.current_fuel

    def get_fuel_cap(self):
        return self.fuel_cap

    def get_current_health(self):
        return self.current_health

    def get_max_health(self):
        return self.max_health

    def get_type(self):
        return self.type

    def to_json(self):
        data = {}
        cargo = []
        for item in self.cargo_space:
            cargo.append(item.to_json())
        data["type"] = self.type
        data["max_cargo"] = self.max_cargo
        data["capacity"] = self.capacity
        data["cargo"] = cargo
        data["max_fuel"] = self.fuel_cap
        data["current_fuel"] = self.current_fuel
        data["max_health"] = self.max_health
        data["current_health"] = self.current_health
        return json.dumps(data)


# Ships
class Ladybug(Ship):
    # Ladybug: max_cargo: 100, fuel_cap: 1000, Health: 100
    def __init__(self):
        super().__init__("Ladybug", 10, 1000, 100)


class BumbleBee(Ship):
    # BumbleBee: max_cargo: 200, fuel_cap: 2000, Health: 200
    def __init__(self):
        super().__init__("BumbleBee", 20, 2000, 200)


class Wasp(Ship):
    # Wasp: max_cargo: 300, fuel_cap: 3000, Health: 300
    def __init__(self):
        super().__init__("Wasp", 30, 3000, 300)
