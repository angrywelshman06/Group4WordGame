import copy

import items
from items import *
from npcs import *

import ani_sprites
from ani_sprites import *
import player


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
            self.win_requirements = room_dict["win_requirements"] # [{}]

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
                case items.Weapon:
                    item = Weapon(item_dict)
                case _:
                    item = Item(item_dict)
                    
            self.items[item.id] = room_dict["items"][item.id]


    def can_escape(self) -> bool:

        # If there are no win requirements in this room
        if self.win_requirements is None:
            return False

        # For each requirement (if there are multiple ways of escaping through this room)
        for list_of_requirements in self.win_requirements:

            modified_list_of_requirements = copy.deepcopy(list_of_requirements)
            for requirement_type in list_of_requirements: # Item id or specific requirement type (mass)

                for item in player.inventory.keys():
                    match requirement_type:

                        case "mass" :
                            if item.mass > list_of_requirements[requirement_type]:
                                modified_list_of_requirements.pop(requirement_type)
                                break

                        case _: # Assumed to be an item id
                            if item.id == requirement_type and player.inventory[item] >= modified_list_of_requirements[requirement_type]:
                                modified_list_of_requirements.pop(requirement_type)
                                break

            # If there are no more requirements in this set, player can escape if they wish
            if len(modified_list_of_requirements) == 0:
                return True

        return False

# Special rooms
# Add all to special rooms list at bottom of file


# Tutorial room
# Do not add to either list, this has been implemented elsewhere
bedroom_tutorial = {
    "name": "Bedroom (Tutorial)",

    "description":
    """The rotten door led to the bedroom with a creak, it has a bed, with the mattress and the bed sheets not aligned at all.The walls covered with mould and paint long since peeled off, The floorboards creak with every step showing decay betraying its once great quality redwood flooring.  The air smells weird, prompting you to mask your nose from the smell. The once beautiful mattress with flowery design lay dusty with no care. There are stains in the floor , there are cobwebs in the roof and a radio lies on the empty wooden table showing signs of termite infestation.""",

    "visual": ani_sprites.room_tutorial,

    "items": {"paracetamol" : 3},

    "npcs" : [test_npc]

}
bathroom_tutorial = {
    "name": "Bathroom",

    "description":
    """The bathroom is dim and filthy, with flickering lights casting eerie shadows on cracked tiles. The air reeks of mildew and decay. Stalls are broken, toilets clogged with sludge, and graffiti stains the walls. A corroded faucet drips, the only sound breaking the silence. A shattered mirror reflects dust, while scattered papers and torn clothing hint at desperate past occupants. An ominous groan echoes nearby, a reminder that danger lurks just beyond the crumbling walls.""",

    "visual": ani_sprites.room_bathroom,

    "items": {'paracetamol': 2}

}

kitchen_tutorial = {
    "name": "Kitchen",

    "description":
    """The kitchen is a wreck, abandoned and coated in dust. Rusty pots and pans hang crookedly from hooks, while broken cabinets sag, their doors ajar. Dishes sit in a sink filled with stagnant, murky water, covered in mould. The once-shiny countertops are smeared with grime and old food stains, and a cracked fridge stands open, its contents long rotted away. The floor is littered with broken glass, utensils, and scattered cans, as if someone left in a hurry. Faint scratching sounds come from behind the walls, hinting at the infestation that's taken over this forgotten place.""",

    "visual": ani_sprites.room_kitchen,

    "items": {'knife': 1}
}

