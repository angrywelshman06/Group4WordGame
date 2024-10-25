import os
import curses

# Here so I can set colors
curses.initscr()

# Run this in the mainloop of the main file
def curses_setcolors():
    curses.init_pair(1, 0, 243), # GREY
    curses.init_pair(2, 0, 136), # WOOD MATERIALS 1
    curses.init_pair(3, 0, 240), # DARK ROOM
    curses.init_pair(4, 0, 34), # GREEN 1
    curses.init_pair(5, 0, 64), # GREY 2 
    curses.init_pair(6, 178, 88), # FIRE
    curses.init_pair(7, 70, 0), # ZOMBIE GREEN
    curses.init_pair(8, 196, 52), # RED
    curses.init_pair(9, 245, 0), # HELICOPTER GREY
    curses.init_pair(10, 0, 249), # BUILDINGS GREY
    curses.init_pair(11, 0, 33), # PROTAG_BLUE
    curses.init_pair(12, 15, 0), # PILLOW WHITE
    curses.init_pair(13, 33, 33), # PROTAG_BLUE2
    curses.init_pair(14, 178,33), # ENEMY INFO PAIR
    curses.init_pair(15, 0, 54), # PURPLE
    curses.init_pair(16, 0, 255), # WHITE
    curses.init_pair(17, 0, 109), # BLUE HUE
    curses.init_pair(18, 0, 105), # SLATE BLUE
    curses.init_pair(19, 88, 88), # DARK RED
    curses.init_pair(20, 0, 7), # SILVER
    curses.init_pair(21, 0, 184), # ORANGE
    curses.init_pair(22, 33, 33), # PROTAG_BLUE 2
    curses.init_pair(23, 196, 0), # red text
    curses.init_pair(24, 178, 0), # yellow text
    
class spritesheet():
    def __init__(self, path, color, zlevel = 0, frames = 0, dx = 0, dy = 0, delay = 0, infolist = 0):
        self.path = path
        self.color = color # curses pair
        self.zlevel = zlevel
        self.frames = frames
        self.dx = dx 
        self.dy = dy
        self.delay = delay # not implemented
        self.frameslist = self.gather_framelist() # list containing every frame
        self.infolist = infolist
        if infolist != 0:
            self.frameslist = self.transform_to_details()
        if (self.dx != 0) or (self.dy != 0):
            self.frameslist = self.extend_frames()

    def gather_framelist(self):
        frameslist = []
        for frame in range(1,self.frames+1):
            # path = os.path.join("modularanimation","spritesheets","{0}".format(self.path), "txt", "ascii-art ({0}).txt".format(frame)) ## os.path.join works regardless of OS
            path = os.path.join("spritesheets",*self.path, "ascii-art ({0}).txt".format(frame)) #if ran directly from animator.py
            file = open(path, "r", encoding="utf-8")
            frameslist.append(file.read())
            file.close()
        return frameslist

    def transform_to_details(self): # By now we have a creature_dict value : spritesheet pair in info_dict
        name = self.infolist[0]
        number = self.infolist[1]
        level = self.infolist[2]
        hp = self.infolist[3]
        newframeslist = []
        
        for index,value in enumerate(self.frameslist):
            newframe = self.frameslist[index].splitlines()     
            
            for index, value in enumerate(newframe):
                newframe[index] = " "*len(newframe[index])
            # for line in newframe:
                # line = " "*len(line)
            
            for index,line in enumerate(newframe):
                if index == 2:
                    newframe[index] = name +" No."+str(number)+line[len(name+" No."+str(number)):]
                if index == 3:
                    newframe[index] = "Lv"+str(level)+" HP:"+str(hp)+line[index][len("Lv"+str(level)+" HP:"+str(hp)):]
                else:
                    pass
            # for line in newframe:
                # for index, char in enumerate(line):
                    # if index == 2:
                        # line[index] = name +" No."+str(number)+line[index][len(name+" No."+str(number)):]
                    # if index == 3:
                        # line[index] = "Lv"+str(level)+" HP:"+str(hp)+line[len("Lv"+str(level)+" HP:"+str(hp)):]
                    # else:
             
            
            newframe = "\n".join(newframe) # joins back the frames
            newframeslist.append(newframe)
        
        return newframeslist

    
    def extend_frames(self):
        ### Standard: col 100, rows 34
        # don't go out of the standard bounds when working with dx and dy
        newframeslist = []
        for index, value in enumerate(self.frameslist):
            newframe = self.frameslist[index].splitlines()
            
            for index, value in enumerate(newframe):
                if len(newframe[index]) < 100:
                    newframe[index] += " "*(100-len(newframe[index])) 
                    
            if len(newframe) < 34: # add empty space 
                for i in range(len(newframe), 34):
                    newframe.append(" "*100)
                    
            for i in range(self.dy): # DY adjustment
                newframe.insert(0,(" "*100))
                del newframe[-1]
                
            if self.dx != 0:
                for index, value in enumerate(newframe): # DX adjustment
                    newframe[index] = (" "*(self.dx) + newframe[index])[:-(self.dx)]
                    
            newframe = "\n".join(newframe) # joins back the frames
            newframeslist.append(newframe)
            
        return newframeslist
        
