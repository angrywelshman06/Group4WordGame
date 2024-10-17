from items import *

# Class for cleanly storing and accessing rooms
class Room:
    def __init__(self):
        self.name = None
        self.description = None
        self.items = None
        self.enemies = None # Might be needed??
        self.exits = None

room_reception = {
    "name": "Reception",

    "description":
    """You are in a maze of twisty little passages, all alike.
Next to you is the School of Computer Science and
Informatics reception. The receptionist, Matt Strangis,
seems to be playing an old school text-based adventure
game on his computer. There are corridors leading to the
south and east. The exit is to the west.""",



    "items": [item_biscuits, item_handbook]

}

room_admins = {
    "name": "MJ and Simon's room",

    "description":
    """You are leaning agains the door of the systems managers'
room. Inside you notice Matt "MJ" John and Simon Jones. They
ignore you. To the north is the reception.""",



    "items": []
}

room_tutor = {
    "name": "your personal tutor's office",

    "description":
    """You are in your personal tutor's office. He intently
stares at his huge monitor, ignoring you completely.
On the desk you notice a cup of coffee and an empty
pack of biscuits. The reception is to the west.""",



    "items": []
}

room_parking = {
    "name": "the parking lot",

    "description":
    """You are standing in the Queen's Buildings parking lot.
You can go south to the COMSC reception, or east to the
general office.""",



    "items": []
}

room_office = {
    "name": "the general office",

    "description":
    """You are standing next to the cashier's till at
30-36 Newport Road. The cashier looks at you with hope
in their eyes. If you go west you can return to the
Queen's Buildings.""",


    "items": [item_pen]
}

# Add special rooms here (replace exercise6 rooms)
special_rooms = [room_admins, room_office, room_parking, room_reception]

# Rooms that will be used as filler, will have no special events and may have randomly generated loot/enemies
generic_rooms = [room_tutor]