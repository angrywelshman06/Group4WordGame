#!/usr/bin/python3
import enemies
import items
import npcs
import player
import random
from items import Consumable, get_item_dict_from_list
from gameparser import *
from map import get_room, map_matrix, Room, generate_map
from colorama import Fore
import subprocess
import sys
from npcs import place_npcs



def install_requirements():
    try:
        import colorama
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


install_requirements()


def print_room_items(room: Room):
    # If there are no items, no output
    if len(room.items) == 0:
        return

    item_list = ""
    count = 0
    for item_id in room.items.keys():

        item_dict = get_item_dict_from_list(item_id)
        if item_dict is None:
            print(f"ERROR: {item_id} HAS NOT BEEN INITIALISED")
            continue

        item = items.Item(item_dict)

        if count == len(room.items) - 1 and len(room.items) > 1:
            item_list += " and "
        elif count != 0:
            item_list += ", "
        item_list += f"{room.items[item.id]} {item.name}"
        if room.items[item.id] > 1: item_list += "s"
        count += 1

    print(f"There is {item_list} here.")


# Prints information about the given room
def print_room(room: Room):
    print()
    print(room.name.upper())
    print()
    print(room.description)
    print()
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
            print("Congratulations! You have escaped the matrix. You win!")
            sys.exit()

        # Ensure the new room has an exit back to the current room
        opposite_direction = {"north": "south", "south": "north", "east": "west", "west": "east"}
        new_room.exits.add(opposite_direction[direction])

        player.previous_room_position = player.current_room_position
        player.current_room_position = new_pos

        if not player.get_current_room().visited:
            player.get_current_room().visited = True
            player.unique_rooms_visited += 1

        # for npc in npcs.randomly_placed_npcs:
        #     if npcs.randomly_placed_npcs[npc] == player.unique_rooms_visited:
        #         player.get_current_room().npcs.append(npc)

        print(f"You are going to {new_room.name}.")
    else:
        print("You cannot go there.")


def execute_consume(item_id):
    for item in player.inventory:
        if item.id == item_id:

            if type(item) != Consumable:
                break

            item.consume()
            print(f"You consumed a {item.name}.")
            player.inventory[item] -= 1
            if player.inventory[item] <= 0:
                player.inventory.pop(item)
            return True
    print("You cannot consume that.")
    return False


def execute_take(item_id, amount=1):

    for item_dict_id in player.get_current_room().items.keys():
        if item_dict_id == item_id:

            item = items.dict_to_item(get_item_dict_from_list(item_dict_id))

            if player.get_current_room().items[item_id] < amount:
                print(f"There are not {amount} many {item.name}s in the room.")
                return


            if player.get_current_room().items[item_id] > amount:
                player.get_current_room().items[item_id] -= amount
            else:
                player.get_current_room().items.pop(item_id)


            found = False
            for item in player.inventory.keys():
                if item.id == item_id:
                    player.inventory[item] += amount
                    found = True
                    break

            if not found:
                player.inventory[item] = amount

            print(f"You picked up {item.name}.")
            return
    print("You cannot take that.")


def execute_drop(item_id, amount=1):
    for item in player.inventory.keys():
        if item.id == item_id:

            if player.inventory[item] < amount:
                print(f"You do not have {amount} {item.name}s.")
                return

            if player.inventory[item] > amount:
                player.inventory[item] -= amount
            else:
                player.inventory.pop(item)

            if item.id in player.get_current_room().items:
                player.get_current_room().items[item.id] += amount
            else:
                player.get_current_room().items[item.id] = amount

            print(f"You dropped {item.name}.")
            return
    print("You cannot drop that.")

def execute_talk(npc_id):
    print(npc_id)
    for npc in player.get_current_room().npcs:
        print(npc.id)
        if npc.id == npc_id:
            npc.talk()
            return
    print("You cannot talk to this NPC.")


def execute_command(command):
    if 0 == len(command):
        return

    if len(player.get_current_room().enemies) >= 1:

        if command[0] == "fight":
            combat()
            return

        if command[0] in ["flee", "leave", "run"]:
            player.current_room_position = player.previous_room_position
            print(f"You fled back to the previous room!")
            return

        print("Not a valid command! Please choose either fight or flee.")
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            if len(command) >= 3 and str(command[2]).isdigit():
                execute_take(command[1], amount=int(command[2]));
                return
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            if len(command) >= 3 and str(command[2]).isdigit():
                execute_drop(command[1], amount=int(command[2])); return
            execute_drop(command[1])
        else:
            print("Drop what?")

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
        print("Goodbye!")
        sys.exit()

    elif command[0] == "help":
        print("Commands: go [direction], take [item], drop [item], use [item], talk [npc], quit")

    elif command[0] == "raptor":
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
        print("This makes no sense, it appears as though the first word is not one of the designated command words..")


