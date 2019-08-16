import os
from room import Room
from player import Player, Character
from item import Item, Weapon

# Declare all the rooms

room = {
    "outside": Room("Outside Cave Entrance", "North of you, the cave mount beckons"),
    "foyer": Room(
        "Foyer",
        """Dim light filters in from the south. Dusty
passages run north and east.""",
    ),
    "overlook": Room(
        "Grand Overlook",
        """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""",
    ),
    "narrow": Room(
        "Narrow Passage",
        """The narrow passage bends here from west
to north. The smell of gold permeates the air.""",
    ),
    "treasure": Room(
        "Treasure Chamber",
        """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""",
    ),
}

loot = {
    "rare_weapon": Weapon(
        "sword", "Magical weapon that adds +2 to attack and damage rolls"
    ),
    "spell_1": Item("scroll", "Magical scroll containing the Fireball spell"),
    "spell_2": Item("scroll", "Magical scroll containing the Cure Wounds spell"),
    "legendary_breastplate": Item(
        "armor", "The breastplate worn by the great warrior Francis, Lord of Storms"
    ),
    "gold": Item("currency", "250 pieces of gold"),
}


# Link rooms together

room["outside"].n_to = room["foyer"]
room["foyer"].s_to = room["outside"]
room["foyer"].n_to = room["overlook"]
room["foyer"].e_to = room["narrow"]
room["overlook"].s_to = room["foyer"]
room["narrow"].w_to = room["foyer"]
room["narrow"].n_to = room["treasure"]
room["treasure"].s_to = room["narrow"]

room["overlook"].treasure = [loot["rare_weapon"]]
room["foyer"].treasure = [loot["spell_2"], loot["gold"]]
room["treasure"].treasure = [
    loot["spell_1"],
    loot["legendary_breastplate"],
    loot["gold"],
]
monster_stats = {"str": 16, "dex": 14, "con": 16, "int": 6, "wis": 12, "cha": 6}
room["treasure"].monsters = [Character("Kobold", 2, monster_stats)]


#
# Main
#

# Make a new player object that is currently in the 'outside' room.

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
def clear():
    os.system("cls")


player_stats = {"str": 12, "dex": 14, "con": 16, "int": 10, "wis": 16, "cha": 8}
player = Player("Ned", room["outside"], 3, player_stats)
# player.hp += player.modifiers["con"] * player.level

playing = True

clear()
while playing:
    # print(player.stats["wis"].score)
    # print(player.current_hp)
    print(player.current_room)

    selection = input(
        """
What would you like to do next?
    (n): North  (s): South  (e): East  (w): West
    (v): Investigate
    (i): Inventory
    (q): Quit
        """
    ).lower()

    # Quit the game
    if selection == "q":

        playing = False

    # Move the player to the room in that direction if possible
    elif selection in ("n", "e", "w", "s"):

        direction = selection + "_to"
        try:
            new_room = getattr(player.current_room, direction)
            player.current_room = new_room
            clear()
        except:
            clear()
            print("**Nothing to find in that direction**")

    # Investigate to find items in current room
    elif selection == "v":

        investigation_check = player.investigate()
        clear()
        print(f"You roll a {investigation_check} and find...")

        found_items = [
            item
            for item in player.current_room.treasure
            if item.find_dc <= investigation_check
        ]

        # Print the investigation results
        if len(found_items) == 0:
            print("  Nothing")
        else:
            for item in found_items:
                print(f"  ({item.name}) {item.description}")

    # Print the player's inventory
    elif selection == "i":
        clear()
        print("Inventory:")
        print("-----------")
        for item in player.loot:
            print("  " + item.description)

    elif selection == "a":
        clear()
        damage = player.attack()

    # Look for an action like get or drop
    elif len(selection.split()) > 1:

        action, item, *left_over = selection.split(" ")

        # Handle getting a new item from the room
        if action in ("get", "take"):
            collected_item = list(
                filter(lambda el: el.name == item, player.current_room.treasure)
            )[0]

            clear()
            collected_item.on_take()
            player.loot.append(collected_item)
            player.current_room.treasure.remove(collected_item)

        # Handle dropping an item from player's inventory
        elif action == "drop":

            dropped_item = list(filter(lambda el: el.name == item, player.loot))[0]

            clear()
            dropped_item.on_drop()
            player.current_room.treasure.append(dropped_item)
            player.loot.remove(dropped_item)

    # Handle all other inputs
    else:
        clear()
        print("Please select an appropriate input")
