import items
from items import *

# Class for cleanly storing and accessing rooms
class Room:
    def __init__(self, room_dict : {}):
        self.name = room_dict["name"]
        self.description = room_dict["description"]
        self.enemies = []
        self.exits = set()

        self.items = []
        for item_dict in room_dict["items"]:
            item = None

            if "type" not in item_dict:
                self.items.append(Item(item_dict))

            match item_dict["type"]:
                case items.Consumable:
                    item = Consumable(item_dict)
                case _:
                    item = Item(item_dict)
            self.items.append(item)






# Special rooms
# Add all to special rooms list at bottom of file

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


# Generic rooms
# Add all to generic rooms list at bottom of file

room_tutor = {
    "name": "your personal tutor's office",

    "description":
    """You are in your personal tutor's office. He intently
stares at his huge monitor, ignoring you completely.
On the desk you notice a cup of coffee and an empty
pack of biscuits. The reception is to the west.""",



    "items": []
}

# Tutorial room
# Do not add to either list, this has been implemented elsewhere
room_tutorial = {
    "name": "ROOM",

    "description":
    """TUTORIAL ROOM DESCRIPTION""",



    "items": [paracetamol]

}

# Add special rooms here (replace exercise 6 rooms)
special_rooms = [room_admins, room_office, room_parking, room_reception]

# Rooms that will be used as filler, will have no special events and may have randomly generated loot/enemies
generic_rooms = [room_tutor]