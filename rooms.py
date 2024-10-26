import copy
import items
from items import *
import player
from npcs import *


# Class for cleanly storing and accessing rooms
class Room:
    def __init__(self, room_dict: {}, position: tuple):
        self.name = room_dict["name"]
        self.description = room_dict["description"]
        self.enemies = {}
        self.exits = set()
        self.position = position
        self.visited = False
        self.npcs = []
        if "npcs" in room_dict:
            for npc in room_dict["npcs"]:
                self.npcs.append(npc)
        self.win_requirements = None
        if "win_requirements" in room_dict:
            self.win_requirements = room_dict["win_requirements"] # [{}]

        self.npcs = []

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

    def can_escape(self) -> bool:

        # If there are no win requirements in this room
        if self.win_requirements is None:
            return False

        # For each requirement (if there are multiple ways of escaping through this room)
        for list_of_requirements in self.win_requirements:
            modified_list_of_requirements = copy.deepcopy(list_of_requirements)
            for requirement_type in list_of_requirements: # the item
                for item in player.inventory.keys():
                    match requirement_type:
                        case "mass" :
                            if item.mass > list_of_requirements[requirement_type]:
                                modified_list_of_requirements.pop(requirement_type)
                                break

                        case _:
                            if item.id == requirement_type and player.inventory[item] >= modified_list_of_requirements[requirement_type]:
                                modified_list_of_requirements.pop(requirement_type)
                                break
            if len(modified_list_of_requirements) == 0:
                return True

        return False

# Special rooms
# Add all to special rooms list at bottom of file


# Tutorial room
# Do not add to either list, this has been implemented elsewhere
bedroom_tutorial = {
    "name": "bedroom_tutorial",

    "description":
    """The rotten door led to the bedroom with a creak, it has a bed, with the mattress and the bed sheets not aligned at all.The walls covered with mould and paint long since peeled off, The floorboards creak with every step showing decay betraying its once great quality redwood flooring.  The air smells weird, prompting you to mask your nose from the smell. The once beautiful mattress with flowery design lay dusty with no care. There are stains in the floor , there are cobwebs in the roof and a radio lies on the empty wooden table showing signs of termite infestation.""",



    "items": {"paracetamol" : 2},

    "win_requirements" : [
        {"paracetamol" : 20, "mass" : 100}
    ],

    "npcs" : []


}
bathroom_tutorial = {
    "name": "Bathroom",

    "description":
    """The bathroom is dim and filthy, with flickering lights casting eerie shadows on cracked tiles. The air reeks of mildew and decay. Stalls are broken, toilets clogged with sludge, and graffiti stains the walls. A corroded faucet drips, the only sound breaking the silence. A shattered mirror reflects dust, while scattered papers and torn clothing hint at desperate past occupants. An ominous groan echoes nearby, a reminder that danger lurks just beyond the crumbling walls.""",



    "items": {'paracetamol': 2}

}

kitchen_tutorial = {
    "name": "Kitchen",

    "description":
    """The kitchen is a wreck, abandoned and coated in dust. Rusty pots and pans hang crookedly from hooks, while broken cabinets sag, their doors ajar. Dishes sit in a sink filled with stagnant, murky water, covered in mould. The once-shiny countertops are smeared with grime and old food stains, and a cracked fridge stands open, its contents long rotted away. The floor is littered with broken glass, utensils, and scattered cans, as if someone left in a hurry. Faint scratching sounds come from behind the walls, hinting at the infestation that's taken over this forgotten place.""",

    "items": {'knife': 1}
}

