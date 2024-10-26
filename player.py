from types import new_class

import map

from items import *

# Starting inventory
inventory = {Consumable(paracetamol) : 2, Weapon(bat) : 1} # could be changed to the gun idc

# Current maximum capacity of inventory (in grams)
max_mass = 10000

# Calculates total mass of the inventory
def inventory_mass():
    mass = 0
    for item in inventory:
        mass += item.mass
    return mass

def get_inventory_items():
    if len(inventory) == 0:
        return -1

    item_list = ""
    count = 0
    for item in inventory:

        if count == len(inventory) - 1 and len(inventory) > 1:
            item_list += " and "
        elif count != 0:
            item_list += ", "
        item_list += f"{inventory[item]} {item.name}"
        if inventory[item] > 1: item_list += "s"
        count += 1

    return f"You have {item_list}."

# Stores players health
health = 100

#Stores current room position as an array
current_room_position = [4,4]

# Stores the previous room position as an array
# Used for fleeing enemy combat
previous_room_position = None

unique_rooms_visited = 0

def get_current_room():
    return map.get_room(current_room_position[0], current_room_position[1])