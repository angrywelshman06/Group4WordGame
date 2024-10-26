import random
import enemies
import rooms
from enemies import Enemy
from rooms import special_rooms, Room, generic_rooms
from collections import deque
#import sys

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
bathroom_position = [4, 3]

def generate_map():
    used_rooms = set()

    # Add in tutorial room
    tutorial_room = Room(rooms.bedroom_tutorial, tuple(starting_position), True)
    tutorial_room.exits = {"north"}
    map_matrix[starting_position[0]][starting_position[1]] = tutorial_room
    used_rooms.add(rooms.bedroom_tutorial['name'])

    # Add bathroom room directly north of the starting position
    bathroom_room = Room(rooms.bathroom_tutorial, tuple(bathroom_position))
    bathroom_room.exits = {"south"}
    map_matrix[bathroom_position[0]][bathroom_position[1]] = bathroom_room
    used_rooms.add(rooms.bathroom_tutorial['name'])

    # Add all special rooms
    for sr in special_rooms:
        #print(f"Generating {sr['name']}.")
        max_attempts = 100  # Maximum number of attempts to find a unique room
        attempts = 0

        while attempts < max_attempts:
            x_coord = random.randint(0, 9)
            y_coord = random.randint(0, 9)
            if map_matrix[x_coord][y_coord] is None and sr['name'] not in used_rooms:
                room = Room(sr, (x_coord, y_coord), visual_in=sr["visual"])
                map_matrix[x_coord][y_coord] = room
                used_rooms.add(sr['name'])
                break
            else:
                #print(f"Attempt {attempts + 1}: Position ({x_coord}, {y_coord}) is already occupied or room name '{sr['name']}' is already used.")
                pass
            attempts += 1

        if attempts == max_attempts:
            #print(f"Failed to place room {sr['name']} after {max_attempts} attempts.")
            continue

    # Add all generic rooms
    # Add all generic rooms
    for y in range(len(map_matrix)):
        for x in range(len(map_matrix[y])):
            if map_matrix[y][x] is None:
                if generic_rooms:
                    room_name = generic_rooms.pop(0)
                    description = "This is a generic room."
                    items = []
                else:
                    room_name = f"Generic Room {x}{y}"
                    description = "This is a generic room."
                    items = []

                generic_room = {'name': room_name, 'description': description, 'items': items}
                room = Room(generic_room, (x, y))

                # enemies are generated in rooms.py, can be changed if need be
                """ if random.random() <= 0.50:
                    for num in range(random.randint(1, 3)):
                        chance = random.random()
                        level = 1
                        if chance < 0.2:
                            level = 3
                        elif chance < 0.5:
                            level = 2

                        room.enemies[f"enemy{num}"] = Enemy(enemies.zombie, level=level) """

                map_matrix[y][x] = room
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

def get_adjacent_room(room, direction) -> Room:
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

def connect_to_nearest_visited_room(room, visited):#This function connects the room to the nearest visited room
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

def dist_from_edge(x, y):
    try:
        if y < 0 or y >= len(map_matrix) or x < 0 or x >= len(map_matrix[y]):
            raise IndexError("Coordinates are out of bounds")

        return {
            "north": y,
            "south": len(map_matrix) - 1 - y,
            "west": x,
            "east": len(map_matrix[y]) - 1 - x,
        }
    except IndexError:
        pass
        #print("Congratulations! You have escaped the matrix. You win!")
        #sys.exit()

# Gets the room based off its matrix position coordinates
def get_room(x, y) -> Room:
    distances = dist_from_edge(x, y)
    for direction in distances:
        if distances[direction] < 0: return None # No room (escaped)
    return map_matrix[y][x]