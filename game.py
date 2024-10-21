#!/usr/bin/python3
import player
from map import Room, generate_map, map_matrix, door_assigner
from gameparser import *
from player import current_room_position
from map import get_room, map_matrix, door_assigner
import random
from colorama import Fore, Back, Style
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

    # Print exits
    if room.exits:
        print("Exits: " + ", ".join(room.exits))
    else:
        print("No exits available.")

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
            item.consume()
            print(f"You consumed a {item.name}.")
            player.inventory[item] -= 1
            if player.inventory[item] <= 0:
                player.inventory.pop(item)
            return
    print("You cannot consume that.")


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

    elif command[0] in ["use", "consume"]:
        if len(command) > 1:
            execute_consume(command[1])

    else:
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
# Display menu
    #print_menu(exits, room_items, inv_items)

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
            pass # Game completed


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
    print(Fore.YELLOW + """\
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