park = {
    "name": "Park",

    "description":
    """
The park is eerily silent, overgrown with tangled weeds and dying trees. Once-trimmed paths are now cracked and hidden beneath layers of dirt and fallen leaves. Benches lie overturned, some broken, while rusty playground equipment creaks in the breeze. A lone swing sways gently, moved by the wind, its chain rattling ominously. The fountain at the park's centre is dry, its stone crumbling and coated with moss. Scattered belongings—torn backpacks, shoes, and a stuffed animal—are grim reminders of those who once fled in panic. The rustle of bushes and distant growls suggest the park is no longer safe.""",

    "visual": ani_sprites.room_park,

}
the_hood = {
    "name": "The Hood",

    "description":
    """The neighbourhood, once vibrant, is now a ghost town. Houses stand with doors wide open, windows shattered, and lawns overgrown with weeds. Abandoned cars block the streets, and children's toys lay forgotten on driveways. Bloodstains and scattered belongings mark desperate escapes. The eerie silence is broken only by distant howls, the air thick with decay. Every home holds its own untold horror.""",

    "visual": ani_sprites.room_neighbourhood,
}
cinema = {
    "name": "Cinema",

    "description":
    """The cinema is dark and desolate, rows of torn seats covered in dust. The projector room stands abandoned, the last reel frozen mid-scene. Empty popcorn containers and spilled drinks line the aisles, with flickering lights casting long shadows across the screen. The ticket booth is smashed, glass strewn everywhere, and the faint sound of footsteps echo in the lobby, hinting that the undead may have taken over.""",

    "visual": ani_sprites.room_cinema,

}
shopping_centre ={
    "name": "Shopping Centre",

    "description":
    """The shopping centre is a massive, hollow ruin, with looted stores and broken glass everywhere. Mannequins lie dismembered across the floor, their limbs scattered like the humans who once shopped here. The food court is trashed, tables overturned, and trays littered with old, rotting food. Escalators stand frozen, and dark hallways lead to unknown dangers. The silence is heavy, interrupted only by the sound of distant shuffling feet.""",

    "visual": ani_sprites.room_shoppingcentre,
}
graveyard = {
    "name": "Graveyard",

    "description":
    """The graveyard is a haunting place, overgrown with wild grass and forgotten headstones. Many graves have been disturbed, their markers broken or toppled over. Dark, open graves gape like wounds in the earth, while the trees surrounding the area sway eerily in the breeze. The fog that rolls in seems to bring with it the moans of the dead, as if the ground itself is groaning.""",

    "visual": ani_sprites.room_graveyard,
}
supermarket = {
    "name": "Supermarket",

    "description":
    """The supermarket is a chaotic wreck, shelves completely stripped of supplies. Empty cans and broken packaging litter the floor, along with overturned shopping carts. The lights flicker occasionally, but most of the aisles are shrouded in darkness. Bloodstains and shattered glass suggest a violent struggle, while the distant groaning hints at dangers still lurking in the stockroom.""",

    "visual": ani_sprites.room_supermarket,
}
hospital = {
    "name": "Hospital",
    "description":
    """The hospital is a maze of horror, with blood-splattered walls and broken equipment strewn across the floors. Gurneys lie abandoned in the hallways, some with blood-soaked sheets, others overturned. Medical supplies are scattered, and monitors beep faintly in the distance. The stench of death fills the air, and the faint, distant groaning hints at a place that is far from safe. Shadows move behind frosted glass doors, a reminder that not all patients left.""",

    "visual": ani_sprites.room_hospital,
}
pharmacy = {
    "name" : "Pharmacy",
    "description":
    """The pharmacy has been ransacked, with pill bottles and medical supplies scattered everywhere. Empty shelves and broken glass make the place feel abandoned and hopeless. The counters are smeared with blood, and the smell of decaying medicine fills the air. Cabinets hang open, their contents long gone, leaving nothing but the chilling memory of desperation.""",

    "visual": ani_sprites.room_pharmacy,
}
gym = {
    "name": "Gym",

    "description":
    """The gym is abandoned, equipment left mid-use, weights scattered across the floor. Bloodstained treadmills and broken mirrors reflect the chaos of a frantic escape. Lockers stand open, their contents looted or forgotten, while the faint smell of sweat mixes with decay. The echo of a distant thud suggests that someone—or something—still lingers.""",

    "visual": ani_sprites.room_gym,
}
firestation = {
    "name": "Fire Station",
    "description":
    """The fire station is a shell of its former self, with overturned fire trucks and smashed windows. Firefighting gear is scattered, and the alarms sit silent, covered in dust. A calendar on the wall is frozen in time, showing the date when everything changed. The smell of gasoline mixes with the stench of death, and the empty pole in the middle of the room seems to promise no one will come to the rescue now.""",

    "visual": ani_sprites.room_firestation,
}
fastfoodplace = {
    "name": "Fast Food Place",

    "description":
    """The fast food place is a wreck, with tables overturned and grease-stained floors slick with grime. Cash registers hang open, looted of money long ago, while trays of half-eaten meals have turned to rot. Bloodstains on the walls suggest a violent struggle, and the once-vibrant posters advertising meals are faded and torn. The fryers are cold, and the stench of decay lingers in the air.""",

    "visual": ani_sprites.room_fastfood,
}
conveniencestore = {
    "name": "Convenience Store",

    "description":
    """The convenience store is a chaotic mess, shelves emptied by frantic looters. The shattered glass door crunches underfoot, and the few remaining items lie scattered on the floor—old magazines, expired snacks, and empty water bottles. Blood splatters on the counter and walls tell the story of a grim struggle. The place feels eerie, with an unnatural quiet as if waiting for the next wave of chaos.""",

    "visual": ani_sprites.room_convenience,
}
trainstation = {
    "name": "Train Station",

    "description":
    """The train station is abandoned, with empty platforms stretching into the darkness. The tracks are overgrown with weeds, and luggage lies discarded, as if its owners fled in a hurry. Flickering lights barely illuminate the shattered ticket booths and benches. Echoes of footsteps reverberate through the cavernous space, but no trains will ever arrive. Bloodstains and broken glass litter the ground, hinting at the violent panic that swept through.""",

    "visual": ani_sprites.room_trainstation,
}
library = {
    "name": "Library",

    "description":
    """The library is a forgotten relic, its once-organised shelves now overturned and chaotic. Books are scattered across the floor, many torn or bloodstained. The soft creak of shelves breaking under their own weight adds to the unsettling quiet. Dust coats everything, and the smell of old paper and decay fills the air. The sound of shuffling pages from deeper within suggests someone—or something—is still searching for answers in the silence.""",

    "visual": ani_sprites.room_library,
}
hairdresser = {
    "name": "Hairdresser",

    "description":
    """The hairdresser's is a mess, with chairs overturned and mirrors shattered. Scissors and combs lie abandoned on the floor, and hair dye stains the walls. The smell of chemicals mixes with the stench of decay, and the faint sound of a radio playing in the background adds to the eerie atmosphere. Bloodstains on the floor hint at a violent struggle, while the empty chairs seem to wait for customers who will never return.""",

    "visual": ani_sprites.room_hairdressers,
}
airport = {
    "name": "Airport",

    "description":
    """The airport is a sprawling ruin of chaos. Luggage is strewn everywhere, and the once-bustling terminals are silent, save for the distant groan of the undead. Planes sit abandoned on the runway, their passengers long gone. The security lines are in disarray, with bins and scattered belongings littering the area. Departure screens flicker with outdated flights, and the eerie silence only amplifies the sense of dread.""",

    "visual": ani_sprites.room_airport,
}
skyscraper = {
    "name": "Skyscraper",

    "description":
    """The skyscrapers are looking half demolished with its parts and debris splattered everywhere and hanging against its walls with bland and dull appearances.""",

    "visual": ani_sprites.room_skyscraper, 

    "win_requirements" : [
        {"parachute" : 1}
    ],

    "escape_animation" : ending_parachute,

}
road = {
    "name": "Road",

    "description":
    """Roads are dirty and are turned upside down with waste particles, damaged cars and  scattered everywhere with major potholes planted around.""",

    "visual": ani_sprites.room_road,
}
armoured_van = {
    "name": "Armoured Van",

    "description":
    """The armoured van, once a fortress on wheels, now sits abandoned with its thick, reinforced doors left slightly ajar. Bullet holes riddle its sides, and the cracked windshield is smeared with dust and grime. Inside, empty crates and torn money bags are strewn across the floor, a silent testament to the chaos and desperation that once unfolded here.""",

    "visual": ani_sprites.room_armoredvan,
}
bank = {
    "name": "Bank",
    "description":
    """The bank’s lobby is eerily silent, with shattered glass doors and overturned counters. Security cameras hang lifeless from the ceiling, and vault doors are left wide open, their contents looted, while scattered bills and coins lay strewn across the marble floors, forgotten in the chaos.""",

    "visual": ani_sprites.room_bank,
}
arcade = {
    "name": "Arcade",
    "description":
    """The arcade, once filled with flashing lights and excited laughter, is now a graveyard of broken machines and shattered screens. Prize claw machines stand empty, their glass cracked, and old tokens litter the floor beneath games that will never be played again, their cheerful music silenced forever.""",

    "visual": ani_sprites.room_arcade,
}
nursery = {
    "name": "Nursery",
    "description":
    """
The nursery is a heartbreaking scene, with tiny chairs tipped over and children's toys scattered across the floor. The walls, once brightly painted with cheerful murals, are peeling, and cribs sit empty, their blankets left askew as if their occupants were snatched away in a hurry.""",

    "visual": ani_sprites.room_nursery,
}
pub = {
    "name": "Pub",
    "description":
    """The pub, once filled with laughter and clinking glasses, now stands in eerie silence, its stools overturned and tables coated in dust. Broken bottles and scattered chairs litter the floor, while the faint smell of stale alcohol mixes with the scent of decay, and shadows move unnervingly in the corners.""",

    "visual": ani_sprites.room_pub,
}
river = {
    "name": "River",
    "description":
    """The river, once a flowing lifeline, is now sluggish and murky, its waters dark and polluted with debris. Plastic bottles, driftwood, and other trash float along the surface, and the smell of decay hangs heavy in the air, while the distant sound of something splashing suggests the water isn’t as lifeless as it seems.""",
    "win_requirements" : [
        {"duct_tape" : 1},
    ],

    "npcs" : [boat_captain],

    "escape_animation" : ending_boat,

    "visual": ani_sprites.room_river,

}
petrol_station = {
    "name": "Petrol Station",
    "description":
    """The petrol station is a wasteland of rusting pumps and broken glass, with abandoned cars still parked at the empty fuel bays. The flickering neon sign buzzes faintly, casting a pale glow on the shattered windows of the convenience store, while dried bloodstains on the tarmac hint at a chaotic, violent end.""",
    "win_requirements" : [
        {"crowbar" : 1, "screwdriver" : 1},
    ],

    "npcs" : [mechanic],

    "escape_animation" : ending_car,

    "visual": ani_sprites.room_petrol,
}




