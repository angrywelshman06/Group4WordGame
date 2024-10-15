#!/usr/bin/python3
import player
from map import Room
from items import *
from gameparser import *


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

    print(f"There is {list_of_items(room["items"])} here.")
    print()


def print_inventory_items(items):
    if len(items) == 0:
        return

    print(f"You have {list_of_items(items)}.")
    print()

def is_valid_exit(exits, chosen_exit): # used to check if the exit is valid
    return chosen_exit in exits


def execute_go(direction):
    if is_valid_exit(player.current_room["exits"], direction):
        player.current_room = move(player.current_room["exits"], direction)
        print(f"You are going to {player.current_room["name"]}.")
    else:
        print("You cannot go there.")


def execute_take(item_id):
    for item in player.current_room["items"]:
        if item["id"] == item_id:

            if player.inventory_mass() + item["mass"] > player.max_mass:
                print("You cannot take that, your inventory is too small")
                print(f"Current Inventory Mass: {player.inventory_mass()}g")
                print(f"Mass of {item["name"]}: {item["mass"]}g")
                return
            player.current_room["items"].pop(player.current_room["items"].index(item))
            player.inventory.append(item)
            print(f"You picked up {item["name"]}.")
            return
    print("You cannot take that.")


def execute_drop(item_id):
    for item in player.inventory:
        if item["id"] == item_id:
            player.inventory.pop(player.inventory.index(item))
            player.current_room["items"].append(item)
            print(f"You dropped {item["name"]}.")
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


# This is the entry point of our program
def main():

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

