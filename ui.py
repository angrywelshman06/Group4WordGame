import curses
from curses import *
from curses import wrapper
from curses import textpad
from curses import panel

x = 0
y = 0

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
    curses.init_pair(23, 240, 240), # GREY 3
    curses.init_pair(24, 196, 0), # red text
    curses.init_pair(25, 11, 0), # yellow text
    curses.init_pair(50, 0, 196), # RED EXPLODING
    
def init_screen(): # initialise the screen
    global stdscreen
    stdscreen = curses.initscr()
    start_color()
    curses_setcolors() # Custom colours
    
    noecho()
    cbreak()
    stdscreen.keypad(1)

    stdscreen.clear()
    stdscreen.refresh()

    global x
    global y

    y, x = stdscreen.getmaxyx()

    global art_pad

    art_pad = curses.newpad(y, x)
    art_pad.scrollok(True)

    art_pad.addstr("init!")

    global text_pad
    global text_pad_pos

    text_pad = curses.newpad(100, int(x/2))
    text_pad.keypad(True)
    text_pad.scrollok(True)
    text_pad_pos = 0

    stdscreen.refresh()

def resize_window():
    global y
    global x

    y, x = stdscreen.getmaxyx()
    

def close(): # return terminal to normal
    stdscreen.keypad(0)
    stdscreen.clear()
    stdscreen.refresh()
    echo()
    nocbreak()
    endwin()
    print("\nwindow closed\n")





    
    

