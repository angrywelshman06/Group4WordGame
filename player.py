from items import *
from map import rooms

# Starting inventory
inventory = [item_id, item_laptop, item_money]

# Current maximum capacity (in grams)
max_mass = 10000

# Calculates total mass of the inventory
def inventory_mass():
    mass = 0
    for item in inventory:
        mass += item["mass"]
    return mass

# Start game at the reception
current_room = rooms["Reception"]
