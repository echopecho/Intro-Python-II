# Write a class to hold player information, e.g. what room they are in
# currently.


class Player:
    def __init__(self, name, position):
        self.name = name
        self.current_room = position
