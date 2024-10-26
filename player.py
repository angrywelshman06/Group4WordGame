from types import new_class

import map
from items import *

# Starting inventory
inventory = {Consumable(paracetamol) : 2, Item(item_pen) : 1, Weapon(gun) : 1}

# Current maximum capacity of inventory (in grams)
max_mass = 10000

# Calculates total mass of the inventory
def inventory_mass():
    mass = 0
    for item in inventory:
        mass += item.mass
    return mass


def print_inventory_items():
    if len(inventory) == 0:
        return

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

    print(f"You have {item_list}.")

# Tracks how many individual rooms have been visited
unique_rooms_visited = 0

# Stores players health
health = 100

#Stores current room position as an array
current_room_position = map.starting_position

# Stores the previous room position as an array
# Used for fleeing enemy combat
previous_room_position = None

def get_current_room():
    return map.get_room(current_room_position[0], current_room_position[1])