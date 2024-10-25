#!/usr/bin/python3
from colorama import Fore

# ui/animation
from ui import *
import ui
from animator import *
from ani_sprites import *

# game systems
import player
from items import Consumable, Weapon, Item
import items
from gameparser import *
from player import current_room_position
from map import get_room, map_matrix, door_assigner, Room, generate_map
import combat

# system shit innit
import threading
from threading import Thread
import subprocess
import sys
import traceback
import random


#TODO add enemies to rooms
#TODO add combat
#from combat import *
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

        global in_danger
        if len(new_room.enemies) >= 1:
            in_danger = True
            write(f"You see near by {len(new_room.enemies)} zombies! You can either FIGHT or FLEE.\n")
            
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

def resolve_danger(command):
    if len(command) == 0:
        return
    
    global in_danger
    global in_combat

    if command[0] == "fight":
        in_danger = False
        in_combat = True
        write("You ready yourself and approach the enemies\n")

    elif command[0] == "flee" or command[0] == "escape":
        in_danger = False
        # TODO go back to previous room
        write("It's not worth the risk, you head back before you are seen\n")

    elif command[0] == "help" or command[0] == "what":
        write("You have to choose FIGHT or to FLEE\n")

    else:
        write("This makes no sense, it appears as though the first word is not one of the designated command words..\n")

def execute_attack(enemy_id, enemy, weapon):
    if random.random() < weapon.crit_chance:
        write(f"You hit the {enemy.name} for critical damage and dealt {weapon.get_damage(True)} damage.\n")
        enemy.health -= weapon.get_damage(True)
    else:
        write(f"You hit the {enemy.name} and dealt {weapon.get_damage(False)} damage.\n")
        enemy.health -= weapon.get_damage(False)

    if enemy.health > 0:
        write(f"The {enemy.name} now has {enemy.health} health.\n")
    else:
        player.get_current_room().enemies.pop(enemy_id)
        write(f"The {enemy.name} has been killed!\n")

def execute_consume(item_id):
    for item in player.inventory:
        if item.id == item_id:
            if type(item) != Consumable:
                break

            item.consume()
            write(f"You consumed a {item.name}.\n")
            player.inventory[item] -= 1
            if player.inventory[item] <= 0:
                player.inventory.pop(item)
            return True
        
    write("You cannot consume that.\n")
    return False

def execute_combat(command):
    if len(command) == 0:
        return
    
    # player turn
    
    if command[0] == "flee":
        if random.random() < 0.7:
            # TODO escape to last room
            write("You manage to escape the battle.\n")
            global in_combat
            in_combat = False
        else:
            write("You failed to escape.\n")
            return

    elif command[0] == "attack":
                
        # Checking correct number of prompts
        if len(command) < 3:
            write("Invalid command. Type HELP for command prompts\n")
            return

        # Checking enemy is valid
        if command[1] not in player.get_current_room().enemies:
            write(command[1] + " is an invalid enemy!\n")
            return
        
        for item in player.inventory:
            if item.id == command[2]:
                if type(item) == items.Weapon:
                    execute_attack(command[1], player.get_current_room().enemies[command[1]], item)
                    return
                else:
                    write("This item is not a weapon!\n")
                    return
    
    elif command[0] in ["use", "consume"]:
        if execute_consume(command[1]):
            return
        else:
            # bad??
            return
        
    # enemy turn
    enemy = random.choice(list(player.get_current_room().enemies.values()))
    write(f"The {enemy.name} attacked you!")
    if random.random() < enemy.crit_chance:
        write(f"It hit you for critical damage and dealt {enemy.get_damage(True)} damage.")
        player.health -= enemy.get_damage(True)
    else:
        write(f"It dealt {enemy.get_damage(False)} damage.")
        player.health -= enemy.get_damage(False)

    if player.health > 0:
        write(f"You are now on {player.health} health.")
    else:
        write("You died!\n")
        close()
        pass



def set_scene_combat():
    write("kill")
    
def set_scene():
    print_room(player.get_current_room())

    inv_items = player.get_inventory_items()
    if inv_items != -1:
        write("\n" + inv_items + "\n")

    write(f"Current Inventory Mass: {player.inventory_mass()}g\n")

    write("\n")

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
in_danger = False
in_combat = False

# This is the entry point of our program
def main():
    global user_input
    global overflow
    global ui_lock
    global in_combat

    # Startup Logic
    generate_map()

    #initialise curses screen
    init_screen()

    # write title screen
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

    #refresh pads
    ui.art_pad.refresh(0,0,0,0, ui.y-1, int(ui.x/2)-1)
    ui.text_pad.refresh(ui.text_pad_pos, 0, 0, int(ui.x/2), ui.y-1, ui.x-1)
    # play cutscene # temporary # in the future could be replaced with intro animation or something
    play_animation(cutscene_1)

    #zombies = [("zombie", 2),("zombie", 5), ("zombie", 1),("zombie", 1)] #this list will be what's returned from the random battle generator
    #fight = initiate_combat(ui.art_pad,zombies)
    #run_animation_curses(*fight.animation)
    #ui.art_pad.getch()
    
    try:
        ###### LOOP CAN BE WHATEVER, JUST FOR TESTING PURPOSES THIS ONE
        # ill get to this soon ish
        """ for i in range(2):
            print_stillshot_curses(*fight.stillstate) ## unpacking tuple with the necessary arguments
            display_win.getch()
            user_input = "attack 1" # REPLACE THIS WITH WHATEVER PARSED USER INPUT. In user_update, the only valid inputs so far are "escape" and "attack_1", "attack_2"... etc. This should check fight.creatures_dict to see if enemy exists before executing the function.
            fight.user_update(user_input)
            run_animation_curses(*fight.animation) # runs the stored animation
            print_stillshot_curses(*fight.stillstate)
            display_win.getch()
            fight.zombie_update() # handles which zombie attacks the player
            run_animation_curses(*fight.animation) """

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
                if in_danger:
                    resolve_danger(normalised_user_input)
                elif in_combat:
                    execute_combat(normalised_user_input)
                else:
                    execute_command(normalised_user_input)

                set_scene() # maybe dont run this everytime?

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
        print()
        print(traceback.format_exc())
        return


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()

