import random

class Creature:
    def __init__(self, enemy : {}, level=1):
        self.name = enemy["name"]
        self.description = enemy["description"]
        self.level = level
        self.health = enemy["health"]
        self.damage = enemy["base_damage"] * (1 + 0.4 * (self.level - 1))
        self.crit_chance = enemy["crit_chance"]
        self.crit_multiplier = enemy["crit_multiplier"]

    def get_damage(self, crit_bool : bool):
        if crit_bool:
            return self.damage * self.crit_multiplier
        return self.damage




zombie = {
    "name" : "zombie",
    "description" : "DESCRIPTION",
    "health" : 50,
    "base_damage" : 10,
    "crit_chance" : 0.3,
    "crit_multiplier" : 2
}