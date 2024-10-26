import curses
import random
import copy
from ani_sprites import *

curses.initscr()
# curses_setcolors()

zombie = {
    "name" : "zombie",
    "description" : "DESCRIPTION",
    "health" : 50,
    "base_damage" : 10,
    "crit_chance" : 0.3,
    "crit_multiplier" : 2,
    "spritesheet" : holder1 # ani_sprites spritesheet object
}

zombie_child = {
    "name" : "zombie child",
    "description" : "DESCRIPTION",
    "health" : 15,
    "base_damage" : 5,
    "crit_chance" : 0.1,
    "crit_multiplier" : 4,
    "spritesheet" : holder1 # ani_sprites spritesheet object
}
protag = {
    "name" : "Protag",
    "description" : "DESCRIPTION",   
    "health" : 200,
    "base_damage" : 20,
    "crit_chance" : 0.3,
    "crit_multiplier" : 2,
    "spritesheet" : holder1
}


class creature():
    # def __init__(self, path,creature_number, creature_type, color, creature_level = 1, hp = 20, creature_zlevel = 1, dx_change = 0, dy_change = 0):
        # self.path = path
        # self.creature_number = 0
        # self.creature_type = creature_type
        # self.creature_level = creature_level
        # self.zlevel = creature_zlevel # Priority it takes when printing the animation
        # self.hp = hp
        # self.color = 3
        # self.basedmg = 3 #Placeholder. Should use self.set_base_damage
        # self.dx_change = dx_change
        # self.dy_change = dy_change
        # self.frames = 6
        # self.spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change)
        # self.frameslist = self.spritesheet.frameslist
        # self.frames_attack = self.spritesheet.frameslist
        # self.frames_standstill = self.spritesheet.frameslist[0]
        
    def __init__(self,creature_number, backend_dict, creature_zlevel = 1, dx_change = 0, dy_change = 0):
        self.creature_number = creature_number
        self.creature_type = backend_dict["name"]
        self.description = backend_dict["description"]
        self.level = 1 # should get combat working first 
        self.health = backend_dict["health"]
        self.damage = backend_dict["base_damage"] * (1 + 0.4 * (self.level - 1))
        self.crit_chance = backend_dict["crit_chance"]
        self.crit_multiplier = backend_dict["crit_multiplier"]
        
        self.zlevel = creature_zlevel # Priority it takes when printing the animation
        self.color = 33
        if self.creature_type != "Protag":
            self.color = 7
        self.dx_change = dx_change
        self.dy_change = dy_change
        self.frames = 6
        self.spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change)
        self.frameslist = self.spritesheet.frameslist
        self.frames_attack = self.spritesheet.frameslist
        self.frames_standstill = self.spritesheet.frameslist[0]
    
    def grab_infolist(self):
        return [self.creature_type, self.creature_number,self.creature_level,self.hp]
    
    def set_base_damage(self):
        #### Base damage should be set based off the type of the creature WIP
        pass
        
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
class initiate_combat():
    def __init__(self, curses_window, enemies):
        self.creatures_dict = {} ### creatures in the current fight stored here. Protagonist is the first key "protag"
        self.info_dict = {} # dictionary to store info enemy : info spritesheet pair
        self.enemies = enemies ### [(creature type, level), (creature type, level)]. This could be done differently and should be pulled from the back end.
        self.curses_window = curses_window
        self.enemies_alive = len(self.creatures_dict.keys())-1 # -1 as one of the creatures is the protagonist 
        self.escape = False # To be used to break from combat loop
        self.place_creatures() # Creates creature objects and corresponding spritesheets.
        # self.info_details() # obsolete for now 
        self.current_weapon = "" # NEEDS WORK: Pull the item of the players from the backend?. This will then be used to set the corresponding spriteshet of the protagonist (WIP)
        self.stillstate = self.set_stillstate() # Returns tuple which is used in print_stillshot_curses
        self.animation = "" # the animation which will take place is stored here as a tuple
        
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
        if attacker.creature_type == "protag":
            for i in self.creatures_dict:
                if i != "protag":
                    self.freeze_all(i) 
        
        if attacker.creature_type != "protag":
            firstframe = self.creatures_dict["protag"].spritesheet.frameslist[0]
            for index, value in enumerate(self.creatures_dict["protag"].spritesheet.frameslist):
                self.creatures_dict["protag"].spritesheet.frameslist[index] = firstframe  
            for i in self.creatures_dict:
                if self.creatures_dict[i] != attacker:
                    self.freeze_all(i)   
            
        self.blank_out_frames(attacked.spritesheet.frameslist)
                        
        tuple_enemies = tuple([self.creatures_dict[i] for i in self.creatures_dict])
        self.curses_window.clear()
        self.animation = (self.curses_window, general_bg, outline, *tuple_enemies)
        
    def set_stillstate(self):
        ########### gotta fix this
        return ([0 for i in range(20)], self.curses_window,general_bg, outline, *self.spritesheets_tuple())
    
    def user_update(self, user_input): #### this should also 
        if user_input == "escape":
            self.escape = True
            return
        #### Here, the user input must be in the format "attack_1", "attack_2".. etc
        if user_input[:-2] == "attack":
            damage = 5 # Placeholder. This can go through a random damage generator that's based on the player's base attack stat
            protag = self.creatures_dict["protag"]
            enemy = self.creatures_dict["Enemy_{0}".format(user_input[-1:])]
            enemy.hp -= damage
            self.set_new_sprites(protag, enemy)

    def zombie_update(self): ### NEEDS WORK. Should attack character based on enemy's basedmg
        #### Placeholder
        protag = self.creatures_dict["protag"]
        enemies = [creature for creature in self.creatures_dict.values() if creature.creature_type != "protag"]
        enemy = random.choice(enemies)
        protag.hp -= enemy.basedmg # should be modified so it's random to some degree
        print(protag.hp)
        self.set_new_sprites(enemy, protag)
        # self.refresh_sprites()
        #### FUNCTION TO UPDATE ANIMATION TUPLE HERE
     # (self,creature_number, backend_dict, creature_zlevel = 1, dx_change = 0, dy_change = 0)   
    def place_creatures(self):
        dx_change = 30
        dy_change = -4
        creature_number = 1
        counter = 1
        z = 6
        protag_level = 1 # placeholder
        # protag = creature(0, protag)
        # info = spritesheet(("placeholder",),14, zlevel = 100, frames = 6, dx = 2, dy = 14, infolist = ["protag", 0,1,50]) # This should be made in creatures, not here.
        self.creatures_dict["protag"] = creature(0, protag) # Protag dict
        self.enemies = (zombie, zombie, zombie_child) # how self.enemies should look like
        for i in self.enemies:
            dx_change += 10
            dy_change += 8
            counter += 1
            self.creatures_dict["enemy_{0}".format(creature_number)] = creature(creature_number, i, creature_zlevel, dx_change = dx_change, dy_change = dy_change)
            if counter == 4:
                counter = 1
                dx_change -= 10
                dy_change = -6
            z += 1
            creature_number += 1

