import random
from collections import deque
import npcs
import items

map_matrix = [[None for x in range(10)] for y in range(10)]

starting_position = [4, 4]
bathroom_position = [4, 3]
kitchen_position = [4, 5]

def generate_map():
    from rooms import Room, special_rooms, generic_rooms
    import rooms

    while True:
        used_npc_positions = []

        for npc in npcs.randomly_placed_npcs:
            bounds = npcs.randomly_placed_npcs[npc]
            max_attempts = 7
            attempts = 0

            while attempts < max_attempts:
                unique_turn = random.randint(bounds[0], bounds[1])
                if unique_turn not in used_npc_positions:
                    used_npc_positions.append(unique_turn)
                    npcs.randomly_placed_npcs[npc] = unique_turn
                    break
                attempts += 1

            if attempts == max_attempts:
                for turn in range(bounds[1], bounds[1] + 10):
                    if turn not in used_npc_positions:
                        used_npc_positions.append(turn)
                        npcs.randomly_placed_npcs[npc] = turn
                        break

        used_rooms = set()

        tutorial_room = Room(rooms.bedroom_tutorial, tuple(starting_position), True, visual_in=rooms.bedroom_tutorial["visual"])
        tutorial_room.exits = {"north"}
        map_matrix[starting_position[1]][starting_position[0]] = tutorial_room
        used_rooms.add(rooms.bedroom_tutorial['name'])

        bathroom_room = Room(rooms.bathroom_tutorial, tuple(bathroom_position), visual_in=rooms.bathroom_tutorial["visual"])
        bathroom_room.exits = {"north", "south", "east", "west"}
        map_matrix[bathroom_position[1]][bathroom_position[0]] = bathroom_room
        used_rooms.add(rooms.bathroom_tutorial['name'])

        kitchen_room = Room(rooms.kitchen_tutorial, tuple(kitchen_position), visual_in=rooms.kitchen_tutorial["visual"])
        kitchen_room.exits = {"north", "south", "east", "west"}
        map_matrix[kitchen_position[1]][kitchen_position[0]] = kitchen_room
        used_rooms.add(rooms.kitchen_tutorial['name'])

        for sr in special_rooms:
            max_attempts = 100
            attempts = 0

            while attempts < max_attempts:
                x_coord = random.randint(0, 9)
                y_coord = random.randint(0, 9)
                if map_matrix[y_coord][x_coord] is None and sr['name'] not in used_rooms:
                    room = Room(sr, (y_coord, x_coord), visual_in=sr["visual"])
                    map_matrix[y_coord][x_coord] = room
                    generate_loot(x_coord, y_coord)
                    used_rooms.add(sr['name'])
                    break
                attempts += 1

        for y in range(len(map_matrix)):
            for x in range(len(map_matrix[y])):
                if map_matrix[y][x] is None:
                    if generic_rooms:
                        room_name = random.choice(generic_rooms)
                        description = f"This is a {room_name}."
                        items = []
                    else:
                        room_name = f"Generic Room {x}{y}"
                        description = "This is a generic room."
                        items = []

                    generic_room = {'name': room_name, 'description': description, 'items': items}
                    room = Room(generic_room, (x, y))
                    map_matrix[y][x] = room
                    generate_loot(x, y)

        ensure_connected_graph()
        if find_path_to_exit():
            break

def generate_loot(x_coord, y_coord):
    room = map_matrix[y_coord][x_coord]

    if len(room.items) != 0:
        return

    for item_dict in items.item_list:
        if random.random() <= item_dict["spawn_chance"]:
            amount = random.randint(item_dict["spawn_quantity"][0], item_dict["spawn_quantity"][1])
            if item_dict["id"] not in room.items:
                room.items[item_dict["id"]] = amount
            else:
                room.items[item_dict["id"]] += amount

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
            print(f"Connected {room.name} at ({x}, {y}) to {adjacent_room.name} at {adjacent_room.position} via {direction}")
            break

def all_rooms():
    rooms_list = []
    for row in map_matrix:
        for room in row:
            if room is not None:
                rooms_list.append(room)
    return rooms_list

def dist_from_start(x, y):
    starting = starting_position
    distance = abs(x - starting[0]) + abs(y - starting[1])
    return distance

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

def get_room(x, y):
    distances = dist_from_edge(x, y)
    try:
        for direction in distances:
            if distances[direction] < 0: return None
    except Exception as e:
        return None
    return map_matrix[y][x]

def find_path_to_exit():
    start_room = get_room(starting_position[0], starting_position[1])
    queue = deque([(start_room, [])])
    visited = set()

    directions = ["north", "south", "east", "west"]
    opposite_direction = {"north": "south", "south": "north", "east": "west", "west": "east"}

    while queue:
        current_room, path = queue.popleft()
        if current_room in visited:
            continue
        visited.add(current_room)

        for direction in current_room.exits:
            next_room = get_adjacent_room(current_room, direction)
            if next_room and next_room not in visited:
                new_path = path + [direction]
                if is_exit(next_room):
                    return new_path
                queue.append((next_room, new_path))

    return None

def is_exit(room):
    x, y = room.position
    is_exit_room = x == 0 or x == len(map_matrix[0]) - 1 or y == 0 or y == len(map_matrix) - 1
    return is_exit_room

def main():
    generate_map()
    path_to_exit = find_path_to_exit()
    if path_to_exit:
        print("Path to exit:", " -> ".join(path_to_exit))
    else:
        print("No exit found")

if __name__ == "__main__":
    main()