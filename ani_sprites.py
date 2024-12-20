import os
import curses


""" 
Spritesheets are objects that contain the data to be used when printing animations or still shots on the screen. 
zlevel - When two or more ASCII characters share the same position on the screen, the highest zlevel determines which character gets printed.

frames - The amount of text files read within a spritesheet. Used for determining the spritesheet with the highest amount of frames, 
then duplicates the final frame of every other spritesheet to the highest amount.

dx, dy - Allows to move the ascii frames to a different position on the screen

infolist - By default 0. If not, the values contained within this list will be used to transform every frame in frameslist according to the 
"""
class spritesheet():
    def __init__(self, path, color, zlevel = 0, frames = 0, dx = 0, dy = 0, infolist = 0):
        self.path = path # folder path in ./spritesheets/
        self.color = color # curses color pair
        self.zlevel = zlevel # printing priority
        self.frames = frames # number of text files to read
        self.dx = dx # x change
        self.dy = dy # y change
        self.frameslist = self.gather_framelist() # list containing every frame. The standard dimensions for most text files read should be col 100 x ln 33
        self.infolist = infolist ### Used for combat. Should be a list containing [creature type, number (in battle), level, hp].
        if infolist != 0:
            # if "protag" not in self.path: This should work but it doesn't
                # self.color = 8
            self.frameslist = self.transform_to_info(infolist) ### Tansforms every spritesheet to the details of a creature by using the infolist.
            
        ## dy and dx are meant to be used when a spritesheet contains text files of a much smaller dimension than the standard.       
        if (self.dx != 0) or (self.dy != 0):
            self.frameslist = self.extend_frames() ## Adds empty space around every item of the frameslist (according to dx and dy) to fit the standard of 100x33. 
        
    def gather_framelist(self): # Gathers every textfile in the given path and appends it to frameslist.
        frameslist = []
        for frame in range(1,self.frames+1):
            # path = os.path.join("modularanimation","spritesheets","{0}".format(self.path), "txt", "ascii-art ({0}).txt".format(frame)) ## os.path.join works regardless of OS
            path = os.path.join("spritesheets",*self.path, "ascii-art ({0}).txt".format(frame)) #if ran directly from animator.py
            file = open(path, "r", encoding="utf-8") # utf-8 ecoding to allow extended ascii art
            frameslist.append(file.read())
            file.close()
        return frameslist

    # Responsible for updating the graphical representation of the stats on the screen. [creature type, number (in battle), level, hp]
    def transform_to_info(self, infolist): # Uses infolist
        name = infolist[0]
        number = infolist[1]
        level = infolist[2]
        hp = infolist[3]
        newframeslist = []
        
        for index,value in enumerate(self.frameslist): # Goes through every item in frameslist
            newframe = self.frameslist[index].splitlines() # Splits every line in the current index of frameslist. The resulting split is then appended as a list to newframe.
            
            for index, value in enumerate(newframe): # Loops through every item of newframe.
                newframe[index] = " "*len(newframe[index]) # Turns every character of the item into empty space. Reasoning behind this is to maintain dimensions.
            
            for index,line in enumerate(newframe): # Goes through newframe again and assigns the info from infolist arbitrarily to index 2 and 3.
                if index == 2:
                    newframe[index] = name +" No."+str(number)+line[len(name+" No."+str(number)):] ### Adds info whilst maintaining the lenght of the item.
                if index == 3:
                    newframe[index] = "Lv"+str(level)+" HP:"+str(hp)+line[index][len("Lv"+str(level)+" HP:"+str(hp)):] ### Adds info whilst maintaining the lenght of the item.
                else:
                    pass
            
            newframe = "\n".join(newframe) # joins back the items of newframe into one frame
            newframeslist.append(newframe) # appends the new frame to newframeslist
        return newframeslist # Returns the altered frames list

    """ Adds empty space around every item of the frameslist (according to dx and dy) to fit the standard of 100x33. """
    def extend_frames(self):
        newframeslist = []
        for index, value in enumerate(self.frameslist): # Goes through every item in frameslist
            newframe = self.frameslist[index].splitlines() # Splits every line in the current index of frameslist. The resulting split is then appended as a list to newframe.
            
            for index, value in enumerate(newframe): # Loops through every item of newframe.
                if len(newframe[index]) < 100: 
                    newframe[index] += " "*(100-len(newframe[index])) #fills newframe to the standard x dimension
                    
            if len(newframe) < 34:
                for i in range(len(newframe), 34):
                    newframe.append(" "*100) # fills newframe to the standard y dimension
                    
            for i in range(self.dy): # DY adjustment
                newframe.insert(0,(" "*100)) # Adds blank space at index 0
                del newframe[-1] # Deletes the last item in newframe list
                
            if self.dx != 0: # DX adjustment
                for index, value in enumerate(newframe): # loops through every item of newframe
                    newframe[index] = (" "*(self.dx) + newframe[index])[:-(self.dx)] # pushes every item towards the right whilst maintaining the standard x dimension of 100.
                    
            newframe = "\n".join(newframe) # joins back the frames
            newframeslist.append(newframe)
            
        return newframeslist # Returns the altered frames list