# protag = {
    # "name" : "Protag",
    # "description" : "DESCRIPTION",
    # "health" : 200,
    # "base_damage" : 20,
    # "crit_chance" : 0.3,
    # "crit_multiplier" : 2
 #}
# zombie = {
    # "name" : "zombie",
    # "description" : "DESCRIPTION",
    # "health" : 50,
    # "base_damage" : 10,
    # "crit_chance" : 0.3,
    # "crit_multiplier" : 2
# }    
    # def place_creatures(self):
        # dx_change = 30
        # dy_change = -4
        # name_counter = 1
        # enemy_number = 1
        # counter = 1 # to keep track of when to change dx, dy to different values 
        # z = 6       
        # protag_level = 1 # placeholder
        ### Could use a rudimentary leveling up system for the protag
        ### such as basic attack and hp going up by a given percentage upon level up
        ### creature(path, creature_type, creature_name, creature_level, hp, creature_zlevel, dx_change, dy_change)
        # protag = creature(("placeholder",),0,"protag", 13, protag_level, 50, 20, 2, 9) #level can be replaced with protag level variable
        # info = spritesheet(("placeholder",),14, zlevel = 100, frames = 6, dx = 2, dy = 14, infolist = ["protag", 0,1,50]) ### Infolist is a placeholder here. Need to pull player stats from somewhere.
        # self.creatures_dict["protag"] = protag
        # for i in self.enemies:
            # hp = 25 #pull enemy HP from backend
            # dx_change += 10
            # dy_change += 8
            # counter += 1
            # print(self.enemies[name_counter-1][1])
            # enemy_level = self.enemies[name_counter-1][1] #grabs second item from tuple
            # enemy = creature(("placeholder",),enemy_number,enemy_type, 7, enemy_level,hp, z, dx_change, dy_change)
            # self.creatures_dict["Enemy_{0}".format(name_counter)] = enemy
            # info = spritesheet(("placeholder",),14, zlevel = z+0.1, frames = 6, dx = dx_change, dy = dy_change+5, infolist = i.grab_infolist)
            #infolist = [enemy_type, enemy_number,enemy_level,hp] # replaced, to delete
            # self.info_dict[enemy] = info
            # if counter == 4:
                # counter = 1
                # dx_change -= 10
                # dy_change = -6
            # z += 1
            # enemy_number += 1
            # name_counter += 1
    
    def spritesheets_tuple(self):
        # need everything as a tuple so I can unpack it
        spritesheets_to_add = [general_bg]
        for i in self.creatures_dict:
            spritesheets_to_add.append(self.creatures_dict[i].spritesheet)
            # print(self.creatures_dict[i], "THIS IS IT ")
            # print(self.info_dict)
            # spritesheets_to_add.append(self.info_dict[self.creatures_dict[i]].spritesheet) # NOT IMPLEMENTED YET
        for i in self.info_dict:
            spritesheets_to_add.append(self.info_dict[i])
        spritesheets_to_add = tuple(spritesheets_to_add)
        return spritesheets_to_add
        
        
    
# fight = initiate_combat(("zombie", 2), ("zombie", 1), ("zombie", 1))
# print(len(self.creatures_dict))