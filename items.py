class Item:
    def __init__(self, item: {}):
        self.id = item["id"]
        self.name = item["name"]
        self.description = item["description"]
        self.mass = item["mass"]
        pass

class Consumable(Item):
    def __init__(self, item: {}):
        super().__init__(item)
        self.healing = item["healing"]  # How much healing (or damage) the consumable does

    def consume(self):
        import player
        player.health += self.healing
        print("Consumed")


class Weapon(Item):
    def __init__(self, item: {}):
        super().__init__(item)
        self.damage = item["damage"]
        self.crit_chance = item["crit_chance"] # Amount of damage the weapon inflicts
        self.crit_multiplier = item["crit_multiplier"]

    def get_damage(self, crit_bool : bool):
        if crit_bool:
            return self.damage * self.crit_multiplier
        return self.damage


""" 
ITEM INFORMATION

id - unique id of the item
name - the display name of the item
description - brief description of the item to be displayed
mass - the weight of the item in grams
type - The specific type of the item that links to the classes above (Item being default)
       Attributes of each child class can be found in their initialisation functions above 
       (Item attributes are carried to all of them)

IGNORE : NOTE: Add all items to the item list at the bottom of the file to initialise them
"""

item_id_card = {
    "id": "id",

    "name": "id card",

    "description":
        """You new shiny student ID card. Expires 1 June 2017.
    You wonder why they have printed a suicide hotline number on it?...""",

    "mass": 100,

    "type": Item
}

item_laptop = {
    "id": "laptop",

    "name": "laptop",

    "description":
        "It has seen better days. At least it has a WiFi card!",

    "mass": 2000,

    "type": Item
}

item_money = {
    "id": "money",

    "name": "money",

    "description":
        "This wad of cash is barely enough to pay your tuition fees.",

    "mass": 50,

    "type": Item
}

item_biscuits = {
    "id": "biscuits",

    "name": "a pack of biscuits",

    "description": "A pack of biscuits."
    ,

    "mass": 200,

    "type": Item
}

item_pen = {
    "id": "pen",

    "name": "pen",

    "description": "A basic ballpoint pen.",

    "mass": 2000,

    "type": Item
}

item_handbook = {
    "id": "handbook",

    "name": "student handbook",

    "description": "This student handbook explains everything. Seriously.",

    "mass": 200,

    "type": Item,
}

paracetamol = {
    "id": "paracetamol",
    "name": "paracetamol tablet",
    "description": "DESCRIPTION",
    "mass": 100,

    "type": Consumable,

    # Consumable specifics

    "healing": 20
}

morphine = {
    "id": "morphine",
    "name": "morphine",
    "description": "DESCRIPTION",
    "type": Consumable,
    "healing": 50,
    "mass": 100
}

gun = {
    "id" : "gun",
    "name" : "gun",
    "description" : "DESCRIPTION",
    "mass" : 100,
    type: Weapon,
    "damage" : 10,
    "crit_chance" : 0.4,
    "crit_multiplier" : 1.5
}

#items = [item_id_card, item_biscuits, item_handbook, item_laptop, item_money, item_pen]
