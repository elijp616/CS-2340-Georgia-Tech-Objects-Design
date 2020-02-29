from enum import Enum
from app.ships import *
import random
import math
import json


class techLevel(Enum):
    PREAG = 1
    AGRICULTURE = 2
    MEDIEVAL = 3
    RENAISSANCE = 4
    INDUSTRIAL = 5
    MODERN = 6
    FUTURISTIC = 7
    
    def to_json(self):
        data["name"] = self.name
        data["value"] = self.value
        return json.dumps(data)

class Item():
    name = ""
    cargo_space = 1
    price = 0

    def __init__(self, name="", cargo_space=1, price=1):
        self.name = name
        self.cargo_space = cargo_space
        self.price = price

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_cargo_space(self):
        return self.cargo_space

    def set_cargo_space(self, cargo_space):
        self.cargo_space = cargo_space

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def to_json(self):
        data={}
        data["name"] = self.name
        data["cargo_space"] = self.cargo_space
        data["price"] = self.price
        return json.dumps(data)

class Market():
    # name, cargo space, price

    tech_level = techLevel(3)
    price_multiplier = 1

    items = [Item("spear", 3, 5),
             Item("axe", 2, 6),
             Item("hatchet", 2, 7),
             Item("arrowhead", 1, 1),
             Item("beef", 1, 5),
             Item("chicken", 1, 5),
             Item("animal pelt", 3, 12),
             Item("flint", 1, 1),
             Item("stick", 3, 1),
             Item("root", 1, 1),
             ]  # default to the PREAG, add more items as we check each tech level

    def get_tech_level(self):
        return self.tech_level

    def fill_inventory(self):
        #print("dwadwaL " + str(self.tech_level))
        print("inventory is being filled with: " + str(self.tech_level))
        if self.tech_level.value >= 2:  # AGRI
            agri_items = [Item("rake", 3, 5),
                          Item("carrots", 2, 5),
                          Item("soil", 1, 3),
                          Item("cow", 10, 10),
                          Item("pig", 9, 10),
                          Item("knife", 1, 8),
                          Item("wheat", 2, 7),
                          Item("cotton", 2, 13),
                          Item("tobacco", 2, 11),
                          Item("hoe", 3, 8),
                          ]
            self.items = agri_items
        if self.tech_level.value >= 3:
            medi_items = [Item("longsword", 10, 15),
                          Item("shield", 9, 15),
                          Item("saddle", 5, 13),
                          Item("bow", 4, 13),
                          Item("arrow", 2, 7),
                          Item("dagger", 2, 8),
                          Item("candle", 1, 9),
                          Item("plate", 1, 5),
                          Item("robes", 3, 14),
                          Item("poison", 1, 15),
                          ]
            self.items = medi_items
        if self.tech_level.value >= 4:
            rena_items = [Item("paintbrush", 2, 10),
                          Item("canvas", 6, 10),
                          Item("book", 1, 20),
                          Item("art", 3, 20),
                          Item("journal", 2, 15),
                          Item("compass", 1, 14),
                          Item("pencil", 1, 9),
                          Item("pen", 1, 9),
                          Item("glass", 5, 16),
                          Item("spectacle", 1, 20),
                          ]
            self.items = rena_items
        if self.tech_level.value >= 5:
            indu_items = [Item("gun", 2, 25),
                          Item("cigarette", 1, 20),
                          Item("coal", 3, 25),
                          Item("jacket", 2, 21),
                          Item("top hat", 3, 23),
                          Item("lightbulb", 2, 30),
                          Item("ink", 3, 25),
                          Item("dog", 5, 40),
                          Item("firewood", 6, 30),
                          Item("collared shirt", 4, 45),
                          ]
            self.items = indu_items
        if self.tech_level.value >= 6:
            mode_items = [Item("phone", 3, 55),
                          Item("laptop", 1, 20),
                          Item("tablet", 3, 25),
                          Item("medicine", 2, 21),
                          Item("fast food", 3, 23),
                          Item("DVD", 2, 30),
                          Item("newspaper", 3, 25),
                          Item("protein bar", 5, 40),
                          Item("pepper spray", 6, 30),
                          Item("graphic t-shirt", 4, 45),
                          ]
            self.items = mode_items
        if self.tech_level.value >= 7:
            futu_items = [Item("laser gun", 3, 70),
                          Item("robot", 8, 50),
                          Item("super medicine", 3, 25),
                          Item("satellite", 12, 90),
                          Item("solar ray", 3, 23),
                          Item("flying car", 2, 130),
                          Item("cool jacket", 3, 25),
                          Item("e-sunglasses", 1, 40),
                          Item("smart dog", 6, 30),
                          Item("hologram", 4, 45),
                          ]
            self.items = futu_items
        # Run all the items through the price calculator
        for item in self.items:
            new_price = item.get_price() * 1+self.price_multiplier
            print("setting old price: " + str(item.get_price()) + " to new one: " + str(new_price))
            item.set_price(new_price)

    def __init__(self, tech_level, price_multiplier):
        self.tech_level = tech_level
        self.price_multiplier = price_multiplier
        print("brought in: " + str(tech_level.value))
        self.fill_inventory()

    def get_current_cargo(self):
        return self.items
    
    def to_json(self):
        data = []
        for item in self.items:
            data.append(item.to_json())
        return json.dumps(data)

