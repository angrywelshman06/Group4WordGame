import random
from ani_sprites import *
import player

import copy

zombie = {
    "name" : "zombie",
    "description" : "DESCRIPTION",
    "health" : 20,
    "base_damage" : 10,
    "crit_chance" : 0.3,
    "crit_multiplier" : 2
}

zombie_child = {
    "name" : "zombie child",
    "description" : "DESCRIPTION",
    "health" : 8,
    "base_damage" : 5,
    "crit_chance" : 0.1,
    "crit_multiplier" : 4
}

zombie_dog = {
    "name" : "zombie dog",
    "description" : "DESCRIPTION",
    "health" : 10,
    "base_damage" : 8,
    "crit_chance" : 0.6,
    "crit_multiplier" : 2
}

zombie_strong = {
    "name" : "strong zombie",
    "description" : "DESCRIPTION",
    "health" : 30,
    "base_damage" : 15,
    "crit_chance" : 0.2,
    "crit_multiplier" : 2
}

zombie_soldier = {
    "name" : "zombie soldier",
    "description" : "DESCRIPTION",
    "health" : 25,
    "base_damage" : 13,
    "crit_chance" : 0.2,
    "crit_multiplier" : 2
}

class Creature:  ## Holds the info related to the creatures and stores spritesheet objects
    def __init__(self, creature : {}, creature_number = 0, level = 1):
        if creature == "You":
            self.creature_number = creature_number # Used for printing out the scene
            self.name = "You"
            self.description = "You"
            self.level = level
            self.health = player.health
            self.damage = "" 
            self.crit_change = "" 
            self.crit_multiplier = "" 
        else:
            self.creature_number = creature_number
            self.name = creature["name"]
            self.description = creature["description"]
            self.level = level # should get combat working first 
            self.health = creature["health"]
            self.damage = creature["base_damage"] * (1 + 0.4 * (self.level - 1))
            self.crit_chance = creature["crit_chance"]
            self.crit_multiplier = creature["crit_multiplier"]
    
    def get_damage(self, crit_bool : bool):
        if crit_bool:
            return self.damage * self.crit_multiplier
        return self.damage
        
    def create_sprites(self, creature_zlevel = 1, dx_change = 1, dy_change = 1, infosheet = False):
        self.path = self.grab_path()
        self.zlevel = creature_zlevel # Priority it takes when printing the animation
        self.color = 11
        if self.name != "You":
            self.color = 7
        self.dx_change = dx_change # moves the spritesheet on the screen
        self.dy_change = dy_change # moves the spritesheet on the screen
        self.frames = 6
        self.spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change)
        self.infosheet = infosheet
        if self.infosheet != False:
            self.color = 16
            if self.name != "You":
                self.color = 8
            self.spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change, infolist = self.grab_infolist())
        self.frameslist = self.spritesheet.frameslist
        self.frames_attack = self.spritesheet.frameslist
        self.frames_standstill = self.spritesheet.frameslist[0]
    
    def grab_path(self): # Path to the spritesheets
        return ("combat_sprites", "{0}".format(self.name))
    
    def grab_infolist(self):
        return [self.name, self.creature_number,self.level,self.health]
        
    def set_original_spritesheet(self): # Brings the spritesheet back to its original amount of frames
        del self.spritesheet
        self.spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change)
        self.frameslist = self.spritesheet.frameslist
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

