#!/usr/bin/python3
import player
from ui import *
import ui
from items import Consumable
from gameparser import *
from animator import *
from ani_sprites import *
import threading
from threading import Thread
from items import Consumable
from gameparser import *
from player import current_room_position
from map import get_room, map_matrix, door_assigner, Room, generate_map
from colorama import Fore
import subprocess
import sys
import traceback


#TODO add enemies to rooms
#TODO add combat
#TODO add items
#TODO add npc's
#TODO add morphine and allow overdose based on chance


def install_requirements():
    try:
        import colorama
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

install_requirements()

def list_of_items(items):
    new_string = ""
    for i in range(len(items)):
        if i != 0: new_string += ", "
        new_string += items[i].name
    return new_string


def print_room_items(room : Room):
    # If there are no items, no output
    if len(room.items) == 0:
        return

    write(f"There is {list_of_items(room.items)} here.")
    write()

# Prints information about the given room
def print_room(room: Room):
    write()
    write(room.name.upper())
    write()
    write(room.description)
    write()
    print_room_items(room)  # Displays items in room

    # Print exits
    if room.exits:
        write("Exits: " + ", ".join(room.exits))
    else:
        write("No exits available seems you might be stuck. What a shame ;)")

# Checks if the exit is valid in the current room
def is_valid_exit(direction):
    return direction in player.get_current_room().exits


def execute_go(direction):
    if is_valid_exit(direction):
        new_pos = player.current_room_position[:]

        # Translating direction into vector movement
        match direction:
            case "north": new_pos[1] -= 1
            case "east": new_pos[0] += 1
            case "south": new_pos[1] += 1
            case "west": new_pos[0] -= 1

        # Ensure the new room has an exit back to the previous room
        current_room = player.get_current_room()
        new_room = get_room(new_pos[0], new_pos[1])

        if new_room is None:
            write("Congratulations! You have escaped the matrix. You win!")
            close()
            sys.exit()

        if new_room is None:
            new_room = Room()
            map_matrix[new_pos[1]][new_pos[0]] = new_room

            # Generate doors for the new room
            new_room.exits = door_assigner(len(map_matrix), len(map_matrix[0]), new_pos[0], new_pos[1])

            # Ensure the new room has an exit back to the current room
            opposite_direction = {"north": "south", "south": "north", "east": "west", "west": "east"}
            new_room.exits.add(opposite_direction[direction])

        # Update the current room's exits
        current_room.exits.add(direction)

        player.previous_room_position = player.current_room_position
        player.current_room_position = new_pos

        write(f"You are going to {new_room.name}.\n")
    else:
        write("You cannot go there.\n")

def execute_consume(item_id):
    for item in player.inventory:
        if item.id == item_id:

            if type(item) != Consumable:
                break

            item.consume()
            write(f"You consumed a {item.name}.")

            player.inventory[item] -= 1
            if player.inventory[item] <= 0:
                player.inventory.pop(item)
            return
    write("You cannot consume that.")


def execute_take(item_id):
    for item in player.get_current_room().items:
        if item["id"] == item_id:

            if player.inventory_mass() + item.mass > player.max_mass:
                write("You cannot take that, your inventory is too small")
                write(f"Current Inventory Mass: {player.inventory_mass()}g")
                write(f"Mass of {item.name}: {item.mass}g")
                return
            player.get_current_room().items.pop(player.get_current_room().items.index(item))
            player.inventory.append(item)
            write(f"You picked up {item.name}.")
            return
    write("You cannot take that.")


def execute_drop(item_id):
    for item in player.inventory:
        if item.id == item_id:
            player.inventory.pop(player.inventory.index(item))
            player.get_current_room().items.append(item)
            write(f"You dropped {item.name}.")
            return
    write("You cannot drop that.")


def execute_command(command):
    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            write("Go where?\n")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            write("Take what?\n")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            write("Drop what?\n")

    elif command[0] in ["consume"]:
        if len(command) > 1:
            execute_consume(command[1])

    elif command[0] == "quit":
        write("Goodbye!\n")
        close()
        sys.exit()

    elif command[0] == "help":
        write("Commands: go [direction], take [item], drop [item], use [item], quit\n")
        write("up arrow : scroll up, down arrow : scroll down, escape key : quit\n")

    elif command[0] == "raptor": # this fucks shit up bad
        print(Fore.RED + r"""\
                ____      ________    
               ,^.__.>--"~~'_.--~_)~^.  
              _L^~   ~    (~ _.-~ \. |\     
           ,-~    __    __,^"/\_A_/ /' \ 
         _/    ,-"  "~~" __) \  ~_,^   /\  
        //    /  ,-~\ x~"  \._"-~     ~ _Y  
        Y'   Y. (__.//     /  " , "\_r ' ]   
        J-.__l_>---r{      ~    \__/ \_ _/  
       (_ (   (~  (  ~"---   _.-~ `\ / \ !   
        (_"~--^----^--------"  _.-c Y  /Y'  
         l~---v----.,______.--"  /  !_/ |   
          \.__!.____./~-.      _/  /  \ !  
           `x._\_____\__,>---"~___Y\__/Y'  
               ~     ~(_~~(_)"~___)/ /\|   
                      (_~~   ~~___)  \_t  
                      (_~~   ~~___)\_/ |  
                      (_~~   ~~___)\_/ |   
                      { ~~   ~~   }/ \ l 
                         """)


    else:
        write("This makes no sense, it appears as though the first word is not one of the designated command words..\n")


