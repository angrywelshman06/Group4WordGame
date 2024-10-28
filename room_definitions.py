# Class for cleanly storing and accessing rooms


class Room:
    def __init__(self, room_dict: {}, position: tuple, no_enemies=False, visual_in=None):
        self.name = room_dict["name"]
        self.description = room_dict["description"]

        if "escape_animation" in room_dict:
            self.escape_animation = room_dict["escape_animation"]

        self.enemies = {}
        self.exits = set()
        self.exits = {"north", "south", "east", "west"}
        self.position = position

        if self.position[0] == 9:
            self.exits.discard("east")
        if self.position[0] == 0:
            self.exits.discard("west")
        if self.position[1] == 9:
            self.exits.discard("south")
        if self.position[1] == 0:
            self.exits.discard("north")

        if visual_in is not None:
            self.visual = visual_in

        self.visited = False

        # Copying over win requirements from the room dictionary
        self.win_requirements = None
        if "win_requirements" in room_dict:
            self.win_requirements = room_dict["win_requirements"]  # [{}]

        self.npcs = []

        # Initialising each NPC in the dictionary and storing into room object
        if "npcs" in room_dict:
            for npc in room_dict["npcs"]:
                self.npcs.append(NPC(npc))

        self.items = {}

        if "items" not in room_dict:
            return

        for key in room_dict["items"]:
            # Searching for item dictionary
            item_dict = None
            for item_dictionary in item_list:
                if item_dictionary["id"] == key:
                    item_dict = item_dictionary

            if item_dict is None:
                print(f"Wrong id in {self.name} (rooms.py) : {key}\nItem not loaded in room")
                continue

            if "type" not in item_dict:
                item = Item(item_dict)
                if item in room_dict["items"]:
                    self.items[item] = room_dict["items"][item]
                continue

            match item_dict["type"]:
                case items.Consumable:
                    item = Consumable(item_dict)
                case _:
                    item = Item(item_dict)

            self.items[item.id] = room_dict["items"][item.id]