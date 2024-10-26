import random


class NPC:
    def __init__(self, npc_dict : {}):
        self.id = npc_dict["id"]
        self.name = npc_dict["name"]
        self.description = npc_dict["description"]
        self.lines = npc_dict["lines"]

    def talk(self):
        print()
        print(f"{self.name}: {random.choice(self.lines)}")
        print()




# Define NPC dictionaries here

test_npc = {
    "id" : "test_man",
    "name" : "Testing Man",
    "description" : "Test description",
    "lines" : ["Hi", "Hello", "Hey there", "Howdy"]
}

# {NPC : Turns in which the npc is randomly placed on)
randomly_placed_npcs = {
        NPC(test_npc) : [2, 4]
     }
