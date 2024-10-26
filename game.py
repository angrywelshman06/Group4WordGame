#!/usr/bin/python3
from colorama import Fore

# ui/animation
from ui import *
import ui
from animator import *
from ani_sprites import *

# game systems
import player
import random
from items import Consumable, Weapon, Item, get_item_dict_from_list
import items
from gameparser import *
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


def print_room_items(room: Room): #  TODO fix this innit
    # If there are no items, no output
    if len(room.items) == 0:
        return

    item_list = ""
    count = 0
    for item_id in room.items.keys():

        item_dict = get_item_dict_from_list(item_id)
        if item_dict is None:
            write(f"ERROR: {item_id} HAS NOT BEEN INITIALISED\n")
            continue

        #item = room.items.get(item_dict)

        if count == len(room.items) - 1 and len(room.items) > 1:
            item_list += " and "
        elif count != 0:
            item_list += ", "
        item_list += f"{room.items[item_dict["id"]]} {item_dict["name"]}"
        if room.items[item_id] > 1: item_list += "s"
        count += 1

    write(f"There is {item_list} here.\n")

    write()


# Prints information about the given room
def print_room(room: Room):
    write()
    write(room.name.upper())
    write()
    write(room.description)
    write()
    print_room_items(room)  # Displays items in room

    #if len(room.enemies) == 0:

    # Print exits
    if room.exits:
        write("Exits: " + ", ".join(room.exits))
    else:
        write("No exits available seems you might be stuck. What a shame ;)\n")

    


# Checks if the exit is valid in the current room
def is_valid_exit(direction):
    return direction in player.get_current_room().exits


def execute_go(direction):
    if is_valid_exit(direction):
        new_pos = player.current_room_position[:]

        # Translating direction into vector movement
        match direction:
            case "north":
                new_pos[1] -= 1
            case "east":
                new_pos[0] += 1
            case "south":
                new_pos[1] += 1
            case "west":
                new_pos[0] -= 1

        # Ensure the new room has an exit back to the previous room
        current_room = player.get_current_room()
        new_room = get_room(new_pos[0], new_pos[1])

        if new_room is None:
            write("Congratulations! You have escaped the matrix. You win!\n")
            close()
            #sys.exit()

        # Ensure the new room has an exit back to the current room
        opposite_direction = {"north": "south", "south": "north", "east": "west", "west": "east"}
        new_room.exits.add(opposite_direction[direction])

        player.previous_room_position = player.current_room_position
        player.current_room_position = new_pos

        write(f"You are going to {new_room.name}.\n")

        try:
            draw_stillshot(new_room.visual) # draw room visual
        except:
            draw_stillshot(room_placeholder) # room has no visuals to print, print generic visual

        global in_danger
        if len(new_room.enemies) >= 1: # if there are enemies in the room put the player in danger
            in_danger = True 
            write(f"\nYou see near by {len(new_room.enemies)} zombies! You can either FIGHT or FLEE.\n", curses.color_pair(24))
            
    else:
        write("You cannot go there.\n")

def execute_consume(item_id): # consumes item in battle and regens health
    for item in player.inventory:
        if item.id == item_id:

            if type(item) != Consumable:
                break

            item.consume()
            write(f"You consumed a {item.name}.\n")

            player.inventory[item] -= 1
            if player.inventory[item] <= 0:
                player.inventory.pop(item)
            return
    write("You cannot consume that.\n")


def execute_take(item_id, amount=1):

    for item_dict_id in player.get_current_room().items.keys():
        if item_dict_id == item_id:

            item = items.dict_to_item(get_item_dict_from_list(item_dict_id))

            if player.get_current_room().items[item_id] < amount:
                write(f"There are not {amount} many {item.name}s in the room.")
                return


            if player.get_current_room().items[item_id] > amount:
                player.get_current_room().items[item_id] -= amount
            else:
                player.get_current_room().items.pop(item_id)
                #player.get_current_room().items.


            found = False
            for item in player.inventory.keys():
                if item.id == item_id:
                    player.inventory[item] += amount
                    found = True
                    break

            if not found:
                player.inventory[item] = amount

            write(f"You picked up {item.name}.\n")
            return
    write("You cannot take that.\n")


def execute_drop(item_id, amount=1):
    for item in player.inventory.keys():
        if item.id == item_id:

            if player.inventory[item] < amount:
                write(f"You do not have {amount} {item.name}s.\n")
                return

            if player.inventory[item] > amount:
                player.inventory[item] -= amount
            else:
                player.inventory.pop(item)

            if item.id in player.get_current_room().items:
                player.get_current_room().items[item.id] += amount
            else:
                player.get_current_room().items[item.id] = amount

            write(f"You dropped {item.name}.\n")
            return
    write("You cannot drop that.\n")


