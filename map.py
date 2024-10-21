import random
import rooms
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

    # Add in tutorial room
    tutorial_room = Room()
    tutorial_room.name = rooms.room_tutorial["name"]
    tutorial_room.description = rooms.room_tutorial["description"]
    tutorial_room.items = rooms.room_tutorial["items"]
    tutorial_room.exits = {"north"}
    map_matrix[starting_position[0]][starting_position[1]] = tutorial_room

    # Add all special rooms
    for sr in special_rooms:
        print(f"Generating {sr["name"]}.")
        room = Room()
        room.name = sr["name"]
        room.description = sr["description"]
        room.items = sr["items"]

        # Finding empty location
        while True:
            x_coord = random.randint(0, 9)
            y_coord = random.randint(0, 9)
            if map_matrix[x_coord][y_coord] is None:
                map_matrix[x_coord][y_coord] = room
                break

    # Add all generic rooms
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
    doors = set()
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

    # Ensure at least one door
    door_direct = random.choices(directions, weights=[probabilities[dir] for dir in directions])[0]
    doors.add(door_direct)

    # Optionally add more doors
    num_doors = random.randint(1, 3)
    for _ in range(num_doors):
        door_direct = random.choices(directions, weights=[probabilities[dir] for dir in directions])[0]
        doors.add(door_direct)

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