def menu(exits, room_items, inv_items): # not needed anymore
# Display menu
    #print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction): #needs to be changed to be used with the matrix in terms of navigating with the x and y coordinates
    pass

def set_scene():
    print_room(player.get_current_room())

    if len(player.get_current_room().enemies) >= 1:
        # Combat
        pass

    inv_items = player.get_inventory_items()
    if inv_items != -1:
        write("\n" + inv_items + "\n")

    write(f"Current Inventory Mass: {player.inventory_mass()}g\n")

    #write(current_room_position) what is this?
    # are these needed?
    #write(repr(player.get_current_room().exits)) 

    write("\n\n")

def write(msg = "\n"):
    ui_lock.acquire() # wait until ui can be modified
    ui.write_text(msg) # write msg to text pad
    ui_lock.release() # allow ui to be modified

def play_animation(animation): # this function creates a thread to play the given animation
    # animation has to be a valid animation from ani_sprites.py
    art_pad_args = [0,0,0,0, ui.y-1, int(ui.x/2)-1]
    try:
        anim_thread = Thread(target=run_animation_curses_pad, args=[ui.art_pad, art_pad_args, ui_lock, *animation])
        anim_thread.start()
    except Exception as e:
        write(f"Exception occured in play_animation:\n{e}\n")
        write(traceback.format_exc())
    
# global variables
user_input = ""
overflow = 0
ui_lock = threading.Lock()

# This is the entry point of our program
def main():
    global user_input
    global overflow
    global ui_lock

    # Startup Logic
    generate_map()

    #initialise curses screen
    init_screen()

    write(r"""\
╔╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╗
╠╬╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╬╣
╠╣  _______     _______.  ______     ___      .______    _______        ╠╣
╠╣ |   ____|   /       | /      |   /   \     |   _  \  |   ____|       ╠╣
╠╣ |  |__     |   (----`|  ,----'  /  ^  \    |  |_)  | |  |__          ╠╣
╠╣ |   __|     \   \    |  |      /  /_\  \   |   ___/  |   __|         ╠╣
╠╣ |  |____.----)   |   |  `----./  _____  \  |  |      |  |____        ╠╣
╠╣ |_______|_______/     \______/__/     \__\ | _|      |_______|       ╠╣
╠╣  _______ .______        ______   .___  ___.                          ╠╣
╠╣ |   ____||   _  \      /  __  \  |   \/   |                          ╠╣
╠╣ |  |__   |  |_)  |    |  |  |  | |  \  /  |                          ╠╣
╠╣ |   __|  |      /     |  |  |  | |  |\/|  |                          ╠╣
╠╣ |  |     |  |\  \----.|  `--'  | |  |  |  |                          ╠╣
╠╣ |__|     | _| `._____| \______/  |__|  |__|                          ╠╣
╠╣   ______     ___      .______       _______   __   _______  _______  ╠╣
╠╣  /      |   /   \     |   _  \     |       \ |  | |   ____||   ____| ╠╣
╠╣ |  ,----'  /  ^  \    |  |_)  |    |  .--.  ||  | |  |__   |  |__    ╠╣
╠╣ |  |      /  /_\  \   |      /     |  |  |  ||  | |   __|  |   __|   ╠╣
╠╣ |  `----./  _____  \  |  |\  \----.|  '--'  ||  | |  |     |  |      ╠╣
╠╣  \______/__/     \__\ | _| `._____||_______/ |__| |__|     |__|      ╠╣
╠╬╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╬╣
╚╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╝
""")
    # play cutscene # temporary # in the future could be replaced with intro animation or something
    #play_animation(cutscene_1)

    try:

        set_scene()

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
                write()

                normalised_user_input = normalise_input(user_input)
                execute_command(normalised_user_input)

                set_scene()

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
                ui.text_pad.refresh(ui.text_pad_pos, 0, 0, int(ui.x/2), ui.y-1, ui.x-1)
            except: #do nothing when trying to scroll past the available screen size
                pass
            ui_lock.release()

    except Exception as e: # if an error occurs return terminal to normal 
        close()
        print("exception occured\n")
        print(e)
        print()
        print(traceback.format_exc())
        return

        

    return

    # Startup Logic
    generate_map()

    # Main game loop
    while True:
        # Differentiates turns
        # Can remove once formatted
        print("=" * 40)

        if player.get_current_room() is None:
            print("Congratulations you have escaped the matrix, you are free from Cardiff and for you the game is over.")


        # Display game status (room description, inventory etc.)
        print_room(player.get_current_room())

        if len(player.get_current_room().enemies) >= 1:
            # Combat
            pass

        player.print_inventory_items()
        print(f"Current Inventory Mass: {player.inventory_mass()}g")
        print()

        print(current_room_position)
        print(player.get_current_room().exits)

        # Show the menu with possible actions and ask the player
        command = menu(player.get_current_room().exits, player.get_current_room().items, player.inventory)

        # Execute the player's command
        execute_command(command)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()

