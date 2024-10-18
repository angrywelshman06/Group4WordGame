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
        room.exits = door_assigner(None, None)
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
                room.exits = door_assigner(None, None)
                map_matrix[y][x] = room



def door_assigner(room_num, turns_num): #This function assigns the random door directions to each of the numbered rooms in the matrix. The number of doors is also randomly assigned but the directions available will change based on the number of turns the player has taken and their distance from the edge of the map.
    doors=[]
    num_doors = random.randint(0, 3)
    directions=["north","south","east","west"]
    for i in range(num_doors):
        door_direct = random.randint(0, 3)
        doors.append(directions[door_direct])
    return doors
        
        
        

def move(x, y, direction): #This function takes the coordinates of the player and the direction that the player wants to move in and returns the new coordinates of the player after the move.
    pass #This function will be used to move the player around the map based on the direction inputted by the user

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