def execute_command(command): # parse what needs to be executed based on command
    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            write("Go where?\n")

    elif command[0] == "take":
        if len(command) > 1:
            if len(command) >= 3 and str(command[2]).isdigit():
                execute_take(command[1], amount=int(command[2]));
                return
            execute_take(command[1])
        else:
            write("Take what?\n")

    elif command[0] == "drop":
        if len(command) > 1:
            if len(command) >= 3 and str(command[2]).isdigit():
                execute_drop(command[1], amount=int(command[2])); return
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

    elif command[0] == "raptor":
        write("""\
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
                         """, curses.A_BOLD)


    else:
        write("This makes no sense, it appears as though the first word is not one of the designated command words..\nTry asking for 'HELP'\n", curses.A_BOLD)

def resolve_danger(command): # when entering a room with enemies the player can choose to flee to the last room or to engage enemies
    # 0 - combat unresolved # 1 - out of combat # 2 - in combat
    if len(command) == 0:
        return 0

    if command[0] == "fight":
        write("You ready yourself and approach the enemies\n")
        return 2

    elif command[0] == "flee" or command[0] == "escape":
        player.current_room_position = player.previous_room_position
        write("It's not worth the risk, you head back before you are seen\n")
        return 1

    elif command[0] == "help" or command[0] == "what":
        write("You have to choose FIGHT or to FLEE\n")
        return 0

    else:
        write("This makes no sense, it appears as though the first word is not one of the designated command words..\n")
        write("You have to choose to FIGHT or to FLEE\n")
        return 0

def execute_attack(enemy_id, enemy, weapon): # attaks an enemy
    if random.random() < weapon.crit_chance:
        damage = weapon.damage * weapon.crit_mult
        write(f"You hit the {enemy.name} for critical damage and dealt {damage} damage.\n")
        enemy.health -= damage
    else:
        damage = weapon.damage
        write(f"You hit the {enemy.name} and dealt {damage} damage.\n")
        enemy.health -= damage

    if enemy.health > 0:
        write(f"The {enemy.name} now has {enemy.health} health.\n")
    else:
        #player.get_current_room().enemies.pop(enemy_id)
        player.get_current_room().enemies.remove(enemy_id)
        write(f"The {enemy.name} has been killed!\n")

def execute_consume(item_id): # consumes an item
    for item in player.inventory:
        if item.id == item_id:
            if type(item) != Consumable:
                write("This item isn't consumable\n")
                return

            item.consume()
            write(f"You consumed a {item.name} and regain {item.healing} health!\n", curses.color_pair(7))
            player.inventory[item] -= 1
            if player.inventory[item] <= 0:
                player.inventory.pop(item)
            return
        
    write("No such item in inventory\n")
    return

def execute_combat(command): # returns if player is still in combat # executes combat

    if len(command) == 0:
        write("no command\n")
        return True
    
    #write(command)
    #write()

    # player turn

    write("executing combat\n")
    
    if command[0] in ["flee", "escape", "run"]:
        write("Attempting to flee\n")
        if random.random() < 0.7:
            # TODO escape to last room
            player.current_room_position = player.previous_room_position
            write("You manage to escape the battle.\n")
            return False
        else:
            write("You failed to escape.\n")

    elif command[0] == "attack":
                
        # Checking correct number of prompts
        if len(command) < 3:
            write("\nInvalid command.\n To attack write attack <target> <weapon>\n")
            write("Example: fight first bat, which will attack the first enemy with the bat\n")
            write("Or write HELP for the help menu\n")
            return True

        target_index = -1
        enemy_count = len(player.get_current_room().enemies)

        # check target validity
        if command[1] in ["1", "first"]:
            target_index = 0
        elif command[1] in ["2", "second"]:
            target_index = 1
            if enemy_count < 2:
                write("\nThere is only one enemy\n")
                return True
        elif command[1] in ["3", "third"]:
            target_index = 2
            if enemy_count < 3:
                write("\nThere are only 2 enemies\n")
                return True
        else:
            write("\nInvalid target, to choose an enemy write 'fisrt' or '1' to select the first enemy, same for every other enemy\n")
            return True
            
        for item in player.inventory:
            if item.id == command[2] or item.name == command[2]:
                if type(item) == items.Weapon:
                    execute_attack(command[1], player.get_current_room().enemies[target_index], item)
                elif type(item) == items.Gun:
                    execute_attack(command[1], player.get_current_room().enemies[target_index], item)
                    item.ammo -= 1
                else:
                    write("This item is not a weapon!\n")
                    return True
    
    elif command[0] in ["use", "consume"]:
        execute_consume(command[1])

    else:
        write("Thats not a valid action\n You can FIGHT, FLEE or USE\n")
        return True
        
    # enemy turn

    if len(player.get_current_room().enemies) == 0:
        write("You won the battle!\n", curses.color_pair(7))
        return False

    enemy = random.choice(list(player.get_current_room().enemies)) # choose random enemy to attack
    write(f"The {enemy.name} attacked you!\n", curses.color_pair(25))
    if random.random() < enemy.crit_chance:
        damage = enemy.damage * enemy.crit_multiplier
        write(f"It hit you for critical damage and dealt {damage} damage.\n", curses.color_pair(24))
        player.health -= damage
    else:
        damage = enemy.damage
        write(f"It dealt {damage} damage.\n")
        player.health -= damage

    if player.health > 0:
        write(f"You are now on {player.health} health.\n")
    else:
        write("You died!\n",curses.color_pair(24))
        play_animation(cutscene_death_1, True)
        close()
        pass

    write()
    return True


