import random
from ani_sprites import *
import player

import copy

## EVERYTHING HERE IS NOW CONTAINED WITHIN CLASS CREATURE.
# class Enemy:
    # def __init__(self, enemy : {}, level=1):
        # self.name = enemy["name"]
        # self.description = enemy["description"]
        # self.level = level
        # self.health = enemy["health"]
        # self.damage = enemy["base_damage"] * (1 + 0.4 * (self.level - 1))
        # self.crit_chance = enemy["crit_chance"]
        # self.crit_multiplier = enemy["crit_multiplier"]

    # def get_damage(self, crit_bool : bool):
        # if crit_bool:
            # return self.damage * self.crit_multiplier
        # return self.damage
        
protag = { # placeholder
    "name" : "You",
    "description" : "DESCRIPTION",
    "health" : 50,
    "base_damage" : 10,
    "crit_chance" : 0.3,
    "crit_multiplier" : 2
}

zombie = {
    "name" : "zombie",
    "description" : "DESCRIPTION",
    "health" : 50,
    "base_damage" : 10,
    "crit_chance" : 0.3,
    "crit_multiplier" : 2
}

zombie_child = {
    "name" : "zombie child",
    "description" : "DESCRIPTION",
    "health" : 15,
    "base_damage" : 5,
    "crit_chance" : 0.1,
    "crit_multiplier" : 4
}

zombie_dog = {
    "name" : "zombie dog",
    "description" : "DESCRIPTION",
    "health" : 25,
    "base_damage" : 8,
    "crit_chance" : 0.6,
    "crit_multiplier" : 2
}

zombie_strong = {
    "name" : "strong zombie",
    "description" : "DESCRIPTION",
    "health" : 65,
    "base_damage" : 15,
    "crit_chance" : 0.2,
    "crit_multiplier" : 2
}

zombie_soldier = {
    "name" : "zombie soldier",
    "description" : "DESCRIPTION",
    "health" : 80,
    "base_damage" : 13,
    "crit_chance" : 0.2,
    "crit_multiplier" : 2
}

class Creature:  
    def __init__(self, creature : {}, creature_number = 0, level = 1):
        if creature == "You":
            self.creature_number = creature_number # Used for printing out the scene
            self.name = "You"
            self.description = "You"
            self.level = level
            self.health = player.health
            self.damage = "" #NA
            self.crit_change = "" #NA
            self.crit_multiplier = "" #NA
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
        self.dx_change = dx_change
        self.dy_change = dy_change
        self.frames = 6
        self.spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change)
        # self.info = spritesheet(self.path,self.color, zlevel = 100, frames = 6, dx = self.dx_change, dy = self.dy_change) # increment dx dy to change position
        # self.info.transform_to_info(self.grab_infolist())
        self.infosheet = infosheet
        if self.infosheet != False:
            self.color = 16
            if self.name != "You":
                self.color = 8
            self.spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change, infolist = self.grab_infolist())
        # print(self.info.frameslist[0])
        self.frameslist = self.spritesheet.frameslist
        self.frames_attack = self.spritesheet.frameslist
        self.frames_standstill = self.spritesheet.frameslist[0]
    
    def grab_path(self):
        return ("combat_sprites", "{0}".format(self.name))
    
    def grab_infolist(self):
        return [self.name, self.creature_number,self.level,self.health]
        
    def set_original_spritesheet(self): # Brings the spritesheet back to its original amount of frames
        del self.spritesheet
        self.spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change)
        self.frameslist = self.spritesheet.frameslist
        self.frames_attack = self.spritesheet.frameslist
        self.frames_standstill = self.spritesheet.frameslist[0]
        # self.spritesheet.frameslist = self.gather_framelist()

    def gather_framelist(self): ### WIP here the name of the creature will be appended below every sprite. Currently, it's just a copy of the original gather_framelist. No use yet.
        frameslist = []
        for frame in range(1,self.frames+1):
            # path = os.path.join("modularanimation","spritesheets","{0}".format(self.path), "txt", "ascii-art ({0}).txt".format(frame)) ## os.path.join works regardless of OS
            path = os.path.join("spritesheets",*self.path, "ascii-art ({0}).txt".format(frame)) #if ran directly from animator.py
            file = open(path, "r", encoding="utf-8")
            frameslist.append(file.read())
            file.close()
        return frameslist   

