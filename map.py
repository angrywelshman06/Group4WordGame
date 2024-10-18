import random
from rooms import special_rooms, Room, generic_rooms

map_matrix = [[None for x in range(10)] for y in range(10)]

'''
This is the structure of map_matrix, 10 by 10, 0s representing randomly placed
room objects, and the 1 being the starting point (and tutorial room)

             [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
              
'''

#This is the starting position of the player, as shown above
starting_position = [4, 4]

# Main function to generate the rooms in the map_matrix
def generate_map():
    for sr in special_rooms:
        print(f"Generating {sr["name"]}.")
        room = Room()
        room.name = sr["name"]
        room.description = sr["description"]
        room.items = sr["items"]
        # Add exit dictionary (or however we are storing it) here

        while True:
            x_coord = random.randint(0, 9)
            y_coord = random.randint(0, 9)
            if type(map_matrix[x_coord][y_coord]) != type(Room()):
                map_matrix[x_coord][y_coord] = room
                break

    for y in range(len(map_matrix)):
        for x in range(len(map_matrix[y])):
            if map_matrix[y][x] is None:
                random_room = generic_rooms[random.randint(0, len(generic_rooms) - 1)]
                room = Room()
                room.name = random_room["name"]
                room.description = random_room["description"]
                room.items = random_room["items"]
                map_matrix[y][x] = room


def door_assigner(room_num, turns_num, x, y):
    doors = {}
    directions = ["north", "south", "east", "west"]
    distances = dist_from_edge(x, y)

    # Calculate weights based on distances and number of turns
    weights = {
        "north": distances["north"] + turns_num,
        "south": distances["south"] + turns_num,
        "east": distances["east"] + turns_num,
        "west": distances["west"] + turns_num
    }

    # Normalize weights to create probabilities
    total_weight = sum(weights.values())
    probabilities = {direction: weight / total_weight for direction, weight in weights.items()}

    num_doors = random.randint(1, 3)  # Ensure at least one door
    for _ in range(num_doors):
        door_direct = random.choices(directions, weights=[probabilities[dir] for dir in directions])[0]
        doors[door_direct] = None  # Initialize with None, will be updated when the room is created

    return doors
        

def dist_from_start(x, y): #This function takes the coordinates of the player and returns the distance from the starting position of the player
    starting = starting_position
    distance = abs(x - starting[0]) + abs(y - starting[1])
    return distance

# Returns a dictionary of the distances for each edge from the player
def dist_from_edge(x, y) -> {}:
    return {
        "north" : y,
        "east" : len(map_matrix[y]) - 1 - x,
        "south" : len(map_matrix) - 1 - y,
        "west" : x
    }

# Gets the room based off its matrix position coordinates
def get_room(x, y) -> Room:
    distances = dist_from_edge(x, y)
    for direction in distances:
        if distances[direction] < 0: return None # No room (escaped)
    return map_matrix[y][x]