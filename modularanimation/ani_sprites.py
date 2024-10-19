import os

class spritesheet():
    def gather_framelist(self):
        frameslist = []
        for frame in range(1,self.frames+1):
            path = os.path.join("modularanimation","spritesheets","{0}".format(self.path), "txt", "ascii-art ({0}).txt".format(frame)) ## os.path.join works regardless of OS
            # path = os.path.join("spritesheets","{0}".format(self.path), "txt", "ascii-art ({0}).txt".format(frame)) #if ran directly from animator.py
            file = open(path, "r", encoding="utf-8")
            frameslist.append(file.read())
            file.close()
        return frameslist
        
    def __init__(self, path, color, zlevel = 0, frames = 0, dx = 0, dy = 0, delay = 0):
        self.path = path
        self.color = color ##escape code
        self.zlevel = zlevel
        self.frames = frames
        self.dx = dx # not implemented
        self.dy = dy # not implemented
        self.delay = delay # not implemented
        self.frameslist = self.gather_framelist() # testing {self: [frame1, frame2,..],...}
        
    def get_whatever(self, attr): # pull attribute as object:attribute dict
        return {self: getattr(self, attr)}
    
    def get_flatvalue(self, attr):
        return getattr(self, attr)
        
# All txt frames should have the same amount of lines and same col at the end of a line. For now.
##################### path, escape code color, z-level, frames
outline = spritesheet("bg","\033[94m", zlevel = 22, frames = 1)
circle = spritesheet("circle","\033[94m", zlevel = 6, frames = 5)
square = spritesheet("square","\033[32m", zlevel = 4, frames = 5)
lightning = spritesheet("lightning","\033[32m", zlevel = 5, frames = 5)
dude = spritesheet("dude", "\033[32m", zlevel= 5, frames = 28)
frontpillars = spritesheet("frontpillars","\033[31m", zlevel = 8, frames = 28)
backpillars = spritesheet("backpillars","\033[31m", zlevel = 2, frames = 28)
outline1 = spritesheet("outline1", "\033[94m", zlevel = 99, frames = 1)

fire2 = spritesheet("fire2", "\033[31m", zlevel = 8, frames = 95)
building1 = spritesheet("building1", "\033[37m", zlevel = 7, frames = 95)
fire = spritesheet("fire", "\033[31m", zlevel = 6, frames = 95)
heli = spritesheet("heli", "\033[90m", zlevel = 5, frames = 95)
skyscraper = spritesheet("skyscraper", "\033[37m", zlevel = 4, frames = 95)
fire3 = spritesheet("fire3", "\033[31m", zlevel = 3, frames = 95)
citybg = spritesheet("citybg", "\033[37m", zlevel = 2, frames = 95)
pulse = spritesheet("pulse", "\033[31m", zlevel = 1, frames = 95)
climbers = spritesheet("climbers", "\033[32m", zlevel = 10, frames = 95)
dudeontop = spritesheet("dudeontop", "\033[94m", zlevel = 11, frames = 95)
moon = spritesheet("moon", "\033[31m", zlevel = 0.5, frames = 1)