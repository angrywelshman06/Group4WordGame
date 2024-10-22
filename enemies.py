class Enemy:
    def __init__(self, enemy : {}):
        self.name = enemy["name"]
        self.description = enemy["description"]
        self.health = enemy["health"]
        self.damage = enemy["damage"]


zombie = {
    "name" : "zombie",
    "description" : "DESCRIPTION",
    "health" : 50,
    "damage" : 10
}