###### SPRITESHEETS ###########
""" After the spritesheets are declared, they are then assigned to a tuple which is used in run_animation_curses and print_stillshot_curses."""

###### Multi-purpose sprites
general_bg = spritesheet(("background",), 3, zlevel = 0.05, frames = 1)
general_bg2 = spritesheet(("background2",),23, zlevel = 0.1, frames = 1)
outline = spritesheet(("outline1",), 9, zlevel = 500, frames = 1)
randomobj = spritesheet(("randomobj",), 8, zlevel = 134, frames = 1, dx = 55, dy = 10)
red_skyline = spritesheet(("skylines", "red"), 8, zlevel = 0.01, frames = 1)

###### Intro part 1
building1 = spritesheet(("intro_1","building1"), 10, zlevel = 7, frames = 95)
heli = spritesheet(("intro_1","heli"), 9, zlevel = 5, frames = 95)
skyscraper = spritesheet(("intro_1","skyscraper"), 10, zlevel = 4, frames = 95)
fire3 = spritesheet(("intro_1","fire3"), 6, zlevel = 3, frames = 95)
fire2 = spritesheet(("intro_1","fire2"), 6, zlevel = 8, frames = 95)
fire = spritesheet(("intro_1","fire"), 6, zlevel = 6, frames = 95)
citybg = spritesheet(("intro_1","citybg"), 10, zlevel = 2, frames = 95)
pulse = spritesheet(("intro_1","pulse"), 8, zlevel = 1, frames = 95)
climbers = spritesheet(("intro_1","climbers"), 7, zlevel = 10, frames = 95)
dudeontop = spritesheet(("intro_1","dudeontop"), 3, zlevel = 11, frames = 95)
moon = spritesheet(("intro_1","moon"), 8, zlevel = 0.5, frames = 1)
#### Unpack this in run_animation_curses. Should look like this: run_animation_curses([insert curses window here],*intro_1) 
intro_1 = (fire,fire2,fire3,skyscraper,building1,heli,citybg,pulse, climbers, dudeontop, moon, outline)

##### Intro part 2 
intro_male_eyes = spritesheet(("intro_2","intro_male_eyes"), 1, zlevel = 5, frames = 38)
intro_male_body = spritesheet(("intro_2","intro_male_body"), 11, zlevel = 3, frames = 1)
intro_male_hair = spritesheet(("intro_2","intro_male_hair"), 2, zlevel = 10, frames = 1)
bed = spritesheet(("intro_2","bed"), 5, zlevel = 0.1, frames = 1)
pillow = spritesheet(("intro_2","pillow"), 12, zlevel = 0.2, frames = 1)
####
intro_2 = (intro_male_body,intro_male_hair,intro_male_eyes, bed, pillow, general_bg,outline)

##### Tutorial Room
bed = spritesheet(("room_tutorial", "bed"), 5, zlevel = 12, frames = 1)
bg = spritesheet(("room_tutorial", "bg"), 3, zlevel = 1, frames = 1)
cobweb = spritesheet(("room_tutorial", "cobweb"), 1, zlevel = 10, frames = 1)
misc = spritesheet(("room_tutorial", "misc"), 1, zlevel = 20, frames = 1)
scratches = spritesheet(("room_tutorial", "scratches"), 1, zlevel = 11, frames = 1)
wood = spritesheet(("room_tutorial", "wood"), 2, zlevel = 15, frames = 1)
#### Unpack in print_stillshot_curses. Should look like print_stillshot_curses(display_win, *room_tutorial).
room_tutorial = (outline,bed, bg, cobweb, misc, scratches, wood)

##### Cutscene 1
zombie_1 = spritesheet(("cutscene_1", "zombie"), 7, zlevel = 12, frames = 58)
body_1 = spritesheet(("cutscene_1", "body_1"), 11, zlevel = 3, frames = 1)
red_elements_1 = spritesheet(("cutscene_1", "red"), 8, zlevel = 15, frames = 58)
red_elements_2 = spritesheet(("cutscene_1", "red2"), 8, zlevel = 4, frames = 1)
cutscene_1 = (outline,zombie_1, red_elements_1, general_bg, body_1, red_elements_2)

##### Combat placeholders
holder1 = spritesheet(("placeholder",), 8, zlevel = 4, frames = 6, dx = 22, dy = 2)
# holder2 = spritesheet(("placeholder",), 7, zlevel = 5, frames = 6, dx = 24, dy = 5)
# holder3 = spritesheet(("placeholder",), 7, zlevel = 4, frames = 6, dx = 27, dy = 8)