special_rooms = [kitchen_tutorial, park, the_hood, cinema, shopping_centre, graveyard, supermarket, hospital, pharmacy, gym, firestation, fastfoodplace, conveniencestore, trainstation, library, hairdresser, airport, skyscraper, road, armoured_van, bank, arcade, nursery, pub, river, petrol_station]

generic_rooms = ['Vet', 'Telephone box', 'Church', 'Bus stop', 'Open-Air Markets', 'Bike street stand', 'Post office', 'Pedestrian tunnels', 'Drive thru_restaurant', 'Sports bar', 'Construction area', 'Street supermarket', 'Abandoned concert aren', 'Firearms Dealers', 'Abandoned yacht', 'Abandoned beach', 'Radio station', 'Status area', 'Cafe', 'Abandoned car mechanics', 'Abandoned nightclub', 'Street smoking area', 'Abandoned aquarium', 'Dock', 'Abandoned clothing workshop', 'Abandoned factory', 'Dance arena', 'Abandoned zoo', 'Abandoned museum', 'Ice cream store', 'Abandoned gaming store', 'Time Capsule Room', 'Abandoned elderly home', 'Kids playground', 'Astroturf', 'Golf course', 'Tennis court', 'Basketball court', 'Karting course', 'Farm', 'Animal shed', 'Abandoned cinema', 'Forest', 'Canyon', 'Pond', 'Beach', 'Meadow', 'Canyon', 'Lake', 'Athletic Track', 'Ice Skating Rink']
