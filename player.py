import map
from items import *

# Starting inventory
inventory = []

# Current maximum capacity of inventory (in grams)
max_mass = 10000

# Calculates total mass of the inventory
def inventory_mass():
    mass = 0
    for item in inventory:
        mass += item["mass"]
    return mass

# Stores players health
health = 100

#Stores current room position as an array
current_room_position = map.starting_position

# Stores the previous room position as an array
# Used for fleeing enemy combat
previous_room_position = None

def get_current_room():
    return map.get_room(current_room_position[0], current_room_position[1])