##### Bathroom
curtain = spritesheet(("room_bathroom", "curtain"), 15, zlevel = 12, frames = 1)
floor = spritesheet(("room_bathroom", "floor"), 18, zlevel = 1, frames = 1)
grafitti = spritesheet(("room_bathroom", "grafitti"), 19, zlevel = 55, frames = 1)
mirror = spritesheet(("room_bathroom", "mirror"), 16, zlevel = 4, frames = 1)
toiletpaper = spritesheet(("room_bathroom", "toiletpaper"), 20, zlevel = 5, frames = 1)
toiletsink = spritesheet(("room_bathroom", "toiletsink"), 20, zlevel = 6, frames = 1)
wall = spritesheet(("room_bathroom", "wall"), 17, zlevel = 2, frames = 1)
###
room_bathroom = (outline,curtain, floor, grafitti, mirror, toiletpaper, toiletsink, wall)

##### Kitchen
cobweb_2 = spritesheet(("room_kitchen", "cobweb_2"), 1, zlevel = 10, frames = 1)
floorwall = spritesheet(("room_kitchen", "floorwall"), 17, zlevel = 1, frames = 1)
grime = spritesheet(("room_kitchen", "grime"), 7, zlevel = 7, frames = 1)
metal = spritesheet(("room_kitchen", "metal"), 20, zlevel = 3, frames = 1)
wood = spritesheet(("room_kitchen", "wood"), 2, zlevel = 2, frames = 1)
###
room_kitchen = (outline,cobweb_2, floorwall, grime, metal, wood)

##### Train station
floor_ts = spritesheet(("room_trainstation", "floor_ts"), 20, zlevel = 1, frames = 1)
grass = spritesheet(("room_trainstation", "grass"), 7, zlevel = 7, frames = 1)
luggage = spritesheet(("room_trainstation", "luggage"), 15, zlevel = 8, frames = 1)
rails = spritesheet(("room_trainstation", "rails"), 20, zlevel = 3, frames = 1)
train_green = spritesheet(("room_trainstation", "train_green"), 11, zlevel = 5, frames = 1)
train_orange = spritesheet(("room_trainstation", "train_orange"), 16, zlevel = 4, frames = 1)
train_silver = spritesheet(("room_trainstation", "train_silver"), 1, zlevel = 6, frames = 1)
wood_ts = spritesheet(("room_trainstation", "wood_ts"), 2, zlevel = 2, frames = 1)
###
room_trainstation = (outline,red_skyline,floor_ts, grass, luggage, rails, train_green, train_orange, train_silver, wood_ts)

##### Gym
blood_gym = spritesheet(("room_gym", "blood_gym"), 8, zlevel = 10, frames = 1)
floor_gym = spritesheet(("room_gym", "floor_gym"), 3, zlevel = 2, frames = 1)
wall_gym = spritesheet(("room_gym", "wall_gym"), 2, zlevel = 3, frames = 1)
weights_gym = spritesheet(("room_gym", "weights"), 20, zlevel = 9, frames = 1)
###
room_gym = (outline,blood_gym, floor_gym, wall_gym, weights_gym, red_skyline)

##### Firestation
floor_fst = spritesheet(("room_firestation", "floor_fst"), 3, zlevel = 1, frames = 1)
garage_fst = spritesheet(("room_firestation", "garage_fst"), 20, zlevel = 2, frames = 1)
misc_fst = spritesheet(("room_firestation", "misc_fst"), 16, zlevel = 4, frames = 1)
truck1_fst = spritesheet(("room_firestation", "truck1_fst"), 16, zlevel = 5, frames = 1)
truck2_fst = spritesheet(("room_firestation", "truck2_fst"), 8, zlevel = 6, frames = 1)
wall_fst = spritesheet(("room_firestation", "wall_fst"), 17, zlevel = 3, frames = 1)
###
room_firestation = (outline,floor_fst, garage_fst, misc_fst, truck1_fst, truck2_fst, wall_fst)

##### Fastfood
counter_ffd = spritesheet(("room_fastfood", "counter_ffd"), 17, zlevel = 2, frames = 1)
floor_ffd = spritesheet(("room_fastfood", "floor_ffd"), 21, zlevel = 1, frames = 1)
misc_ffd = spritesheet(("room_fastfood", "misc_ffd"), 15, zlevel = 6, frames = 1)
screens_ffd = spritesheet(("room_fastfood", "screens_ffd"), 3, zlevel = 4, frames = 1)
tills_ffd = spritesheet(("room_fastfood", "tills_ffd"), 20, zlevel = 3, frames = 1)
wood_ffd = spritesheet(("room_fastfood", "wood_ffd"), 2, zlevel = 5, frames = 1)
logo_ffd = spritesheet(("room_fastfood", "logo_ffd"), 13, zlevel = 9, frames = 1)
###
room_fastfood = (outline,counter_ffd, floor_ffd, misc_ffd, screens_ffd, tills_ffd, wood_ffd, red_skyline, logo_ffd)