class Region():
    x_coord = 0
    y_coord = 0
    tech_level = techLevel(1)
    name = ""
    price_multiplier = 0
    market = None

    def __init__(self, x, y, tech_level, name):
        print("region tech??: " + str(tech_level))
        self.x_coord = x
        self.y_coord = y
        self.tech_level = tech_level
        self.name = name
        self.price_multiplier = round(abs(x + y) / 500, 2)
        self.market = Market(tech_level, self.price_multiplier)
        self.market.fill_inventory()
        print(self.market.get_current_cargo()[0].name)

    def get_x(self):
        return self.x_coord

    def get_y(self):
        return self.y_coord

    def get_name(self):
        return self.name

    def get_tech_level(self):
        return self.tech_level

    def get_market(self):
        return self.market

    def to_json(self):
        data = {}
        data["name"] = self.name
        data["x_coord"] = self.x_coord
        data["y_coord"] = self.y_coord
        data["tech_level"] = self.tech_level.to_json()
        data["market"] = self.market.to_json()
        return json.dumps(data)

class User():
    name = ""
    pilot_skill = 0
    fighter_skill = 0
    merchant_skill = 0
    engineer_skill = 0
    credits = 0
    region = Region(0, 0, techLevel(1), "Default")
    ship = Ladybug()

    def __init__(self):
        pass

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_pilot_skill(self):
        return self.pilot_skill

    def set_pilot_skill(self, skill):
        self.pilot_skill = skill

    def get_fighter_skill(self):
        return self.fighter_skill

    def set_fighter_skill(self, skill):
        self.fighter_skill = skill

    def get_merchant_skill(self):
        return self.merchant_skill

    def set_merchant_skill(self, skill):
        self.merchant_skill = skill

    def get_engineer_skill(self):
        return self.engineer_skill

    def set_engineer_skill(self, skill):
        self.engineer_skill = skill

    def get_credits(self):
        return self.credits

    def set_credits(self, credits):
        self.credits = credits

    def get_region(self):
        return self.region

    def set_region(self, region):
        self.region = region

    def set_ship(self, ship):
        self.ship = ship

    def get_ship(self):
        return self.ship
    
    def to_json(self):
        data["name"] = self.name
        data["credits"] = self.credits
        data["pilot_skill"] = self.pilot_skill
        data["fighter_skill"] = self.fighter_skill
        data["merchant_skill"] = self.merchant_skill
        data["engineer_skill"] = self.engineer_skill
        data["region"] = self.region.get_name()
        data["ship"] = self.ship.to_json()


class Game():
    names = ['Plantar', 'Jantar', 'Cantar', 'Exodous', 'Beef',
             'Tanger', 'Pangeria', 'Tanzia', 'Lokus', 'Asakuki']
    gameDifficulty = ""
    x_coord = 10

    def __init__(self):
        pass

    def set_difficulty(self, difficulty):
        self.gameDifficulty = difficulty

    def start_game(self, player, universe):
        if (self.gameDifficulty == "easy"):
            self.x_coord = 1000
        elif (self.gameDifficulty == "medium"):
            self.x_coord = 500
        player.set_credits(self.x_coord)
        universe.create_universe(self.names)
        player.set_region(universe.regionList[random.randint(0, 9)])

    def get_difficulty(self):
        return self.gameDifficulty


class Universe():
    regionList = []

    def __init__(self):
        pass

    def get_region(self, num):
        return self.regionList[num]

    def get_region_list(self):
        return self.regionList

    def create_universe(self, regions):
        if (self.regionList != []):
            self.regionList = []
        usedCoords = []
        for region in regions:
            currCoords = []
            x = random.randrange(-200, 200, 5)
            y = random.randrange(-200, 200, 5)
            currCoords.append(x)
            currCoords.append(y)

            if currCoords not in usedCoords:
                usedCoords.append(currCoords)
            else:
                x = random.randrange(-200, 200, 3)
                y = random.randrange(-200, 200, 3)
                currCoords.append(x)
                currCoords.append(y)
                usedCoords.append(currCoords)

            self.regionList.append(Region(x, y, techLevel(random.randint(1, 7)), region))
            
    def to_json(self):
        data = []
        for region in self.regionList:
            data.append(region.to_json())
        return json.dumps(data)

class Calculations:
    def __init__(self):
        pass

    def distance_x_y(self, x1, y1, x2, y2):
        return sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))
