import random


class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.find_dc = random.randint(1, 20)

    def on_take(self):
        print(f"You have picked up {self.name}")

    def on_drop(self):
        print(f"You have dropped {self.name}")


class Weapon(Item):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.damage = 8

