from items import *
global starting_position
map_matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#This is the matrix which will be filled with the random unique numbers that are going to be used to place the rooms on the map



def door_assigner(room_num): #This function assigns the random door directions to each of the numbered doors stored in the matrix.
    pass
def where_am_i(x, y): #This function takes the coordinates of the player and returns the room that the player is in and calculates how many positions from the edge the player is using north, south, east and west.
    return map_matrix[x][y]
def move(x, y, direction): #This function takes the coordinates of the player and the direction that the player wants to move in and returns the new coordinates of the player after the move.
    pass