def set_scene_combat(): # gives the player info on how the battle is progressing
    enemies = player.get_current_room().enemies

    write(f"There are {len(enemies)} enemies left. You see a ")
    for enemy in enemies:
        write(f"{enemy.name}, ")
    
    write(f"\nYou have {player.health} health left.\n")
    write("ATTACK <enemy> <weapon>\tor\t")
    write("CONSUME <item>\tor\t")
    write("FLEE\n\n")

    
def set_scene(): # gives the player info on the current room and thier charecter
    print_room(player.get_current_room())

    inv_items = player.get_inventory_items()
    if inv_items != -1:
        write("\n" + inv_items + "\n")

    write(f"Current Inventory Mass: {player.inventory_mass()}g\n")

    write("\n")

def write(msg = "\n", arg=None): # writes text to text pad
    ui_lock.acquire() # wait until ui can be modified
    if arg == None:
        ui.text_pad.addstr(msg) # add string to text pad
    else:
        try:
            ui.text_pad.addstr(msg, arg) # add string with given args
        except:
            ui.text_pad.addstr("\ninvalid curses attribute passed\n")

    #refresh text pad
    try: 
        ui.text_pad.refresh(ui.text_pad_pos, 0, 0, int(ui.x/2), ui.y-1, ui.x-1) # could cause error when trying to refresh beyound pad extent (because of scrolling too far down)
    except:
        ui.text_pad.refresh(ui.text_pad_pos-1, 0, 0, int(ui.x/2), ui.y-1, ui.x-1) # refresh without going out of pad extent
    
    ui_lock.release() # allow ui to be modified

def play_animation(animation, hold=False): # this function creates a thread to play the given animation
    # animation has to be a valid animation from ani_sprites.py
    art_pad_args = [0,0,0,0, ui.y-1, int(ui.x/2)-1]
    try:
        anim_thread = Thread(target=run_animation_curses_pad, args=[ui.art_pad, art_pad_args, ui_lock, *animation])
        anim_thread.start()
        if hold:
            anim_thread.join()
    except Exception as e:
        write(f"Exception occured in play_animation:\n{e}\n")
        write(traceback.format_exc())

def draw_stillshot(stillshot): # prints a still shot to the art pad

    art_pad_args = [0,0,0,0, ui.y-1, int(ui.x/2)-1]
    try:
        ui.art_pad.clear()
        print_stillshot_curses_pad(ui.art_pad, art_pad_args, ui_lock, *stillshot)
    except Exception as e:
        write(f"Exception occured in draw_stillshot\n{e}\n")
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
    global in_danger

    try:

        # Startup Logic
        generate_map()
        
        #initialise curses screen
        init_screen()

        # play intro animations
        play_animation(intro_1, True) # hold main thread unntil this animation stops playing
        play_animation(intro_2)

    except Exception as e:
        close()
        print(f"Exception '{e}' occured\n")
        print(traceback.format_exc())

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
""", curses.color_pair(24))
    
    write("Lorem ipsum (should be intro text)", curses.color_pair(25))
    
    try:

        set_scene()

        #main game loop
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
                #write("enter pressed\n\n")
                #write(f"{user_input} : uinp\n")

                normalised_user_input = normalise_input(user_input)

                #write(f"{normalised_user_input} : normal inp\ncombat:{in_combat}\n")

                if in_combat == True:
                    #write("execute combat!\n")
                    in_combat = execute_combat(normalised_user_input)
                    set_scene_combat()
                elif in_danger == True:
                    #write("resolving danger\n")
                    resolution = resolve_danger(normalised_user_input)
                    if resolution == 0: # danger unresolved
                       in_danger = True
                    elif resolution == 1: # escaped from danger / fled back to last room
                        in_danger = False
                    elif resolution == 2: # combat started
                        in_danger = False
                        in_combat = True

                    #write(f"in danger:{in_danger}|||in combnat:{in_combat}\n")

                    
                elif in_combat == False and in_danger == False:
                    #write("executing normal command\n")
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
