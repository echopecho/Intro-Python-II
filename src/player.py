# Write a class to hold player information, e.g. what room they are in
# currently.
import random
import math


class Character:
    def __init__(self, name, level, stats):
        self.name = name
        self.proficiency = math.ceil(level / 4) + 1
        self.level = level
        self.loot = []
        self.curret_hp = self.max_hp = sum(random.sample(range(2, 8), self.level))
        self.stats = dict(zip(stats.keys(), self.set_stats(stats)))
        self.armor_class = 12 + self.stats["dex"].modifier

    def set_stats(self, stats):
        stat_list = []
        for stat in stats.items():
            stat_list.append(Character.Stat(self, stat))
        return stat_list

    def attack(self):
        weapon = [item for item in self.loot if item.name == "sword"]
        if not weapon:
            print("You have no weapon!")
        else:
            damage = (
                random.randint(1, weapon[0].damage)
                + self.stats["dex"].modifier
                + self.proficiency
            )
            print(f"You did {damage} points of damage!")
            return damage

    class Stat:
        def __init__(self, char, stat):
            self.char = char
            self.name = stat[0]
            self.score = stat[1]
            self.modifier = int((self.score - 10) / 2)
            self.saving_throw = self.char.proficiency + self.modifier


class Player(Character):
    def __init__(self, name, position, level, stats):
        super().__init__(name, level, stats)
        self.current_room = position
        self.current_hp = self.max_hp = (
            self.max_hp + self.stats["con"].modifier * self.level
        )

        # for key, value in self.stats.items():
        #     mod = int((value - 10) / 2)
        #     self.modifiers[key] = mod

    def investigate(self):
        return random.randint(1, 20) + self.stats["int"].modifier + self.proficiency

