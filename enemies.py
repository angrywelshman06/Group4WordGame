class Enemy:
    def __init__(self, enemy : {}, level=1):
        self.name = enemy["name"]
        self.description = enemy["description"]
        self.level = level
        self.health = enemy["health"]
        self.damage = enemy["base_damage"] * (1 + 0.4 * self.level)


zombie = {
    "name" : "zombie",
    "description" : "DESCRIPTION",
    "health" : 50,
    "base_damage" : 10
}