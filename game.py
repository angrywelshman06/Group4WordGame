#!/usr/bin/python3
import enemies
import items
import npcs
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
from map import get_room, Room, generate_map
import combat

# system shit innit
import threading
from threading import Thread, Lock, Event
import subprocess
import sys
import traceback
import random



def install_requirements():
    try:
        import colorama
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])



install_requirements()


def print_room_items(room: Room): #  TODO fix this innit
    # If there are no items, no output
    if len(room.items) == 0:
        #write("\nroom supposedlyt has no tiems!!\n")
        return
    
    #write("\nprint room items called!\n")

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
        item_list += f"{room.items[item_dict['id']]} {item_dict['name']}"
        if room.items[item_id] > 1: item_list += "s"
        count += 1

    write(f"\nThere is {item_list} here.\n", curses.color_pair(18))

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
            write("CONGRATULATIONS YOU’VE ESCAPED CARDIFF! By going beyond the surrounding wall you have reached the safe haven, a span of gorgeous green land carefully tendered too by the remaining few. Although danger still remains within the city, signs of rebuilding life are slowly developing once again around you\n")
            close()
            #sys.exit()

        # Ensure the new room has an exit back to the current room
        opposite_direction = {"north": "south", "south": "north", "east": "west", "west": "east"}
        new_room.exits.add(opposite_direction[direction])

        player.previous_room_position = player.current_room_position
        player.current_room_position = new_pos

        if not player.get_current_room().visited:
            player.get_current_room().visited = True
            player.unique_rooms_visited += 1

        for npc in npcs.randomly_placed_npcs:
            if npcs.randomly_placed_npcs[npc] == player.unique_rooms_visited:
                player.get_current_room().npcs.append(npc)

        print(f"You are going to {new_room.name}.")
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

def execute_talk(npc_id):
    for npc in player.get_current_room().npcs:
        if npc.id == npc_id:
            npc.talk()
            return
    print("You cannot talk to this NPC.")