##### Park
bushes_prk = spritesheet(("room_park", "bushes_prk"), 7, zlevel = 1, frames = 1)
cobweb_prk = spritesheet(("room_park", "cobweb_prk"), 1, zlevel = 5, frames = 1)
metal_prk = spritesheet(("room_park", "metal_prk"), 20, zlevel = 2, frames = 1)
water_prk = spritesheet(("room_park", "water_prk"), 8, zlevel = 4, frames = 1)
wood_prk = spritesheet(("room_park", "wood_prk"), 2, zlevel = 3, frames = 1)
####
room_park = (outline,bushes_prk, cobweb_prk, metal_prk, water_prk, wood_prk, general_bg)

##### Police Station
badge_pol = spritesheet(("room_policestation", "badge_pol"), 21, zlevel = 5, frames = 1)
insidecell_pol = spritesheet(("room_policestation", "insidecell_pol"), 15, zlevel = 1.9, frames = 1)
papers_pol = spritesheet(("room_policestation", "papers_pol"), 16, zlevel = 6, frames = 1)
wallfloor_pol = spritesheet(("room_policestation", "wallfloor_pol"), 17, zlevel = 1, frames = 1)
wood_pol = spritesheet(("room_policestation", "wood_pol"), 2, zlevel = 4, frames = 1)
metal_pol = spritesheet(("room_policestation", "metal_pol"), 20, zlevel = 2, frames = 1)
radio_pol = spritesheet(("room_policestation", "radio_pol"), 20, zlevel = 10, frames = 1)
####
room_policestation = (outline,badge_pol, insidecell_pol, papers_pol, wallfloor_pol, wood_pol, metal_pol,radio_pol)

##### Cinema
blood_cin = spritesheet(("room_cinema", "blood_cin"),8, zlevel = 6, frames = 1)
chairs_cin = spritesheet(("room_cinema", "chairs_cin"), 10, zlevel = 2, frames = 1)
popcorn_cin = spritesheet(("room_cinema", "popcorn_cin"), 1, zlevel = 10, frames = 1)
pocornbox_cin = spritesheet(("room_cinema", "pocornbox_cin"), 11, zlevel = 5, frames = 1)
screen_cin = spritesheet(("room_cinema", "screen_cin"), 20, zlevel = 3, frames = 1)
wallfloor_cin = spritesheet(("room_cinema", "wallfloor_cin"), 15, zlevel = 1, frames = 1)
####
room_cinema = (outline,blood_cin, chairs_cin, pocornbox_cin, popcorn_cin, screen_cin, wallfloor_cin)

#### Shopping centre
floorwall_shc = spritesheet(("room_shoppingcentre", "floorwall_shc"),3, zlevel = 1, frames = 1)
glass_shc = spritesheet(("room_shoppingcentre", "glass_shc"),16, zlevel = 2, frames = 1)
greenery_shc = spritesheet(("room_shoppingcentre", "greenery_shc"),7, zlevel = 6, frames = 1)
sign1_shc = spritesheet(("room_shoppingcentre", "sign1_shc"),11, zlevel = 3, frames = 1)
sign2_shc = spritesheet(("room_shoppingcentre", "sign2_shc"),4, zlevel = 4, frames = 1)
wood_shc = spritesheet(("room_shoppingcentre", "wood_shc"),2, zlevel = 5, frames = 1)
####
room_shoppingcentre = (outline,floorwall_shc, glass_shc, greenery_shc, sign1_shc, sign2_shc, wood_shc)


#### Graveyard
blood_grv = spritesheet(("room_graveyard", "blood_grv"),8, zlevel = 4, frames = 1)
headstones_grv = spritesheet(("room_graveyard", "headstones_grv"),20, zlevel = 2, frames = 1)
path_grv = spritesheet(("room_graveyard", "path_grv"),21, zlevel = 1, frames = 1)
wood_grv = spritesheet(("room_graveyard", "wood_grv"),2, zlevel = 3, frames = 1)
####
room_graveyard = (outline,blood_grv,headstones_grv,path_grv, wood_grv,general_bg)

#### Supermarket
cart_smrkt = spritesheet(("room_supermarket", "cart_smrkt"),20, zlevel = 6, frames = 1)
checkouts_smrkt = spritesheet(("room_supermarket", "checkouts_smrkt"),20, zlevel = 5, frames = 1)
floorwall_smrkt = spritesheet(("room_supermarket", "floorwall_smrkt"),3, zlevel = 1, frames = 1)
items1_smrkt = spritesheet(("room_supermarket", "items1_smrkt"),7, zlevel = 3, frames = 1)
items2_smrkt = spritesheet(("room_supermarket", "items2_smrkt"),8, zlevel = 4, frames = 1)
shelves_smrkt = spritesheet(("room_supermarket", "shelves_smrkt"),2, zlevel = 2, frames = 1)
####
room_supermarket = (outline,cart_smrkt, checkouts_smrkt, floorwall_smrkt, items1_smrkt, items2_smrkt, shelves_smrkt, red_skyline)