def execute_attack(enemy_id, enemy: enemies.Enemy, weapon: items.Weapon):
    if random.random() < weapon.crit_chance:
        print(f"You hit the {enemy.name} for critical damage and dealt {weapon.get_damage(True)} damage.")
        enemy.health -= weapon.get_damage(True)
    else:
        print(f"You hit the {enemy.name} and dealt {weapon.get_damage(False)} damage.")
        enemy.health -= weapon.get_damage(False)

    if enemy.health > 0:
        print(f"The {enemy.name} now has {enemy.health} health.")
    else:
        player.get_current_room().enemies.pop(enemy_id)
        print(f"The {enemy.name} has been killed!")


def combat():
    # Main Combat Loop
    while True:
        print("=" * 40)  # To separate turns

        # Player turn, loop till valid command entered
        while True:

            print("\nMake your move.\n")
            print("ATTACK <enemy> <weapon>")
            print("CONSUME <item>")
            print("FLEE")

            for i in player.get_current_room().enemies:
                print(i)

            command = menu()

            # Flee command
            if command[0] == "flee":
                player.current_room_position = player.previous_room_position
                print(f"You fled back to the previous room!")
                return

            elif command[0] == "attack":

                # Checking correct number of prompts
                if len(command) < 3:
                    print("Invalid command. Type HELP for command prompts")
                    continue

                # Checking enemy is valid
                if command[1] not in player.get_current_room().enemies:
                    print(command[1])
                    print("Invalid enemy!")
                    continue

                item_valid = False
                for item in player.inventory:
                    if item.id == command[2]:

                        if type(item) == items.Weapon:
                            execute_attack(command[1], player.get_current_room().enemies[command[1]], item)
                            item_valid = True
                            break
                        else:
                            print("This item is not a weapon!")
                            continue

                if item_valid:
                    break
                else:
                    print("You do not have that item!")
                    continue

            elif command[0] in ["use", "consume"]:
                if execute_consume(command[1]):
                    break

        if len(player.get_current_room().enemies) == 0:
            print("You defeated all of the enemies. You can now advance into the room!")
            return

        # Enemy turn
        enemy = random.choice(list(player.get_current_room().enemies.values()))
        print(f"The {enemy.name} attacked you!")
        if random.random() < enemy.crit_chance:
            print(f"It hit you for critical damage and dealt {enemy.get_damage(True)} damage.")
            player.health -= enemy.get_damage(True)
        else:
            print(f"It dealt {enemy.get_damage(False)} damage.")
            player.health -= enemy.get_damage(False)

        if player.health > 0:
            print(f"You are now on {player.health} health.")
        else:
            # Player dead
            pass


def menu():

    if len(player.get_current_room().enemies) >= 1:
        print(
            f"There are {len(player.get_current_room().enemies)} enemies in this room. Choose whether to FIGHT to continue or FLEE to the previous room.")
    else:
        if player.get_current_room().exits:
            print("You can GO: " + ", ".join(player.get_current_room().exits))
            print()
        else:
            print("No exits available seems you might be stuck. What a shame ;)")
            print()

        if len(player.get_current_room().items) >= 1:
            print("You can TAKE any items in this room.")
            print_room_items(player.get_current_room()) # Displays items in room
            print()

        if len(player.inventory) >= 1:
            print("You can DROP any of the items in your inventory.")
            player.print_inventory_items()
            print(f"Current Inventory Mass: {player.inventory_mass()}g")
            print()

        if len(player.get_current_room().npcs) >= 1:
            for npc in player.get_current_room().npcs:
                print(f"You can TALK to {npc.id}.")
            print()

        if player.get_current_room().can_escape():
            print("You can ESCAPE!")


    # Read player's input
    user_input = input("Choose what you would like to do \n> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


# This is the entry point of our program
def main():
    # Startup Logic
    generate_map()
    place_npcs()

    # Main game loop
    while True:
        # Differentiates turns
        # Can remove once formatted
        print("=" * 40)

        print_room(player.get_current_room())

        # Show the menu with possible actions and ask the player
        command = menu()

        if command[0] == "escape" and player.get_current_room().can_escape():
            print(
                "Congratulations you have escaped the matrix, you are free from Cardiff and for you the game is over.")
            break

        # Execute the player's command
        execute_command(command)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    print(Fore.YELLOW + r"""\
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
    main()
