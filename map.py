import random
import rooms
from rooms import special_rooms, Room, generic_rooms
from collections import deque
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
def generate_map():
    # Add in tutorial room
    tutorial_room = Room(rooms.room_tutorial, tuple(starting_position))
    tutorial_room.exits = {"north"}
    map_matrix[starting_position[0]][starting_position[1]] = tutorial_room

    # Add all special rooms
    for sr in special_rooms:
        print(f"Generating {sr['name']}.")
        while True:
            x_coord = random.randint(0, 9)
            y_coord = random.randint(0, 9)
            if map_matrix[x_coord][y_coord] is None:
                room = Room(sr, (x_coord, y_coord))
                map_matrix[x_coord][y_coord] = room
                break

    # Add all generic rooms
    for y in range(len(map_matrix)):
        for x in range(len(map_matrix[y])):
            if map_matrix[y][x] is None:
                random_room = generic_rooms[random.randint(0, len(generic_rooms) - 1)]
                room = Room(random_room, (x, y))
                map_matrix[y][x] = room

    # Generate doors for all rooms
    for y in range(len(map_matrix)):
        for x in range(len(map_matrix[y])):
            room = map_matrix[y][x]
            room.exits = door_assigner(len(map_matrix), len(map_matrix[0]), x, y)

    # Ensure the map is a connected graph
    ensure_connected_graph()

def ensure_connected_graph():
    start_room = get_room(starting_position[0], starting_position[1])
    visited = set()
    queue = deque([start_room])

    while queue:
        current_room = queue.popleft()
        if current_room in visited:
            continue
        visited.add(current_room)

        for direction in current_room.exits:
            next_room = get_adjacent_room(current_room, direction)
            if next_room and next_room not in visited:
                queue.append(next_room)

    for room in all_rooms():
        if room not in visited:
            connect_to_nearest_visited_room(room, visited)

def get_adjacent_room(room, direction):
    x, y = room.position
    if direction == "north":
        y -= 1
    elif direction == "south":
        y += 1
    elif direction == "east":
        x += 1
    elif direction == "west":
        x -= 1

    if 0 <= x < len(map_matrix[0]) and 0 <= y < len(map_matrix):
        return map_matrix[y][x]
    return None

def connect_to_nearest_visited_room(room, visited):
    x, y = room.position
    for direction in ["north", "south", "east", "west"]:
        adjacent_room = get_adjacent_room(room, direction)
        if adjacent_room and adjacent_room in visited:
            room.exits.add(direction)
            opposite_direction = {"north": "south", "south": "north", "east": "west", "west": "east"}
            adjacent_room.exits.add(opposite_direction[direction])
            break

def all_rooms():
    rooms_list = []
    for row in map_matrix:
        for room in row:
            if room is not None:
                rooms_list.append(room)
    return rooms_list


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