#### Pharmacy
blood_phar = spritesheet(("room_pharmacy", "blood_phar"),8, zlevel = 5, frames = 1)
floorwall_phar = spritesheet(("room_pharmacy", "floorwall_phar"),3, zlevel = 1, frames = 1)
glass_phar = spritesheet(("room_pharmacy", "glass_phar"),16, zlevel = 4, frames = 1)
symbol_phar = spritesheet(("room_pharmacy", "symbol_phar"),4, zlevel = 3, frames = 1)
wood_phar = spritesheet(("room_pharmacy", "wood_phar"),2, zlevel = 2, frames = 1)
####
room_pharmacy = (outline,blood_phar,floorwall_phar,glass_phar,symbol_phar,wood_phar,red_skyline)

#### Hospital
blood_hsp = spritesheet(("room_hospital", "blood_hsp"),8, zlevel = 4, frames = 1)
floor_hsp = spritesheet(("room_hospital", "floor_hsp"),16, zlevel = 1, frames = 1)
gurneys_hsp = spritesheet(("room_hospital", "gurneys_hsp"),11, zlevel = 3, frames = 1)
signs_hsp = spritesheet(("room_hospital", "signs_hsp"),18, zlevel = 5, frames = 1)
wall_hsp = spritesheet(("room_hospital", "wall_hsp"),16, zlevel = 2, frames = 1)
item_hsp = spritesheet(("room_hospital", "item_hsp"),3, zlevel = 10, frames = 1)
####
room_hospital = (outline,blood_hsp, floor_hsp, gurneys_hsp, signs_hsp, wall_hsp,item_hsp)

#### Convenience store
blood_cnv = spritesheet(("room_conveniencestore", "blood_cnv"),8, zlevel = 5, frames = 1)
counter_cnv = spritesheet(("room_conveniencestore", "counter_cnv"),20, zlevel = 3, frames = 1)
floorwall_cnv = spritesheet(("room_conveniencestore", "floorwall_cnv"),15, zlevel = 1, frames = 1)
item_cnv = spritesheet(("room_conveniencestore", "item_cnv"),18, zlevel = 4, frames = 1)
shelf_cnv = spritesheet(("room_conveniencestore", "shelf_cnv"),2, zlevel = 2, frames = 1)
cobweb_cnv = spritesheet(("room_conveniencestore", "cobweb_cnv"),16, zlevel = 10, frames = 1)
#####
room_convenience = (outline,blood_cnv, counter_cnv, floorwall_cnv, item_cnv, shelf_cnv, red_skyline, cobweb_cnv)

#### Library
blood_lib = spritesheet(("room_library", "blood_lib"),8, zlevel = 6, frames = 1)
books1_lib = spritesheet(("room_library", "books1_lib"),4, zlevel = 4, frames = 1)
books2_lib = spritesheet(("room_library", "books2_lib"),15, zlevel = 5, frames = 1)
carpet_lib = spritesheet(("room_library", "carpet_lib"),11, zlevel = 2, frames = 1)
floorwall_lib = spritesheet(("room_library", "floorwall_lib"),3, zlevel = 1, frames = 1)
wood_lib = spritesheet(("room_library", "wood_lib"),2, zlevel = 3, frames = 1)
#####
room_library = (outline,blood_lib, books1_lib, books2_lib, carpet_lib, floorwall_lib, wood_lib)

#### Petrol station
building_ptr = spritesheet(("room_petrol", "building_ptr"),3, zlevel = 2, frames = 1)
floor_ptr = spritesheet(("room_petrol", "floor_ptr"),3, zlevel = 1, frames = 1)
glass_ptr = spritesheet(("room_petrol", "glass_ptr"),16, zlevel = 4, frames = 1)
pillar_ptr = spritesheet(("room_petrol", "pillar_ptr"),2, zlevel = 5, frames = 1)
pump_ptr = spritesheet(("room_petrol", "pump_ptr"),20, zlevel = 6, frames = 1)
sign_ptr = spritesheet(("room_petrol", "sign_ptr"),7, zlevel = 3, frames = 1)
car_ptr = spritesheet(("room_petrol", "car_ptr"),16, zlevel = 50, frames = 1)
#####
room_petrol = (outline,building_ptr,floor_ptr,glass_ptr,pillar_ptr,pump_ptr,sign_ptr,red_skyline,car_ptr)

#### River
bottle_rvr = spritesheet(("room_river", "bottle_rvr"),16, zlevel = 5, frames = 1)
ground_rvr = spritesheet(("room_river", "ground_rvr"),4, zlevel = 2, frames = 1)
path_rvr = spritesheet(("room_river", "path_rvr"),21, zlevel = 3, frames = 1)
river_rvr = spritesheet(("room_river", "river_rvr"),11, zlevel = 1, frames = 1)
wood_rvr = spritesheet(("room_river", "wood_rvr"),2, zlevel = 4, frames = 1)
#####
room_river = (outline,bottle_rvr,ground_rvr,path_rvr,river_rvr,wood_rvr, red_skyline)