##### Data related to visual printing of the combat
class Combatprinter():
    def __init__(self):
        self.creatures_dict = {} ### creatures in the current fight stored here. Protagonist is the first key "You"
        self.info_dict = {} # dictionary to store info enemy : info spritesheet pair
        self.enemies = player.get_current_room().enemies ### [(creature type, level), (creature type, level)]. This could be done differently and should be pulled from the back end.
        self.enemies_alive = len(self.creatures_dict.keys())-1 # -1 as one of the creatures is the protagonist 
        self.place_creatures() # Creates creature objects and corresponding spritesheets.
        self.stillstate = self.set_stillstate() # Returns tuple which is used in print_stillshot_curses
        self.animation = "" # the animation which will take place is stored here as a tuple

    def update_infosheet(self): # Updates HP in infospritesheets.
        # print(self.health)
        self.creatures_dict["You"].health = player.health
        
        #### checks for deaths, deletes entries in both dicts
        to_delete = False
        for i in self.creatures_dict:
            if self.creatures_dict[i].health <= 0:
                to_delete = i 
        if to_delete:
            del self.creatures_dict[to_delete]
            del self.info_dict[to_delete]
        self.stillstate = self.set_stillstate()
        
        ### Alters the info
        for i in self.creatures_dict:
            self.info_dict[i].health = self.creatures_dict[i].health
            # self.info_dict[i].spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change, infolist = self.grab_infolist())
            creature = self.info_dict[i]
            creature.create_sprites(creature_zlevel = creature.zlevel, dx_change = creature.dx_change, dy_change = creature.dy_change, infosheet = True)
        
    def refresh_sprites(self): # sets the spritesheets back to their original state
        for i in self.creatures_dict:
            self.creatures_dict[i].set_original_spritesheet()
        # for i in self.info_dict: # WIP, UPDATES INFO AFTER EVERY ATTACK
            # self.info_dict[i]
        self.stillstate = self.set_stillstate()    
        
    def blank_out_frames(self, spritesheet_to_modify): # Blanks out every other frame of a spritesheet
        for index, value in enumerate(spritesheet_to_modify):
            if index%2 == 1:
                newframe = ""
                for i in value:
                    if i == "\n":
                        newframe += "\n"
                    else:
                        newframe += " "
                spritesheet_to_modify[index] = newframe        
    
    def freeze_all(self, i): # Extends the first frame to the other frames in the same spritesheet
        firstframe = self.creatures_dict[i].spritesheet.frameslist[0]
        for index, value in enumerate(self.creatures_dict[i].spritesheet.frameslist):
            self.creatures_dict[i].spritesheet.frameslist[index] = firstframe 
            
    def set_new_sprites(self, attacker, attacked): # Makes changes to sprites and alters self.animation, the tuple which will be used when calling run_animation_curses
        self.refresh_sprites()
        if attacker == "You":
            for i in self.creatures_dict:
                if i != "You":
                    self.freeze_all(i) 
        
        if attacker != "You":
            for i in self.creatures_dict:
                if i != "enemy_{0}".format(attacker):
                    self.freeze_all(i)   
                    
        if attacked == "You":
            attacked = self.creatures_dict["You"]
        else:
            attacked = self.creatures_dict["enemy_{0}".format(attacked)]
            
        self.blank_out_frames(attacked.spritesheet.frameslist)
                    
        tuple_enemies = tuple([self.creatures_dict[i].spritesheet for i in self.creatures_dict])
        self.animation = (general_bg, outline, *tuple_enemies)
        
    def set_stillstate(self):
        return (general_bg, outline, *self.spritesheets_tuple())
    
    def general_update(self, attacker = 0, attacked = 0):
        if attacker != 0:
            self.set_new_sprites(attacker,attacked) # "1"/"2"...., "You"
        self.update_infosheet()
             
     
    def place_creatures(self):
        dx_change = 20
        dy_change = -8
        creature_number = 1
        counter = 1
        z = 6
        
        ### Protagonist sprites
        protag = Creature("You")
        protag_copy = copy.deepcopy(protag)
        protag.create_sprites(creature_zlevel = 5, dx_change = 3, dy_change = 8)
        protag_copy.create_sprites(creature_zlevel = 5.1, dx_change = 5, dy_change = 19, infosheet = True)
        self.creatures_dict["You"] = protag
        self.info_dict["You"] = protag_copy
        
        ### Enemy sprites
        self.enemies = player.get_current_room().enemies
        creatureobjects = [i for i in player.get_current_room().enemies.values()]
        
        for i in creatureobjects:
            dx_change += 10
            dy_change += 8
            counter += 1
            i.creature_number = creature_number
            i_copy = copy.deepcopy(i) # deep copy to be turned into the info spritesheet
            i.create_sprites(creature_zlevel = z, dx_change = dx_change, dy_change = dy_change)
            i_copy.create_sprites(creature_zlevel = z+0.1, dx_change = dx_change+2, dy_change = dy_change+7, infosheet = True)
            self.creatures_dict["enemy_{0}".format(creature_number)] = i
            self.info_dict["enemy_{0}".format(creature_number)] = i_copy
            if counter == 4:
                counter = 1
                dx_change -= 10
                dy_change = -6
            z += 1
            creature_number += 1
            
    def spritesheets_tuple(self): # Sends back a tuple of spritesheets ot unpack in run_animation_curses_pad
        spritesheets_to_add = [general_bg]
        for i in self.creatures_dict:
            spritesheets_to_add.append(self.creatures_dict[i].spritesheet)
        for i in self.info_dict:
            spritesheets_to_add.append(self.info_dict[i])
        spritesheets_to_add = tuple(spritesheets_to_add)
        return spritesheets_to_add

all_enemies = [zombie, zombie_child, zombie_dog, zombie_strong, zombie_soldier]