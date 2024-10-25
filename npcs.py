class NPC:
    def __init__(self, npc_dict : {}):
        self.id = npc_dict["id"]
        self.name = npc_dict["name"]
        self.lines = []



# Define NPC dictionaries here

test_npc = {
    "id" : "test_npc",
    "name" : "Testing NPC",
    "lines" : ["Hi", "Hello", "Hey there", "Howdy"],
}