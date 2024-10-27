
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


class Weapon(Item):
    def __init__(self, item: {}):
        super().__init__(item)
        self.damage = item["damage"] # Amount of damage the weapon inflicts
        self.crit_chance = item["crit_chance"] # critical hit chance
        self.crit_mult = item["crit_mult"] # critical hit multiplier

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

paracetamol = {
    "id": "paracetamol",
    "name": "paracetamol tablet",
    "description": "DESCRIPTION",
    "mass": 100,

    "spawn_chance": 0.23,
    "spawn_quantity" : [1, 5],

    "type": Consumable,

    # Consumable specifics

    "healing": 45,
}

morphine = {
    "id": "morphine",
    "name": "morphine",
    "description": "DESCRIPTION",

    "spawn_chance": 0.23,
    "spawn_quantity" : [1, 2],

    "type": Consumable,
    "healing": 70,
    "mass": 100
}

gun = {
    "id" : "shotgun",
    "name" : "shotgun",
    "description" : "DESCRIPTION",
    "mass" : 3500,

    "spawn_chance": 0.23,
    "spawn_quantity": [1, 1],

    "type": Weapon,
    "damage" : 35,
    "crit_chance" : 0.4,
    "crit_multiplier" : 1.5
}


parachute = {
    "id" : "parachute",
    "name" : "parachute",
    "description" : "DESCRIPTION",
    "mass" : 9000,

    "spawn_chance": 0.80,
    "spawn_quantity": [1, 1],

}

explosives = {
    "id" : "explosives",
    "name" : "explosives",
    "description" : "DESCRIPTION",
    "mass" : 45000,

    "spawn_chance": 0.23,
    "spawn_quantity" : [1, 1],

}

lighter = {
    "id" : "lighter",
    "name" : "lighter",
    "description" : "DESCRIPTION",
    "mass" : 21,

    "spawn_chance": 0.23,
    "spawn_quantity": [1, 1],

}

rope = {
    "id" : "rope",
    "name" : "rope",
    "description" : "DESCRIPTION",
    "mass" : 3900,

    "spawn_chance": 0.23,
    "spawn_quantity": [1, 1],

}

duct_tape = {
    "id" : "duct_tape",
    "name" : "duct tape",
    "description" : "DESCRIPTION",
    "mass" : 350,

    "spawn_chance": 0.23,
    "spawn_quantity": [1, 1],

}

crowbar = {
    "id" : "crowbar",
    "name" : "crowbar",
    "description" : "DESCRIPTION",


    "spawn_chance": 0.23,
    "spawn_quantity": [1, 1],
  
    "mass" : 4500
}

screwdriver = {
    "id" : "screwdriver",
    "name" : "screwdriver",
    "description" : "DESCRIPTION",
    "mass" : 80,

    "spawn_chance": 0.23,
    "spawn_quantity": [1, 1],

}

starter_knife = {
    "id" : "knife",
    "name" : "knife",
    "description" : "DESCRIPTION",
    "type" : Weapon,
    "mass" : 240,
    "damage" : 20,
    "crit_chance" : 0.2,
    "crit_multiplier" : 2,

    "spawn_chance": 0.13,
    "spawn_quantity": [1, 1],

}

machete = {
    "id" : "machete",
    "name" : "machete",
    "description" : "DESCRIPTION",
    "mass" : 250,

    "type" : Weapon,
    "damage" : 25,
    "crit_chance" : 0.4,
    "crit_multiplier" : 2,

    "spawn_chance": 0.13,
    "spawn_quantity": [1, 1],

}

grappling_hook = {
    "id": "grappling_hook",
    "name": "grappling hook",
    "description": "DESCRIPTION",

    "spawn_chance": 0.5,
    "spawn_quantity": [1, 1],

    "mass": 5000
}

ammo = {
    "id": "ammo",
    "name": "ammo",
    "description": "DESCRIPTION",
    "mass": 21,

    "spawn_chance": 0.5,
    "spawn_quantity": [1, 3],

}

bat = {
    "id": "bat",
    "name" : "baseball bat",
    "description" : "DESCRIPTION",
    "type": Weapon,
    "damage" : 15,
    "crit_chance": 0.1,
    "crit_mult": 2,
    "mass": 1500,

    "spawn_chance": 0.03,
    "spawn_quantity": [1, 1],

}

item_list = [paracetamol, morphine, gun, parachute,
             explosives, lighter, rope, duct_tape,
             crowbar, screwdriver, starter_knife,
             machete, ammo, grappling_hook, bat]

def get_item_dict_from_list(item_id : str) -> {}:
    for item_dict in item_list:
        if item_dict["id"] == item_id:
            return item_dict
    return None

def dict_to_item(item_dict : {}):
    if "type" not in item_dict:
        item = Item(item_dict)
        return item

    match item_dict["type"].__name__:
        case Consumable.__name__:
            item = Consumable(item_dict)
        case _:
            item = Item(item_dict)
    return item