park = {
    "name": "Park",

    "description":
    """
The park is eerily silent, overgrown with tangled weeds and dying trees. Once-trimmed paths are now cracked and hidden beneath layers of dirt and fallen leaves. Benches lie overturned, some broken, while rusty playground equipment creaks in the breeze. A lone swing sways gently, moved by the wind, its chain rattling ominously. The fountain at the park's centre is dry, its stone crumbling and coated with moss. Scattered belongings—torn backpacks, shoes, and a stuffed animal—are grim reminders of those who once fled in panic. The rustle of bushes and distant growls suggest the park is no longer safe.""",
}
the_hood = {
    "name": "The Hood",

    "description":
    """The neighbourhood, once vibrant, is now a ghost town. Houses stand with doors wide open, windows shattered, and lawns overgrown with weeds. Abandoned cars block the streets, and children's toys lay forgotten on driveways. Bloodstains and scattered belongings mark desperate escapes. The eerie silence is broken only by distant howls, the air thick with decay. Every home holds its own untold horror.""",
}
cinema = {
    "name": "Cinema",

    "description":
    """The cinema is dark and desolate, rows of torn seats covered in dust. The projector room stands abandoned, the last reel frozen mid-scene. Empty popcorn containers and spilled drinks line the aisles, with flickering lights casting long shadows across the screen. The ticket booth is smashed, glass strewn everywhere, and the faint sound of footsteps echo in the lobby, hinting that the undead may have taken over.""",
}
shopping_centre ={
    "name": "Shopping Centre",

    "description":
    """The shopping centre is a massive, hollow ruin, with looted stores and broken glass everywhere. Mannequins lie dismembered across the floor, their limbs scattered like the humans who once shopped here. The food court is trashed, tables overturned, and trays littered with old, rotting food. Escalators stand frozen, and dark hallways lead to unknown dangers. The silence is heavy, interrupted only by the sound of distant shuffling feet.""",
}
graveyard = {
    "name": "Graveyard",

    "description":
    """The graveyard is a haunting place, overgrown with wild grass and forgotten headstones. Many graves have been disturbed, their markers broken or toppled over. Dark, open graves gape like wounds in the earth, while the trees surrounding the area sway eerily in the breeze. The fog that rolls in seems to bring with it the moans of the dead, as if the ground itself is groaning.""",
}
supermarket = {
    "name": "Supermarket",

    "description":
    """The supermarket is a chaotic wreck, shelves completely stripped of supplies. Empty cans and broken packaging litter the floor, along with overturned shopping carts. The lights flicker occasionally, but most of the aisles are shrouded in darkness. Bloodstains and shattered glass suggest a violent struggle, while the distant groaning hints at dangers still lurking in the stockroom.""",
}
hospital = {
    "name": "Hospital",
    "description":
    """The hospital is a maze of horror, with blood-splattered walls and broken equipment strewn across the floors. Gurneys lie abandoned in the hallways, some with blood-soaked sheets, others overturned. Medical supplies are scattered, and monitors beep faintly in the distance. The stench of death fills the air, and the faint, distant groaning hints at a place that is far from safe. Shadows move behind frosted glass doors, a reminder that not all patients left.""",
}
pharmacy = {
    "name" : "Pharmacy",
    "description":
    """The pharmacy has been ransacked, with pill bottles and medical supplies scattered everywhere. Empty shelves and broken glass make the place feel abandoned and hopeless. The counters are smeared with blood, and the smell of decaying medicine fills the air. Cabinets hang open, their contents long gone, leaving nothing but the chilling memory of desperation.""",
}
gym = {
    "name": "Gym",

    "description":
    """The gym is abandoned, equipment left mid-use, weights scattered across the floor. Bloodstained treadmills and broken mirrors reflect the chaos of a frantic escape. Lockers stand open, their contents looted or forgotten, while the faint smell of sweat mixes with decay. The echo of a distant thud suggests that someone—or something—still lingers.""",
}
firestation = {
    "name": "Fire Station",
    "description":
    """The fire station is a shell of its former self, with overturned fire trucks and smashed windows. Firefighting gear is scattered, and the alarms sit silent, covered in dust. A calendar on the wall is frozen in time, showing the date when everything changed. The smell of gasoline mixes with the stench of death, and the empty pole in the middle of the room seems to promise no one will come to the rescue now.""",
}
fastfoodplace = {
    "name": "Fast Food Place",

    "description":
    """The fast food place is a wreck, with tables overturned and grease-stained floors slick with grime. Cash registers hang open, looted of money long ago, while trays of half-eaten meals have turned to rot. Bloodstains on the walls suggest a violent struggle, and the once-vibrant posters advertising meals are faded and torn. The fryers are cold, and the stench of decay lingers in the air.""",
}
conveniencestore = {
    "name": "Convenience Store",

    "description":
    """The convenience store is a chaotic mess, shelves emptied by frantic looters. The shattered glass door crunches underfoot, and the few remaining items lie scattered on the floor—old magazines, expired snacks, and empty water bottles. Blood splatters on the counter and walls tell the story of a grim struggle. The place feels eerie, with an unnatural quiet as if waiting for the next wave of chaos.""",
}
trainstation = {
    "name": "Train Station",

    "description":
    """The train station is abandoned, with empty platforms stretching into the darkness. The tracks are overgrown with weeds, and luggage lies discarded, as if its owners fled in a hurry. Flickering lights barely illuminate the shattered ticket booths and benches. Echoes of footsteps reverberate through the cavernous space, but no trains will ever arrive. Bloodstains and broken glass litter the ground, hinting at the violent panic that swept through.""",
}
library = {
    "name": "Library",

    "description":
    """The library is a forgotten relic, its once-organised shelves now overturned and chaotic. Books are scattered across the floor, many torn or bloodstained. The soft creak of shelves breaking under their own weight adds to the unsettling quiet. Dust coats everything, and the smell of old paper and decay fills the air. The sound of shuffling pages from deeper within suggests someone—or something—is still searching for answers in the silence.""",
}
hairdresser = {
    "name": "Hairdresser",

    "description":
    """The hairdresser's is a mess, with chairs overturned and mirrors shattered. Scissors and combs lie abandoned on the floor, and hair dye stains the walls. The smell of chemicals mixes with the stench of decay, and the faint sound of a radio playing in the background adds to the eerie atmosphere. Bloodstains on the floor hint at a violent struggle, while the empty chairs seem to wait for customers who will never return.""",
}
airport = {
    "name": "Airport",

    "description":
    """The airport is a sprawling ruin of chaos. Luggage is strewn everywhere, and the once-bustling terminals are silent, save for the distant groan of the undead. Planes sit abandoned on the runway, their passengers long gone. The security lines are in disarray, with bins and scattered belongings littering the area. Departure screens flicker with outdated flights, and the eerie silence only amplifies the sense of dread.""",
}
skyscraper = {
    "name": "Skyscraper",

    "description":
    """The skyscrapers are looking half demolished with its parts and debris splattered everywhere and hanging against its walls with bland and dull appearances.""",

    "win_requirements" : [
        {"parachute" : 1}
    ]

}
road = {
    "name": "Road",

    "description":
    """Roads are dirty and are turned upside down with waste particles, damaged cars and  scattered everywhere with major potholes planted around.""",
}
armoured_van = {
    "name": "Armoured Van",

    "description":
    """The armoured van, once a fortress on wheels, now sits abandoned with its thick, reinforced doors left slightly ajar. Bullet holes riddle its sides, and the cracked windshield is smeared with dust and grime. Inside, empty crates and torn money bags are strewn across the floor, a silent testament to the chaos and desperation that once unfolded here.""",
}
bank = {
    "name": "Bank",
    "description":
    """The bank’s lobby is eerily silent, with shattered glass doors and overturned counters. Security cameras hang lifeless from the ceiling, and vault doors are left wide open, their contents looted, while scattered bills and coins lay strewn across the marble floors, forgotten in the chaos.""",
}
arcade = {
    "name": "Arcade",
    "description":
    """The arcade, once filled with flashing lights and excited laughter, is now a graveyard of broken machines and shattered screens. Prize claw machines stand empty, their glass cracked, and old tokens litter the floor beneath games that will never be played again, their cheerful music silenced forever.""",
}
nursery = {
    "name": "Nursery",
    "description":
    """
The nursery is a heartbreaking scene, with tiny chairs tipped over and children's toys scattered across the floor. The walls, once brightly painted with cheerful murals, are peeling, and cribs sit empty, their blankets left askew as if their occupants were snatched away in a hurry.""",
}
pub = {
    "name": "Pub",
    "description":
    """The pub, once filled with laughter and clinking glasses, now stands in eerie silence, its stools overturned and tables coated in dust. Broken bottles and scattered chairs litter the floor, while the faint smell of stale alcohol mixes with the scent of decay, and shadows move unnervingly in the corners.""",
}
river = {
    "name": "River",
    "description":
    """The river, once a flowing lifeline, is now sluggish and murky, its waters dark and polluted with debris. Plastic bottles, driftwood, and other trash float along the surface, and the smell of decay hangs heavy in the air, while the distant sound of something splashing suggests the water isn’t as lifeless as it seems.""",
    "win_requirements" : [
        {"flex tape" : 20},
    ]
}
petrol_station = {
    "name": "Petrol Station",
    "description":
    """The petrol station is a wasteland of rusting pumps and broken glass, with abandoned cars still parked at the empty fuel bays. The flickering neon sign buzzes faintly, casting a pale glow on the shattered windows of the convenience store, while dried bloodstains on the tarmac hint at a chaotic, violent end.""",
    "win_requirements" : [
        {"crowbar" : 1, "screwdriver" : 100},
    ]
}
subway = {
    "name": "Subway",
    "description":
    """The subway is a labyrinth of crumbling tiles, with dim lights flickering over graffiti-covered walls. Abandoned trains sit motionless, their doors half-open, while rats scurry between the tracks, the silence occasionally broken by the distant rumble of something unseen.""",
}
rooftop_garden = {
    "name": "Rooftop Garden",
    "description":
    """Once a peaceful retreat, the rooftop garden is now overgrown and untamed, with vines creeping across cracked stone pathways. The view of the city below is eerily quiet, as skyscrapers loom in the hazy distance, their windows shattered and empty.""",
}
abandoned_hotel = {
    "name": "Abandoned Hotel",
    "description":
    """The grand chandeliers sway slightly in the musty air, casting dim light over dusty furniture and torn upholstery. The reception desk is empty, the concierge long gone, and the eerie quiet is only disturbed by the sound of distant creaking from the upper floors.""",
}
parking_garage = {
    "name": "Parking Garage",
    "description":
    """The underground parking garage is a concrete cavern filled with the stench of gasoline and decay. Cars sit abandoned in their spots, some with doors ajar and windows shattered, as a thick silence fills the air, broken by the occasional drip of water from unseen pipes.""",
}
industrial_warehouse = {
    "name": "Industrial Warehouse",
    "description":
    """Rusting machinery and toppled crates clutter the darkened warehouse, casting long shadows under the faint glow of cracked windows. The air smells of oil and dust, and the silence is punctuated by the distant clang of metal, as if something is moving in the shadows.""",
}
old_school = {
    "name": "Old School",
    "description":
    """Desks and chairs are haphazardly thrown about in classrooms, while faded chalkboards still display lessons left unfinished. Broken windows let in the cold breeze, carrying with it the faint echo of children's laughter, long gone but still haunting the empty halls.""",
}
bridge = {
    "name": "Bridge",
    "description":
    """The once-bustling bridge now stands eerily quiet, with abandoned cars scattered across it and debris littering the lanes. Below, the river flows sluggishly, filled with trash and reflecting the hollow, broken skyline.""",
}
museum = {
    "name": "Museum",
    "description":
    """The museum lobby, once pristine and polished, is now a desolate space, with cracked marble floors and broken display cases. Dust clings to ancient artefacts, and the eerie silence suggests that time itself has stopped in this forgotten place of history.""",
}
fountain = {
    "name": "Fountain",
    "description":
    """The once-beautiful fountain is now dry, its stone cracked and overgrown with moss, with coins still visible at the bottom of the empty basin. Surrounding benches sit empty, rusting under the weight of time, as the square lies deserted, overtaken by nature.""",
}
skate_park = {
    "name": "Skate Park",
    "description":
    """  Void arena with waste wooden boards scattered around and decaying benches around the arena""",
}
office_building = {
    "name": "Office Building",
    "description":
    """Area in total disarray with furnitures flipped upside down with broken items and objects""",
}