def execute_talk(npc_id):
    for npc in player.get_current_room().npcs:
        if npc.id == npc_id:
            npc.talk()
            return
    print("You cannot talk to this NPC.")


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
        else:
            print("Consume what>")

    elif command[0] in ["talk"]:
        if len(command) > 1:
            execute_talk(command[1])
        else:
            print("Talk to who?")

    elif command[0] == "quit":
        write("Goodbye!\n")
        close()
        sys.exit()

    elif command[0] == "help":
        write("Commands: go [direction], take [item], drop [item], use [item], quit\n")
        write("up arrow : scroll up, down arrow : scroll down, escape key : quit\n")

    elif command[0] == "raptor":
        write("""
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
        try:
            draw_stillshot(player.get_current_room().visual) # draw room visual
        except:
            draw_stillshot(room_placeholder) # room has no visuals to print, print generic visual
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
        write(f"You hit the {enemy.name} for critical damage and dealt {damage} damage.\n", curses.color_pair(24))
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
        return True
    
    # player turn
    
    if command[0] in ["flee", "escape", "run"]:
        write("Attempting to flee\n")
        if random.random() < 0.7:
            player.current_room_position = player.previous_room_position
            write("You manage to escape the battle.\n")
            try:
                draw_stillshot(player.get_current_room().visual) # draw room visual
            except:
                draw_stillshot(room_placeholder) # room has no visuals to print, print generic visual
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
        if command[1] in ["1", "first", "1st"]:
            target_index = 1
            write("attaking first\n")
        elif command[1] in ["2", "second", "2nd"]:
            target_index = 2
            if enemy_count < 2:
                write("\nThere is only one enemy\n")
                return True
        elif command[1] in ["3", "third", "3rd"]:
            target_index = 3
            if enemy_count < 3:
                write("\nThere are only 2 enemies\n")
                return True
        else:
            write("\nInvalid target, to choose an enemy write 'fisrt' or '1' to select the first enemy, same for every other enemy\n\n")
            return True
            
        for item in player.inventory:
            if item.id == command[2] or item.name == command[2]:
                if type(item) == items.Weapon:
                    count = 1
                    for e in player.get_current_room().enemies.values():
                        if count == target_index:
                            execute_attack(command[1], e, item)
                            break
                        else:
                            count += 1
                elif type(item) == items.Gun:
                    count = 1
                    for e in player.get_current_room().enemies.values():
                        if count == target_index:
                            execute_attack(command[1], e, item)
                            break
                        else:
                            count += 1

                    item.ammo -= 1
                else:
                    write("This item is not a weapon!\n\n")
                    return True
    
    elif command[0] in ["use", "consume"]:
        execute_consume(command[1])

    else:
        write("Thats not a valid action\n You can FIGHT, FLEE or USE\n\n")
        return True
        
    # enemy turn

    if len(player.get_current_room().enemies) == 0:
        write("You won the battle!\n", curses.color_pair(7))
        return False

    enemy_key = random.choice([*player.get_current_room().enemies.keys()]) # choose random enemy to attack
    enemy = player.get_current_room().enemies[enemy_key]

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
    enemies_dict = player.get_current_room().enemies
    enemies = []

    for enemy_id in enemies_dict:
        enemies.append(enemies_dict[enemy_id].name)

    write(f"You spot {len(enemies)} enemies. ")
    if len(enemies) == 0:
        write("no enemies (this prolly means theres an error, a user shouldnt see this)\n")
    if len(enemies) == 1:
        write(f"You see a {enemies[0]}.\n")
    else:
        write("You see a ")
        for i in range(0, len(enemies)):
            write(f"{enemies[i]} ")
            if i == len(enemies)-2:
                write(f"and {enemies[i+1]}.\n")
                break
            else:
                write(", ")
    
    write(f"\nYou have {player.health} health left.\n")

    weapons = []
    for item in player.inventory:
        if type(item) is items.Weapon or type(item) is items.Gun:
            weapons.append(item.name)

    weapon_num = len(weapons)
    if weapon_num == 0:
        write("You have no weapons to fight with.\n")
    elif weapon_num == 1:
        write(f"You have a {weapons[0]}.\n")
    else:
        write("You have a ")
        for i in range(0,weapon_num):
            write(f"{weapons[i]} ")
            if i == weapon_num-2:
                write(f"and {weapons[i+1]}.\n")
                break
            else:
                write(f", ")

    write("ATTACK <which enemy> <weapon>   or   ")
    write("CONSUME <item>   or   ")
    write("FLEE\n\n")

def print_intro(): # prints the intro text, makes all the sound effects italic and blinking
    write("\nzzzzzzzzz.. brrrrrrrr… crrrrrrrr\n", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write(" bbbbbrrrrrr…zzzzzzzz… ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write("EMERGENCY CODE: 35627", curses.color_pair(25))
    write(" beeeeeeeeep… ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write("Emergency Alert. If you can hear this you are currently a survivor.", curses.color_pair(25))
    write(" ...zzzzzzzz ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write("The date is… 28TH OF OCTOBER 2024…", curses.color_pair(25))
    write(" fzzzzzt bzzzzt ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write("Emergency contact systems are down due to unforeseen damage", curses.color_pair(25))
    write(" zzzzzzzzz.. brrrrrrrr… crrrrrrrr ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write(" crrrrrrr ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write("Current status: The infected population has been walled off to the remaining population", curses.color_pair(25))
    write(" zzzzzzzz ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write("despite this, Cardiff City has been classified as CRITICAL LEVEL", curses.color_pair(25))
    write(" bzzzzzt ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write(" fzzzzzzt ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write("Do NOT approach infected individuals… They are extremely dangerous and can transmit the infection through direct contact ", curses.color_pair(25))
    write(" beeeeeeeeeeep ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write("Military personnel are no longer in transit due to the lack of remaining survivors… ", curses.color_pair(25))
    write(" fzzzzzt bzzzzzzzt ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write("Attempt to escape the city at you’re own risk…", curses.color_pair(25))
    write(" ZZZZZZZZ ", curses.color_pair(25) | curses.A_ITALIC | curses.A_BLINK)
    write("\n – Transmission cuts.\n",curses.color_pair(25))


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
    ui.art_pad.clear()
    try:
        anim_thread = Thread(target=run_animation_curses_pad, args=[ui.art_pad, art_pad_args, ui_lock, resize_window_event, *animation])
        anim_thread.start()
        if hold:
            anim_thread.join() # if hold is true wait for animation to finish
            curses.flushinp() # flush any input from when animation was held
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
resize_window_event = threading.Event()

# This is the entry point of our program
def main():
    global user_input
    global overflow
    global ui_lock
    global in_combat
    global in_danger
    global resize_window_event

    try:

        # Startup Logic
        generate_map()
        
        #initialise curses screen
        init_screen()
        curses_setcolors()

        # play intro animations
        play_animation(intro_1, True) # hold main thread unntil this animation stops playing
        play_animation(intro_2)

    except Exception as e:
        close()
        print(f"Exception '{e}' occured at startup\n")
        print(traceback.format_exc())

    # write title screen
    write("""
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
""", curses.color_pair(24) | curses.A_BOLD)
    
    write()
    print_intro()
    
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
            
            elif cmd == curses.KEY_BACKSPACE or cmd == 127: # backspace # delete last char
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

            elif cmd == curses.KEY_RESIZE:
                ui_lock.acquire()
                resize_window() # update the x, y variables of ui
                resize_window_event.set() # set the resize window event so that animation threds know that the window was resized and can update pad args
                ui_lock.release()

            elif cmd == 10 or cmd == curses.KEY_ENTER: # enter key
                write()

                normalised_user_input = normalise_input(user_input)

                if in_combat == True:
                    in_combat = execute_combat(normalised_user_input)
                    if in_combat:
                        set_scene_combat()
                    else:
                        set_scene()
                elif in_danger == True:
                    resolution = resolve_danger(normalised_user_input)
                    if resolution == 0: # danger unresolved
                       in_danger = True
                    elif resolution == 1: # escaped from danger / fled back to last room
                        in_danger = False
                    elif resolution == 2: # combat started
                        in_danger = False
                        in_combat = True
                        play_animation(fight_cutscene)
                    
                elif in_combat == False and in_danger == False:
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