#### Armored van
blood_van = spritesheet(("room_armoredvan", "blood_van"),8, zlevel = 4, frames = 1)
floorwall_van = spritesheet(("room_armoredvan", "floorwall_van"),3, zlevel = 1, frames = 1)
glass_van = spritesheet(("room_armoredvan", "glass_van"),16, zlevel = 3, frames = 1)
van_van = spritesheet(("room_armoredvan", "van_van"),5, zlevel = 2, frames = 1)
####
room_armoredvan = (outline,blood_van, floorwall_van, glass_van, van_van)

#### Pub
bottles_pub = spritesheet(("room_pub", "bottles_pub"),16, zlevel = 4, frames = 1)
cobweb_pub = spritesheet(("room_pub", "cobweb_pub"),16, zlevel = 5, frames = 1)
floorwall_pub = spritesheet(("room_pub", "floorwall_pub"),3, zlevel = 1, frames = 1)
shelf_pub = spritesheet(("room_pub", "shelf_pub"),5, zlevel = 2, frames = 1)
wood_pub = spritesheet(("room_pub", "wood_pub"),2, zlevel = 3, frames = 1)
####
room_pub = (outline,bottles_pub,cobweb_pub,floorwall_pub, shelf_pub,wood_pub)

#### Road
road_buildings = spritesheet(("room_road", "road_buildings"),3, zlevel = 2, frames = 1)
road_car1 = spritesheet(("room_road", "road_car1"),16, zlevel = 5, frames = 1)
road_car2 = spritesheet(("room_road", "road_car2"),4, zlevel = 4, frames = 1)
road_car3 = spritesheet(("room_road", "road_car3"),17, zlevel = 3, frames = 1)
road_street = spritesheet(("room_road", "road_street"),3, zlevel = 1, frames = 1)
####
room_road = (outline, road_buildings, road_car1, road_car2, road_car3, road_street, red_skyline)

#### Nursery
carpet_nrs = spritesheet(("room_nursery", "carpet_nrs"),15, zlevel = 4, frames = 1)
crib_nrs = spritesheet(("room_nursery", "crib_nrs"),16, zlevel = 5, frames = 1)
floor_nrs = spritesheet(("room_nursery", "floor_nrs"),21, zlevel = 1, frames = 1)
table_nrs = spritesheet(("room_nursery", "table_nrs"),2, zlevel = 6, frames = 1)
wall1_nrs = spritesheet(("room_nursery", "wall1_nrs"),15, zlevel = 3, frames = 1)
wall2_nrs = spritesheet(("room_nursery", "wall2_nrs"),4, zlevel = 2, frames = 1)
####
room_nursery = (outline, carpet_nrs, crib_nrs, floor_nrs, table_nrs, wall1_nrs, wall2_nrs)

#### Bank
coins_bnk = spritesheet(("room_bank", "coins_bnk"),21, zlevel = 3, frames = 1)
floorwall_bnk = spritesheet(("room_bank", "floorwall_bnk"),3, zlevel = 1, frames = 1)
metal_bnk = spritesheet(("room_bank", "metal_bnk"),20, zlevel = 20, frames = 1)
notes_bnk = spritesheet(("room_bank", "notes_bnk"),7, zlevel = 4, frames = 1)
wood_bnk = spritesheet(("room_bank", "wood_bnk"),2, zlevel = 5, frames = 1)
####
room_bank = (outline, coins_bnk, floorwall_bnk, metal_bnk, notes_bnk, wood_bnk)

#### Arcade
arrows_arc = spritesheet(("room_arcade", "arrows_arc"),8, zlevel = 7, frames = 1)
ddrmachine_arc = spritesheet(("room_arcade", "ddrmachine_arc"),17, zlevel = 6, frames = 1)
machines1_arc = spritesheet(("room_arcade", "machines1_arc"),17, zlevel = 5, frames = 1)
machines2_arc = spritesheet(("room_arcade", "machines2_arc"),4, zlevel = 3, frames = 1)
neon1_arc = spritesheet(("room_arcade", "neon1_arc"),15, zlevel = 4, frames = 1)
neon2_arc = spritesheet(("room_arcade", "neon2_arc"),7, zlevel = 2, frames = 1)
wallfloor_arc = spritesheet(("room_arcade", "wallfloor_arc"),3, zlevel = 1, frames = 1)
####
room_arcade = (outline,arrows_arc, ddrmachine_arc, machines1_arc, machines2_arc, neon1_arc, neon2_arc, wallfloor_arc)

#### Neighbourhood
blood_nhg = spritesheet(("room_neighbourhood", "blood_nhg"),8, zlevel = 6, frames = 1)
building_nhg = spritesheet(("room_neighbourhood", "building_nhg"),16, zlevel = 3, frames = 1)
glass_nhg = spritesheet(("room_neighbourhood", "glass_nhg"),16, zlevel = 5, frames = 1)
road_nhg = spritesheet(("room_neighbourhood", "road_nhg"),3, zlevel = 1, frames = 1)
roof_nhg = spritesheet(("room_neighbourhood", "roof_nhg"),2, zlevel = 4, frames = 1)
wall2_nhg = spritesheet(("room_neighbourhood", "wall2_nhg"),18, zlevel = 2, frames = 1)
####
room_neighbourhood = (outline,blood_nhg, building_nhg, road_nhg, roof_nhg, wall2_nhg)


