import random
from rooms import special_rooms, Room



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
        print(f"Generating {sr['name']}.")
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







def door_assigner(room_num): #This function assigns the random door directions to each of the numbered doors stored in the matrix.
    pass
def where_am_i(x, y): #This function takes the coordinates of the player and returns the room that the player is in and calculates how many positions from the edge the player is using north, south, east and west.
    return map_matrix[x][y]
def move(x, y, direction): #This function takes the coordinates of the player and the direction that the player wants to move in and returns the new coordinates of the player after the move.
    pass #This function will be used to move the player around the map based on the direction inputted by the user
def dist_from_start(x, y): #This function takes the coordinates of the player and returns the distance from the starting position of the player
    starting = starting_position
    distance = abs(x - starting[0]) + abs(y - starting[1])
    return distance


#generate_map()
#print(map_matrix)