special_rooms = [park, the_hood, cinema, shopping_centre, graveyard, supermarket, hospital, pharmacy, gym, firestation, fastfoodplace, conveniencestore, trainstation, library, hairdresser, airport, skyscraper, road, armoured_van, bank, arcade, nursery, pub, river, petrol_station, subway, rooftop_garden, abandoned_hotel, parking_garage, industrial_warehouse, old_school, bridge, museum, fountain, skate_park, office_building]


generic_rooms = ['Vet', 'Telephone_box', 'Church', 'Bus_stop', 'Open-Air_Markets', 'Bike_street_stand', 'Post_office', 'Pedestrian_tunnels', 'Drive_thru_restaurant', 'Sports_bar', 'Construction_area', 'Street_supermarket', 'Abandoned_concert_aren', 'Firearms_Dealers', 'Abandoned_yacht', 'Abandoned_beach', 'Radio_station', 'Status_area', 'Cafe', 'Abandoned_car_mechanics', 'Abandoned_nightclub', 'Street_smoking_area', 'Abandoned_aquarium', 'Dock', 'Abandoned_clothing_workshop', 'Abandoned_factory', 'Dance_arena', 'Abandoned_zoo', 'Abandoned_museum', 'Ice_cream_store', 'Abandoned_gaming_store', 'Time_Capsule_Room', 'Abandoned_elderly_home', 'Kids_playground', 'Astroturf', 'Golf_course', 'Tennis_court', 'Basketball_court', 'Karting_course', 'Farm', 'Animal_shed', 'Abandoned_cinema', 'Forest', 'Canyon', 'Pond', 'Beach', 'Meadow', 'Canyon', 'Lake', 'Athletic_Track', 'Ice_Skating_Rink']