##### Skyscraper
floor_sky = spritesheet(("room_skyscraper", "floor_sky"),3, zlevel = 1, frames = 1)
papers_sky = spritesheet(("room_skyscraper", "papers_sky"),16, zlevel = 4, frames = 1)
wall_sky = spritesheet(("room_skyscraper", "wall_sky"),17, zlevel = 3, frames = 1)
wood_sky = spritesheet(("room_skyscraper", "wood_sky"),2, zlevel = 2, frames = 1)
####
room_skyscraper = (outline, floor_sky,papers_sky,wall_sky, wood_sky, red_skyline)

#### Airport
floor_air = spritesheet(("room_airport", "floor_air"),3, zlevel = 2, frames = 1)
luggage1_air = spritesheet(("room_airport", "luggage1_air"),2, zlevel = 4, frames = 1)
luggage2_air = spritesheet(("room_airport", "luggage2_air"),15, zlevel = 5, frames = 1)
metal_air = spritesheet(("room_airport", "metal_air"),20, zlevel = 3, frames = 1)
plane_air = spritesheet(("room_airport", "plane_air"),16, zlevel = 1, frames = 1)
####
room_airport = (floor_air,luggage1_air,luggage2_air,metal_air,plane_air, red_skyline, outline)

#### Hairdressers
blood_hrd = spritesheet(("room_hairdressers", "blood_hrd"),8, zlevel = 4, frames = 1)
floor_hrd = spritesheet(("room_hairdressers", "floor_hrd"),3, zlevel = 1, frames = 1)
items_hrd = spritesheet(("room_hairdressers", "items_hrd"),15, zlevel = 5, frames = 1)
mirror_hrd = spritesheet(("room_hairdressers", "mirror_hrd"),16, zlevel = 2, frames = 1)
wood_hrd = spritesheet(("room_hairdressers", "wood_hrd"),2, zlevel = 3, frames = 1)
#####
room_hairdressers = (outline,blood_hrd, floor_hrd, items_hrd, mirror_hrd, wood_hrd)

#### Low-risk exit
barricade_lre = spritesheet(("room_lowriskescape", "barricade_lre"),16, zlevel = 1, frames = 1)
buildings_lre = spritesheet(("room_lowriskescape", "buildings_lre"),3, zlevel = 3, frames = 1)
floor_lre = spritesheet(("room_lowriskescape", "floor_lre"),3, zlevel = 2, frames = 1)
weeds_lre = spritesheet(("room_lowriskescape", "weeds_lre"),7, zlevel = 6, frames = 1)
white_lre = spritesheet(("room_lowriskescape", "white_lre"),16, zlevel = 5, frames = 1)
wood_lre = spritesheet(("room_lowriskescape", "wood_lre"),2, zlevel = 4, frames = 1)
#####
room_lowriskexit = (outline, barricade_lre, buildings_lre, floor_lre, weeds_lre, white_lre, wood_lre)

#### Restaurant
floor_rstr = spritesheet(("room_restaurant", "floor_rstr"),3, zlevel = 1, frames = 1)
glass_rstr = spritesheet(("room_restaurant", "glass_rstr"),16, zlevel = 2, frames = 1)
grime_rstr = spritesheet(("room_restaurant", "grime_rstr"),7, zlevel = 4, frames = 1)
wood_rstr = spritesheet(("room_restaurant", "wood_rstr"),2, zlevel = 3, frames = 1)
#####
room_restaurant = (outline, floor_rstr, glass_rstr, grime_rstr, wood_rstr)

#### Camp
blood_camp = spritesheet(("room_camp", "blood_camp"),8, zlevel = 5, frames = 1)
floor_camp = spritesheet(("room_camp", "floor_camp"),3, zlevel = 1, frames = 1)
items_camp = spritesheet(("room_camp", "items_camp"),16, zlevel = 3, frames =1)
sleepingbags_camp = spritesheet(("room_camp", "sleepingbags_camp"),21, zlevel = 4, frames = 1)
tent_camp = spritesheet(("room_camp", "tent_camp"),11, zlevel = 2, frames = 1)
####
room_camp = (outline, blood_camp, floor_camp, items_camp, sleepingbags_camp, tent_camp)

#### Cutscene death 1
blood_csd1 = spritesheet(("cutscene_death_1", "blood_csd1"),8, zlevel = 0.1, frames = 33)
mc_csd1 = spritesheet(("cutscene_death_1", "mc_csd1"),22, zlevel = 2, frames = 33)
zombie1_csd1 = spritesheet(("cutscene_death_1", "zombie1_csd1"),7, zlevel = 3, frames = 33)
zombie2_csd1 = spritesheet(("cutscene_death_1", "zombie2_csd1"),7, zlevel = 1, frames = 33)
#####
cutscene_death_1 = (blood_csd1, mc_csd1, zombie1_csd1, zombie2_csd1, general_bg,outline)

