import curses
from ani_sprites import *
# from animator import *

# What do I want to achieve here?
# The end result of this should be a tuple that's assigned to an attribute which
# can then be used as an arg in print_stillshot
# However, I also need a way to handle the animations of the zombies or MC attacking.

# Maybe create another class that handles the animation state of the characters?


# pseudo of the mainloop during a battle
# gameloop():
#   ...
#   ...
#   battle():
#       fight = initiate_combat(("zombie_1", 2), ("zombie_2", 1), ("zombie_3", 1))
#       while (playerhp != 0) or (enemies_alive != 0):
#           ### stillshot of the combat situation
#           ### player takes turn
#           ### call animation of player attacking, zombie getting hit
#           ### back to stillshot
#           ### zombie taking turn
#           ### call animation of zombie attacking, player getting hit
#           ### back to stillshot
#       del fight
#   ...
#   ...

# 1st step: Battle animation. Actually put the characters on the screen
# 2nd step: Pulling the frames of standstill and attack to their respective attributes
# 3nd step: Handle the battle state going from stillshot, to something moving, and back to stillshot. Calling standstill and attack.

class creature():
    def __init__(self, path, creature_type, creature_name, creature_level, creature_zlevel, dx_change, dy_change):
        self.path = path
        self.creature_type = creature_type
        self.creature_name = creature_name
        self.creature_level = creature_level
        self.z = creature_zlevel
        self.hp = 100
        self.basedmg = 3
        self.spritesheet = spritesheet(self.path, 11, zlevel = creature_zlevel, frames = 6, dx = dx_change, dy = dy_change )
        self.frames_attack = self.spritesheet.frameslist
        self.frames_standstill = self.spritesheet.frameslist[0]

    def gather_framelist(self): ### WIP here the name of the creature will be appended below every sprite. Currently, it's just a copy of the original gather_framelist. No use yet.
        frameslist = []
        for frame in range(1,self.frames+1):
            # path = os.path.join("modularanimation","spritesheets","{0}".format(self.path), "txt", "ascii-art ({0}).txt".format(frame)) ## os.path.join works regardless of OS
            path = os.path.join("spritesheets",*self.path, "ascii-art ({0}).txt".format(frame)) #if ran directly from animator.py
            file = open(path, "r", encoding="utf-8")
            frameslist.append(file.read())
            file.close()
        return frameslist   


class initiate_combat():
    def __init__(self, curses_window, *enemies):
        self.creatures_dict = {}
        self.enemies = enemies
        self.curses_window = curses_window
        self.place_creatures()
        # self.draw_on_window()
    
    def place_creatures(self):
        dx_change = 55
        dy_change = 3
        counter = 1
        z = 6
        
        ### Could use a rudimentary leveling up system for the protagonist
        ### such as basic attack and hp going up by a given percentage upon level up
        protag = creature(("placeholder",),"protag", "You", 1, z, dx_change, dy_change) #level can be replaced with protagonist level variable
        
        for i in self.enemies:
            # enemy = spritesheet(("placeholder",), 3, zlevel = z, frames = 2)
            enemy_type = i[0]
            enemy_level = i[1]
            enemy_name = "Zombie_{0}".format(counter)
            enemy = creature(("placeholder",),enemy_type, enemy_name, enemy_level, z, dx_change, dy_change)
            self.creatures_dict["Enemy_{0}".format(counter)] = enemy
            dx_change += 6
            dy_change += 3
            counter += 1
    
    def draw_on_window(self):
        # need everything as a tuple
        print(len(self.creatures_dict))
        creatures_to_add = []
        for i in self.creatures_dict:
            creatures_to_add.append(self.creatures_dict[i].spritesheet)
        # print(creatures_to_add)
        creatures_to_add = tuple(creatures_to_add)
        print(creatures_to_add)
        # frames_to_print = [0 for i in range(len(creatures_to_add))]
        # return (frames_to_print,self.curses_window, *creatures_to_add)
        return creatures_to_add
        
        
    
# fight = initiate_combat(("zombie", 2), ("zombie", 1), ("zombie", 1))
# print(len(self.creatures_dict))