# All txt frames should have the same amount of lines and same col at the end of a line. For now.
##################### path, escape code color, z-level, frames

###### Test
# outline = spritesheet(("bg",),"\033[37m", zlevel = 22, frames = 1)
# circle = spritesheet(("circle",),"\033[94m", zlevel = 6, frames = 5)
# square = spritesheet(("square",),"\033[32m", zlevel = 4, frames = 5)
# lightning = spritesheet(("lightning",),"\033[32m", zlevel = 5, frames = 5)
# dude = spritesheet(("dude",), "\033[32m", zlevel= 5, frames = 28)
# frontpillars = spritesheet(("frontpillars",),"\033[31m", zlevel = 8, frames = 28)
# backpillars = spritesheet(("backpillars",),"\033[31m", zlevel = 2, frames = 28)

###### Multi-purpose
general_bg = spritesheet(("background",), 3, zlevel = 0.05, frames = 1)
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
intro_1 = (fire,fire2,fire3,skyscraper,building1,heli,citybg,pulse, climbers, dudeontop, moon)

##### Intro part 2 
intro_male_eyes = spritesheet(("intro_2","intro_male_eyes"), 1, zlevel = 5, frames = 38)
intro_male_body = spritesheet(("intro_2","intro_male_body"), 11, zlevel = 3, frames = 1)
intro_male_hair = spritesheet(("intro_2","intro_male_hair"), 2, zlevel = 10, frames = 1)
bed = spritesheet(("intro_2","bed"), 5, zlevel = 0.1, frames = 1)
pillow = spritesheet(("intro_2","pillow"), 12, zlevel = 0.2, frames = 1)
#### Unpack this in run_animation_curses
intro_2 = (intro_male_body,intro_male_hair,intro_male_eyes, bed, pillow, general_bg,outline)

##### Tutorial Room
bed = spritesheet(("room_tutorial", "bed"), 5, zlevel = 12, frames = 1)
bg = spritesheet(("room_tutorial", "bg"), 3, zlevel = 1, frames = 1)
cobweb = spritesheet(("room_tutorial", "cobweb"), 1, zlevel = 10, frames = 1)
misc = spritesheet(("room_tutorial", "misc"), 1, zlevel = 20, frames = 1)
scratches = spritesheet(("room_tutorial", "scratches"), 1, zlevel = 11, frames = 1)
wood = spritesheet(("room_tutorial", "wood"), 2, zlevel = 15, frames = 1)
#### Unpack in print_stillshot_curses. Should look like print_stillshot_curses([0,0,0,0,0,0,0],display_win, *room_tutorial). The list thing is dumb, I'll rework it.
room_tutorial = (outline,bed, bg, cobweb, misc, scratches, wood)

##### Cutscene 1
zombie_1 = spritesheet(("cutscene_1", "zombie"), 7, zlevel = 12, frames = 58)
body_1 = spritesheet(("cutscene_1", "body_1"), 11, zlevel = 3, frames = 1)
red_elements_1 = spritesheet(("cutscene_1", "red"), 8, zlevel = 15, frames = 58)
red_elements_2 = spritesheet(("cutscene_1", "red2"), 8, zlevel = 4, frames = 1)
cutscene_1 = (outline,zombie_1, red_elements_1, general_bg, body_1, red_elements_2)

#####
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
#####
room_petrol = (outline,building_ptr,floor_ptr,glass_ptr,pillar_ptr,pump_ptr,sign_ptr,red_skyline)

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

#### Cutscene death 1
blood_csd1 = spritesheet(("cutscene_death_1", "blood_csd1"),8, zlevel = 0.1, frames = 33)
mc_csd1 = spritesheet(("cutscene_death_1", "mc_csd1"),22, zlevel = 2, frames = 33)
zombie1_csd1 = spritesheet(("cutscene_death_1", "zombie1_csd1"),7, zlevel = 3, frames = 33)
zombie2_csd1 = spritesheet(("cutscene_death_1", "zombie2_csd1"),7, zlevel = 1, frames = 33)
#####
cutscene_death_1 = (blood_csd1, mc_csd1, zombie1_csd1, zombie2_csd1, general_bg,outline)