##### Data related to the current fight is contained within initiate_combat objects.
class Combatprinter():
    def __init__(self):
        self.creatures_dict = {} ### creatures in the current fight stored here. Protagonist is the first key "You"
        self.info_dict = {} # dictionary to store info enemy : info spritesheet pair
        self.enemies = player.get_current_room().enemies ### [(creature type, level), (creature type, level)]. This could be done differently and should be pulled from the back end.
        # self.curses_window = curses_window
        self.enemies_alive = len(self.creatures_dict.keys())-1 # -1 as one of the creatures is the protagonist 
        self.escape = False # To be used to break from combat loop
        self.place_creatures() # Creates creature objects and corresponding spritesheets.
        # self.info_details() # obsolete for now 
        self.current_weapon = "" # NEEDS WORK: Pull the item of the players from the backend?. This will then be used to set the corresponding spriteshet of the protagonist (WIP)
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
        
        ### Alters the info
        for i in self.creatures_dict:
            self.info_dict[i].health = self.creatures_dict[i].health
            # self.info_dict[i].spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change, infolist = self.grab_infolist())
            creature = self.info_dict[i]
            creature.create_sprites(creature_zlevel = creature.zlevel, dx_change = creature.dx_change, dy_change = creature.dy_change, infosheet = True)
        
            
    # def get_current_room():
        # return map.get_room(current_room_position[0], current_room_position[1])
    
    def refresh_sprites(self): # sets the spritesheets back to their original state
        for i in self.creatures_dict:
            self.creatures_dict[i].set_original_spritesheet()
        # for i in self.info_dict: # WIP, UPDATES INFO AFTER EVERY ATTACK
            # self.info_dict[i]
        self.stillstate = self.set_stillstate()    
    
    def refresh_info(self, spritesheet, info):
        pass
        
    def change_protag_sprites(self): #WIP. This will fire when the protag changes weapons.
        pass
        
    def blank_out_frames(self, spritesheet_to_modify): # NEW
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
            # firstframe = self.creatures_dict["enemy_{0}".format(attacker)].spritesheet.frameslist[0]
            # for index, value in enumerate(self.creatures_dict["You"].spritesheet.frameslist):
                # self.creatures_dict["You"].spritesheet.frameslist[index] = firstframe  
            for i in self.creatures_dict:
                if i != "enemy_{0}".format(attacker):
                    self.freeze_all(i)   
                    
        if attacked == "You":
            attacked = self.creatures_dict["You"]
        else:
            attacked = self.creatures_dict["enemy_{0}".format(attacked)]
            
        self.blank_out_frames(attacked.spritesheet.frameslist)

        # tuple_enemies = tuple([self.creatures_dict[i] for i in self.creatures_dict])                      
        tuple_enemies = tuple([self.creatures_dict[i].spritesheet for i in self.creatures_dict])
        # self.curses_window.clear()
        self.animation = (general_bg, outline, *tuple_enemies)
        
    def set_stillstate(self):
        return (general_bg, outline, *self.spritesheets_tuple())
    
    def general_update(self, attacker = 0, attacked = 0):
        # if attacker == "You":
            # self.set_new_sprites(attacker,attacked) # "You", "1"/"2"....
            # return
        if attacker != 0:
            self.set_new_sprites(attacker,attacked) # "1"/"2"...., "You"
        self.update_infosheet()
            
        
    # def user_update(self, user_input): #### this should also 
        # if user_input == "escape":
            # self.escape = True
            # return
        ### Here, the user input must be in the format "attack_1", "attack_2".. etc
        # if user_input[:-2] == "attack":
            # damage = 5 # Placeholder. This can go through a random damage generator that's based on the player's base attack stat
            # protag = self.creatures_dict["You"]
            # enemy = self.creatures_dict["Creature_{0}".format(user_input[-1:])]
            # enemy.hp -= damage
            # self.set_new_sprites(protag, enemy)

    # def zombie_update(self): ### NEEDS WORK. Should attack character based on enemy's basedmg
        #### Placeholder
        # protag = self.creatures_dict["You"]
        # enemies = [creature for creature in self.creatures_dict.values() if creature.creature_type != "You"]
        # enemy = random.choice(enemies)
        # protag.hp -= enemy.basedmg # should be modified so it's random to some degree
        # print(protag.hp)
        # self.set_new_sprites(enemy, protag)
        # self.refresh_sprites()
        #### FUNCTION TO UPDATE ANIMATION TUPLE HERE
     # (self,creature_number, backend_dict, creature_zlevel = 1, dx_change = 0, dy_change = 0)   
     
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
            # (self, creature : {}, creature_number = 0, level = 1, creature_zlevel = 1, dx_change = 1, dy_change = 1, infosheet = False)
            i_copy = copy.deepcopy(i) # to be turned into the info spritesheet
            i.create_sprites(creature_zlevel = z, dx_change = dx_change, dy_change = dy_change)
            i_copy.create_sprites(creature_zlevel = z+0.1, dx_change = dx_change+2, dy_change = dy_change+7, infosheet = True)
            self.creatures_dict["enemy_{0}".format(creature_number)] = i
            self.info_dict["enemy_{0}".format(creature_number)] = i_copy
            # print(self.info_dict["enemy_1"].spritesheet.frameslist)
            # self.creatures_dict["enemy_{0}".format(creature_number)] = Creature(i,creature_number, creature_zlevel = z, dx_change = dx_change, dy_change = dy_change)
            if counter == 4:
                counter = 1
                dx_change -= 10
                dy_change = -6
            z += 1
            creature_number += 1
            
    def spritesheets_tuple(self):
        # need everything as a tuple so I can unpack it
        spritesheets_to_add = [general_bg]
        for i in self.creatures_dict:
            spritesheets_to_add.append(self.creatures_dict[i].spritesheet)
        for i in self.info_dict:
            spritesheets_to_add.append(self.info_dict[i])
        spritesheets_to_add = tuple(spritesheets_to_add)
        return spritesheets_to_add

all_enemies = [zombie, zombie_child, zombie_dog, zombie_strong, zombie_soldier]