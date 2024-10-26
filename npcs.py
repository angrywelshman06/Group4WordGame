import random
from map import map_matrix
from map import map_matrix, starting_position, rooms

class NPC:
    def __init__(self, npc_dict : {}):
        self.id = npc_dict["id"]
        self.description = npc_dict["description"]
        self.name = npc_dict["name"]
        self.lines = npc_dict["lines"]

    def talk(self):
        print()
        print(f"{self.name}: {random.choice(self.lines)}")
        print()

# Function to place NPCs
def place_npcs():
    used_positions = set()

    # Find the river room coordinates
    river_room_position = None
    for y in range(len(map_matrix)):
        for x in range(len(map_matrix[y])):
            if map_matrix[y][x] and map_matrix[y][x].name == rooms.river['name']:
                river_room_position = (x, y)
                break
        if river_room_position:
            break

    # Place the boat captain in the river room
    if river_room_position:
        map_matrix[river_room_position[1]][river_room_position[0]].npc = NPC(boat_captain)
        used_positions.add(river_room_position)

    # Place other NPCs randomly
    for npc_dict in npcs:
        if npc_dict["id"] == "boat_captain":
            continue
        while True:
            x_coord = random.randint(0, len(map_matrix[0]) - 1)
            y_coord = random.randint(0, len(map_matrix) - 1)
            if (x_coord, y_coord) not in used_positions and map_matrix[y_coord][x_coord] is not None:
                map_matrix[y_coord][x_coord].npc = NPC(npc_dict)
                used_positions.add((x_coord, y_coord))
                break




# Define NPC dictionaries here

injured_civilian = {
    "id" : "injured_civilian",
    "description" : "An injured man sits propped against a wall. He is clutching his right arm - or whatever of it that remains. He looks up at you, showing initial fear in his eyes with an assumption of you being a zombie later changing to hope as he sees the humanity behind your eyes. Dread overcomes you knowing he can’t be saved and needs to go.",
    "name" : "Injured Civilian",
    "lines" : ["Hey man, are you a zombie ? Nice seeing another person, I really thought i would die not seeing any humans at all. It's so cold... everything’s blurry. You know when all this my momma said"]
}
boat_captain = {
    "id" : "boat_captain",
    "description": " A huge, burly man stares at you while smoking a cigar, his bulged arms showing his tattoos of a Royal Marines army insignia. He waves at you, calling you towards him.",
    "name" : "Boat Captain",
    "lines" : ["Hey Mate! Nice to see another who hasn’t gone rotten… it's been a while. Suppose you’re trying to find a way out of here? I’ve been trying for weeks now but I managed to crack a pretty big hole in my last working boat. I’m sure I could get us out of ‘ere with some tape to fix the hole in the bottom of me boat. Let me know if you find any..."]
}
mechanic = {
    "id" : "mechanic",
    "description": "The grease-covered mechanic looks up at you, a bloodied spanner in one hand and a tool belt hanging loosely from his waist. His eyes look tired and showing remorse, constantly scanning the room and settling on some of the fly-infested rotten bodies.",
    "name" : "Mechanic",
    "lines" : ["Never thought I’d see another fresh person in here, hope you’re ok bro. I gave up trying to escape after my last screwdriver snapped, pretty sure you could still break into that car in the petrol station too - there’s enough petrol to get you out too just need a crowbar and another screwdriver… shame."]
}
business_man = {
    "id" : "business man",
    "description": "A man in a bloodied suit looks at you, he is panting with sweat trailing down his forehead and tightly clutching his suitcase - with anticipation of you being another zombie in his way.",
    "name" : "Business man",
    "lines" : ["Oh god man, I thought you were a zombie! I’ve been running around looking for a way to escape - I suppose you’re looking for a way out too. I’ve seen some people flying a few times, pretty sure they’re using the skyscraper; however, I’m not sure if there are more parachutes left in here!"]
}



# {NPC : Turns in which the npc is randomly placed on)
# randomly_placed_npcs = {
#         NPC(test_npc) : [2, 4]
#      }
npcs = [injured_civilian, boat_captain, mechanic, business_man]



