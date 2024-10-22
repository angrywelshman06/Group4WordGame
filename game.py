#!/usr/bin/python3
import player
from ui import *
import ui
from map import Room
from items import *
from gameparser import *
from animator import *
from ani_sprites import *
import threading
from threading import Thread


def list_of_items(items):
    new_string = ""
    for i in range(len(items)):
        if i != 0: new_string += ", "
        new_string += items[i]["name"]
    return new_string


def print_room_items(room):
    # If there are no items, no output
    if len(room["items"]) == 0:
        return

    print(f"There is {list_of_items(room['items'])} here.")
    print()


def print_inventory_items(items):
    if len(items) == 0:
        return

    ui.write(f"You have {list_of_items(items)}.")
    ui.write()

def is_valid_exit(exits, chosen_exit): # used to check if the exit is valid
    return chosen_exit in exits


def execute_go(direction):
    if is_valid_exit(player.current_room["exits"], direction):
        player.current_room = move(player.current_room["exits"], direction)
        print(f"You are going to {player.current_room['name']}.")
    else:
        print("You cannot go there.")


def execute_take(item_id):
    for item in player.current_room["items"]:
        if item["id"] == item_id:

            if player.inventory_mass() + item["mass"] > player.max_mass:
                print("You cannot take that, your inventory is too small")
                print(f"Current Inventory Mass: {player.inventory_mass()}g")
                print(f"Mass of {item['name']}: {item['mass']}g")
                return
            player.current_room["items"].pop(player.current_room["items"].index(item))
            player.inventory.append(item)
            print(f"You picked up {item['name']}.")
            return
    print("You cannot take that.")


def execute_drop(item_id):
    for item in player.inventory:
        if item["id"] == item_id:
            player.inventory.pop(player.inventory.index(item))
            player.current_room["items"].append(item)
            print(f"You dropped {item['name']}.")
            return
    print("You cannot drop that.")


def execute_command(command):
    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    else:
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
# Display menu
    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction): #needs to be changed to be used with the matrix in terms of navigating with the x and y coordinates
    pass

def play_animation(animation): # this function creates a thread to play the given animation
    # animation has to be a valid animation from ani_sprites.py
    art_pad_args = [0,0,0,0, ui.y-1, int(ui.x/2)-1]
    try:
        anim_thread = Thread(target=run_animation_curses_pad, args=[ui.art_pad, art_pad_args, ui_lock, *animation])
        anim_thread.start()
    except Exception as e:
        ui.write(f"Exception occured in play_animation:\n{e}\n")
    
# global variables
user_input = ""
overflow = 0
ui_lock = threading.Lock()

# This is the entry point of our program
def main():
    #initialise curses screen
    init_screen()
    #refresh pads
    ui.art_pad.refresh(0,0,0,0, ui.y-1, int(ui.x/2)-1)
    ui.text_pad.refresh(ui.text_pad_pos, 0, 0, int(ui.x/2), ui.y-1, ui.x)
    # play cutscene # temporary # in the future could be replaced with intro animation or something
    play_animation(cutscene_1)
    
    ui.write("game start!\n")

    try:

        while True:
            cmd = ui.text_pad.getch() # wair for the user to press a key

            if cmd == curses.KEY_DOWN: # scroll down
                ui.text_pad_pos += 1
                
            elif cmd == curses.KEY_UP: # scroll up
                ui.text_pad_pos -= 1
                
            elif cmd == 27: # escape key # stop program
                ui_lock.acquire()
                close()
                return
            
            elif cmd == curses.KEY_BACKSPACE: # backspace # delete last char
                ui_lock.acquire()

                y, x = ui.text_pad.getyx() # get cursor position

                # x is 0 when at the left edge of the screen
                if x != 0: # delete char normally
                    ui.text_pad.move(y, x-1)
                    ui.text_pad.delch()
                    user_input = user_input[:-1]
                elif overflow > 0: # if line overflowed move up a line and delete
                    y_2, x_2 = ui.text_pad.getmaxyx()
                    ui.text_pad.move(y-1, x_2-1)
                    ui.text_pad.delch()
                    user_input = user_input[:-1]
                    overflow -= 1

                ui_lock.release()

            elif cmd == 10 or cmd == curses.KEY_ENTER: # enter key
                ui_lock.acquire()
                ui.write()
                ui_lock.release()

                #do something with user input or something

                user_input = ""
                overflow = 0

            else: # write a letter to text_pad
                ui_lock.acquire()

                y, x = ui.text_pad.getyx()

                ui.text_pad.addch(cmd)
                user_input += chr(cmd)
                
                y_2, x_2 = ui.text_pad.getyx()

                if y != y_2: # check if after adding char the cursor goes down a line
                    overflow += 1 # if so increment the overflow

                ui_lock.release()

            #refresh the pads 
            ui_lock.acquire()
            ui.art_pad.refresh(0,0,0,0, ui.y-1, int(ui.x/2)-1)
            try: 
                ui.text_pad.refresh(ui.text_pad_pos, 0, 0, int(ui.x/2), ui.y-1, ui.x)
            except: #do nothing when trying to scroll past the available screen size
                pass
            ui_lock.release()

    except Exception as e: # if an error occurs return terminal to normal 
        close()
        print("exception occured\n")
        print(e)
        return

        

    return

    # Main game loop
    while True:
        # Display game status (room description, inventory etc.)
        print_room(player.current_room)
        print_inventory_items(player.inventory)
        print(f"Current Inventory Mass: {player.inventory_mass()}g")
        print()

        # Show the menu with possible actions and ask the player
        command = menu(player.current_room["exits"], player.current_room["items"], player.inventory)

        # Execute the player's command
        execute_command(command)

        # Differentiates turns
        # Can remove once formatted
        print()
        print("=" * 40)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()

