import random
#from map import map_matrix
#from map import map_matrix, starting_position, rooms

class NPC:
    def __init__(self, npc_dict : {}):
        self.id = npc_dict["id"]
        self.description = npc_dict["description"]
        self.name = npc_dict["name"]
        self.description = npc_dict["description"]
        self.lines = npc_dict["lines"]

    def talk(self):
        print()
        print(f"{self.name}: {random.choice(self.lines)}")
        print()

# Function to place NPCs




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
test_npc = {
    "id" : "test_man",
    "name" : "Testing Man",
    "description" : "Test description",
    "lines" : ["Hi", "Hello", "Hey there", "Howdy"]

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
randomly_placed_npcs = {
        NPC(business_man) : [2, 4],
        NPC(mechanic) : [5, 7],
        NPC(injured_civilian) : [8, 10],

     }




