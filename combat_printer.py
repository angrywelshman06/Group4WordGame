from combat import *
# curses.initscr()
# curses_setcolors()

# zombie = {
    # "name" : "zombie",
    # "description" : "DESCRIPTION",
    # "health" : 50,
    # "base_damage" : 10,
    # "crit_chance" : 0.3,
    # "crit_multiplier" : 2
# }

# zombie_child = {
    # "name" : "zombie child",
    # "description" : "DESCRIPTION",
    # "health" : 15,
    # "base_damage" : 5,
    # "crit_chance" : 0.1,
    # "crit_multiplier" : 4
# }

# zombie_dog = {
    # "name" : "zombie dog",
    # "description" : "DESCRIPTION",
    # "health" : 25,
    # "base_damage" : 8,
    # "crit_chance" : 0.6,
    # "crit_multiplier" : 2
# }

# zombie_strong = {
    # "name" : "strong zombie",
    # "description" : "DESCRIPTION",
    # "health" : 65,
    # "base_damage" : 15,
    # "crit_chance" : 0.2,
    # "crit_multiplier" : 2
# }

# protagonist = {
    # "name" : "protag",
    # "description" : "DESCRIPTION",
    # "health" : 50,
    # "base_damage" : 10,
    # "crit_chance" : 0.3,
    # "crit_multiplier" : 2,
# }

class creature():
        
    def __init__(self,creature_number, backend_dict, creature_zlevel = 1, dx_change = 1, dy_change = 1, infosheet = False):
        self.creature_number = creature_number
        self.name = backend_dict["name"]
        self.description = backend_dict["description"]
        self.level = 1 # should get combat working first 
        self.health = backend_dict["health"]
        self.damage = backend_dict["base_damage"] * (1 + 0.4 * (self.level - 1))
        self.crit_chance = backend_dict["crit_chance"]
        self.crit_multiplier = backend_dict["crit_multiplier"]
        self.user_input = "" # placeholder

        self.path = self.grab_path()
        self.zlevel = creature_zlevel # Priority it takes when printing the animation
        self.color = 11
        if self.name != "protag":
            self.color = 7
        self.dx_change = dx_change
        self.dy_change = dy_change
        self.frames = 6
        self.spritesheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change)
        # self.info = spritesheet(self.path,self.color, zlevel = 100, frames = 6, dx = self.dx_change, dy = self.dy_change) # increment dx dy to change position
        # self.info.transform_to_info(self.grab_infolist())
        self.infosheet = infosheet
        if self.infosheet != False:
            self.infosheet = spritesheet(self.path, self.color, zlevel = self.zlevel, frames = self.frames, dx = self.dx_change, dy = self.dy_change, infolist = self.grab_infolist())
        # print(self.info.frameslist[0])
        self.frameslist = self.spritesheet.frameslist
        self.frames_attack = self.spritesheet.frameslist
        self.frames_standstill = self.spritesheet.frameslist[0]
    
    def get_damage(self, crit_bool : bool):
        if crit_bool:
            return self.damage * self.crit_multiplier
        return self.damage
    
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
class initiate_combat_printer():
    def __init__(self, curses_window, enemies):
        self.creatures_dict = {} ### creatures in the current fight stored here. Protagonist is the first key "protag"
        self.info_dict = {} # dictionary to store info enemy : info spritesheet pair
        # self.enemies = enemies 
        self.enemies = (zombie, zombie_strong, zombie_child, zombie_strong, zombie_dog) # GET ENEMIES FROM CURRENT ROOM HERE
        self.curses_window = curses_window
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
    
    def freeze_frames(self, i): # Extends the first frame to the other frames in the same spritesheet
        firstframe = self.creatures_dict[i].spritesheet.frameslist[0]
        for index, value in enumerate(self.creatures_dict[i].spritesheet.frameslist):
            self.creatures_dict[i].spritesheet.frameslist[index] = firstframe 
            
    def set_new_sprites(self, attacker, attacked): # Makes changes to sprites and alters self.animation, the tuple which will be used when calling run_animation_curses
        self.refresh_sprites()
        if attacker.name == "protag":
            for i in self.creatures_dict:
                if i != "protag":
                    self.freeze_frames(i) 
        
        if attacker.name != "protag":
            firstframe = self.creatures_dict["protag"].spritesheet.frameslist[0]
            for index, value in enumerate(self.creatures_dict["protag"].spritesheet.frameslist):
                self.creatures_dict["protag"].spritesheet.frameslist[index] = firstframe  
            for i in self.creatures_dict:
                if self.creatures_dict[i] != attacker:
                    self.freeze_frames(i)
            
        self.blank_out_frames(attacked.spritesheet.frameslist)
                        
        tuple_creatures = tuple([self.creatures_dict[i] for i in self.creatures_dict])
        tuple_info = tuple([self.info_dict[i] for i in self.info_dict])
        self.curses_window.clear()
        self.animation = (self.curses_window, general_bg, outline, *tuple_creatures)
        
    def set_stillstate(self):
        ######### the mythical list of 0's
        return ([0 for i in range(20)], self.curses_window,general_bg, outline, *self.spritesheets_tuple())
    
    def user_update(self, user_input): #### this should also 
        #### Here, the user input must be in the format "attack_1", "attack_2".. etc
        if user_input[:-2] == "attack":
            damage = 5 # Placeholder. This can go through a random damage generator that's based on the player's base attack stat
            protag = self.creatures_dict["protag"]
            enemy = self.creatures_dict["creature_{0}".format(user_input[-1:])]
            self.set_new_sprites(protag, enemy)
        else:
            pass

    def zombie_update(self): ### NEEDS WORK. Should attack character based on enemy's basedmg
        #### Placeholder
        protag = self.creatures_dict["protag"]
        enemies = [creature for creature in self.creatures_dict.values() if creature.name != "protag"]
        enemy = random.choice(enemies)
        self.set_new_sprites(enemy, protag)
        # self.refresh_sprites()
        #### FUNCTION TO UPDATE ANIMATION TUPLE HERE
     # (self,creature_number, backend_dict, creature_zlevel = 1, dx_change = 0, dy_change = 0)
     
    def place_creatures(self):
        dx_change = 11
        dy_change = -9
        creature_number = 1
        counter = 1
        z = 6
        protag_level = 1 # placeholder
        # protag = creature(0, protagonist)
        self.creatures_dict["protag"] = creature(0, protagonist,creature_zlevel = 5, dx_change = 4, dy_change = 6) # Protag dict
        # self.info_dict["protag"] = creature(0, protagonist,creature_zlevel = 5.1, dx_change = 4, dy_change = 6, infosheet = True).infosheet
        for i in self.enemies:
            dx_change += 10
            dy_change += 9
            counter += 1
            # (self,creature_number, backend_dict, creature_zlevel = 1, dx_change = 0, dy_change = 0)
            self.creatures_dict["creature_{0}".format(creature_number)] = creature(creature_number, i, creature_zlevel = z, dx_change = dx_change, dy_change = dy_change)
            self.info_dict["creature_{0}".format(creature_number)] = creature(creature_number, i, creature_zlevel = z+0.1, dx_change = dx_change+15, dy_change = dy_change+9, infosheet = True).infosheet
            if counter == 4:
                counter = 1
                dx_change -= 1
                dy_change = -6
            z += 1
            creature_number += 1

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
