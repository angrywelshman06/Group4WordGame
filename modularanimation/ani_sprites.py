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
    
class spritesheet():
    def __init__(self, path, color, zlevel = 0, frames = 0, dx = 0, dy = 0, delay = 0):
        self.path = path
        self.color = color # curses pair
        self.zlevel = zlevel
        self.frames = frames
        self.dx = dx 
        self.dy = dy
        self.delay = delay # not implemented
        self.frameslist = self.gather_framelist() # list containing every frame
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
outline = spritesheet(("outline1",), 9, zlevel = 77, frames = 1)
randomobj = spritesheet(("randomobj",), 8, zlevel = 134, frames = 1, dx = 66, dy = 22)

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

cutscene_1_1 = (outline,zombie_1, red_elements_1, general_bg, body_1, red_elements_2, randomobj)