#### Ending: Explosion
bg_exploend = spritesheet(("ending_explosion", "bg_exploend"),4, zlevel = 1, frames = 55)
c4_exploend = spritesheet(("ending_explosion", "c4_exploend"),50, zlevel = 3, frames = 15)
fire_exploend = spritesheet(("ending_explosion", "fire_exploend"),8, zlevel = 4, frames = 29)
mc_exploend = spritesheet(("ending_explosion", "mc_exploend"),22, zlevel = 5, frames = 55)
wall_exploend = spritesheet(("ending_explosion", "wall_exploend"),3, zlevel = 2, frames = 55)#
#####
ending_explosion = (outline,bg_exploend, c4_exploend, fire_exploend, mc_exploend, wall_exploend)

#### Ending: Rope escape
bg_ropeend = spritesheet(("ending_rope", "bg_ropeend"),4, zlevel = 1, frames = 62)
mc_ropeend = spritesheet(("ending_rope", "mc_ropeend"),22, zlevel = 3, frames = 23)
mc2_ropeend = spritesheet(("ending_rope", "mc2_ropeend"),22, zlevel = 5, frames = 62)
rope_ropeend = spritesheet(("ending_rope", "rope_ropeend"),21, zlevel = 4, frames = 62)
wall_ropeend = spritesheet(("ending_rope", "wall_ropeend"),3, zlevel = 2, frames = 62)
#####
ending_rope = (outline, bg_ropeend, mc_ropeend, mc2_ropeend, rope_ropeend, wall_ropeend)

#### Ending: Boat
bg1_endboat = spritesheet(("ending_boat", "bg1_endboat"),8, zlevel = 0.2, frames = 50)
bg2_endboat = spritesheet(("ending_boat", "bg2_endboat"),17, zlevel = 0.1, frames = 1)
boat_endboat = spritesheet(("ending_boat", "boat_endboat"),16, zlevel = 7, frames = 50)
building1_endboat = spritesheet(("ending_boat", "building1_endboat"),3, zlevel = 5, frames = 50)
building2_endboat = spritesheet(("ending_boat", "building2_endboat"),3, zlevel = 6, frames = 50)
mc_endboat = spritesheet(("ending_boat", "mc_endboat"),22, zlevel = 8, frames = 50)
ocean_endboat = spritesheet(("ending_boat", "ocean_endboat"),18, zlevel = 4, frames = 1)
sun_endboat = spritesheet(("ending_boat", "sun_endboat"),21, zlevel = 0.3, frames = 50)
#####
ending_boat = (outline, bg1_endboat, bg2_endboat, boat_endboat, building1_endboat, building2_endboat, mc_endboat, ocean_endboat, sun_endboat)

#### Ending: Car
car_endcar = spritesheet(("ending_car", "car_endcar"),16, zlevel = 7, frames = 1)
mc_endcar = spritesheet(("ending_car", "mc_endcar"),22, zlevel = 6.8, frames = 1)
road_endcar = spritesheet(("ending_car", "road_endcar"),20, zlevel = 4, frames = 50)
#####
ending_car = (outline, bg1_endboat, bg2_endboat, car_endcar, building1_endboat, building2_endboat, mc_endcar, road_endcar, sun_endboat)

#### Ending: Parachute
building_endpara = spritesheet(("ending_parachute", "building_endpara"),3, zlevel = 2, frames = 31)
building2_endpara = spritesheet(("ending_parachute", "building2_endpara"),16, zlevel = 1, frames = 60)
mc_endpara = spritesheet(("ending_parachute", "mc_endpara"),22, zlevel = 4, frames = 60)
parachute_endpara = spritesheet(("ending_parachute", "parachute_endpara"),15, zlevel = 5, frames = 60)
rooftop_endpara = spritesheet(("ending_parachute", "rooftop_endpara"),3, zlevel = 3, frames = 20)
#####
ending_parachute = (outline,building_endpara, building2_endpara, mc_endpara, parachute_endpara, rooftop_endpara, sun_endboat, red_skyline)

#### Placeholder for minor rooms
building_placeholder = spritesheet(("city_placeholder","building_plhl"),16, zlevel = 6, frames = 1)
building2_placeholder = spritesheet(("city_placeholder","building2_plhl"),3, zlevel = 5, frames = 1)
road_placeholder = spritesheet(("city_placeholder","road_plhl"),20, zlevel = 4, frames = 1)
sun_placeholder = spritesheet(("city_placeholder","sun_plhl"),21, zlevel = 2, frames = 1)
####
room_placeholder = (outline, building_placeholder, building2_placeholder, road_placeholder, sun_placeholder, red_skyline)

#### Fight cutscene
body_fight = spritesheet(("cutscene_fight", "body_fight"),7, zlevel = 1, frames = 31)
eyes_fight = spritesheet(("cutscene_fight", "eyes_fight"),8, zlevel = 2, frames = 31)
#####
fight_cutscene = (body_fight,eyes_fight,outline, general_bg)