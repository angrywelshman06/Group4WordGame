#!/usr/bin/python3
import enemies
import items
import player
import random
from items import Consumable
from gameparser import *
from map import get_room, map_matrix, door_assigner, Room, generate_map
from colorama import Fore
import subprocess
import sys

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

    print(f"There is {list_of_items(room.items)} here.")
    print()

# Prints information about the given room
def print_room(room: Room):
    print()
    print(room.name.upper())
    print()
    print(room.description)
    print()
    print_room_items(room)  # Displays items in room

    if len(room.enemies) == 0:

        # Print exits
        if room.exits:
            print("Exits: " + ", ".join(room.exits))
        else:
            print("No exits available seems you might be stuck. What a shame ;)")

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
            print("Congratulations! You have escaped the matrix. You win!")
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


def execute_take(item_id):
    for item in player.get_current_room().items:
        if item["id"] == item_id:

            if player.inventory_mass() + item.mass > player.max_mass:
                print("You cannot take that, your inventory is too small")
                print(f"Current Inventory Mass: {player.inventory_mass()}g")
                print(f"Mass of {item.name}: {item.mass}g")
                return
            player.get_current_room().items.pop(player.get_current_room().items.index(item))
            player.inventory.append(item)
            print(f"You picked up {item.name}.")
            return
    print("You cannot take that.")


def execute_drop(item_id):
    for item in player.inventory:
        if item.id == item_id:
            player.inventory.pop(player.inventory.index(item))
            player.get_current_room().items.append(item)
            print(f"You dropped {item.name}.")
            return
    print("You cannot drop that.")


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
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    elif command[0] in ["consume"]:
        if len(command) > 1:
            execute_consume(command[1])

    elif command[0] == "quit":
        print("Goodbye!")
        sys.exit()

    elif command[0] == "help":
        print("Commands: go [direction], take [item], drop [item], use [item], quit")

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
        print("This makes no sense.")

def execute_attack(enemy : enemies.Enemy, weapon : items.Weapon):

    if random.random() < weapon.crit_chance:
        print(f"You hit the {enemy.name} for critical damage and dealt {weapon.get_damage(True)} damage.")
        enemy.health -= weapon.get_damage(True)
    else:
        print(f"You hit the {enemy.name} and dealt {weapon.get_damage(False)} damage.")
        enemy.health -= weapon.get_damage(False)

    if enemy.health > 0:
        print(f"The {enemy.name} now has {enemy.health} health.")
    else:
        player.get_current_room().enemies.pop(player.get_current_room().enemies.index(enemy))
        print(f"The {enemy.name} has been killed!")

def combat():

    # Main Combat Loop
    while True:
        print("=" * 40) # To separate turns

        # Player turn, loop till valid command entered
        while True:

            print("\nMake your move.\n")
            print("ATTACK <enemy> <weapon>")
            print("CONSUME <item>")
            print("FLEE")

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
                if not( 1 <= int(command[1]) <= len(player.get_current_room().enemies)):
                    print("Invalid enemy!")
                    continue

                item_valid = False
                for item in player.inventory:
                    if item.id == command[2]:

                        if type(item) == items.Weapon:
                            execute_attack(player.get_current_room().enemies[int(command[1]) - 1], item)
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
        enemy = random.choice(player.get_current_room().enemies)
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

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


# This is the entry point of our program
def main():

    # Startup Logic
    generate_map()

    # Main game loop
    while True:
        # Differentiates turns
        # Can remove once formatted
        print("=" * 40)

        if player.get_current_room() is None:
            print("Congratulations you have escaped the matrix, you are free from Cardiff and for you the game is over.")

        print_room(player.get_current_room())

        if len(player.get_current_room().enemies) >= 1:
            print(f"There are {len(player.get_current_room().enemies)} enemies in this room. Choose whether to fight to continue or flee to the previous room.")
        else:
            # Display game status (room description, inventory etc.)
            player.print_inventory_items()
            print(f"Current Inventory Mass: {player.inventory_mass()}g")
            print()
            print(player.current_room_position)


        # Show the menu with possible actions and ask the player
        command = menu()

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

