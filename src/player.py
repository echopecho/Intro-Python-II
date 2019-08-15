# Write a class to hold player information, e.g. what room they are in
# currently.
import random


class Player:
    def __init__(self, name, position):
        self.name = name
        self.current_room = position
        self.investigation = 3
        self.loot = []

    def investigate(self):
        return random.randint(1, 20) + self.investigation

