import curses
from curses import *
from curses import wrapper
from curses import textpad
from curses import panel

x = 0
y = 0

def init_screen(): # initialise the screen
    global stdscreen
    stdscreen = curses.initscr()

    noecho()
    cbreak()
    stdscreen.keypad(1)

    stdscreen.clear()

    stdscreen.addstr("test string\n")
    stdscreen.addstr("test string\n")
    stdscreen.addstr("test string\n")

    stdscreen.refresh()

    curses.napms(2000)

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

def close(): # return terminal to normal
    stdscreen.keypad(0)
    stdscreen.keypad(0)
    echo()
    echo()
    echo()
    echo()
    nocbreak()
    nocbreak()
    nocbreak()
    nocbreak()
    endwin()
    print("\nwindow closed\n")

def write(msg = "\n"):
    art_pad.addstr("write called\n")
    art_pad.refresh(0,0,0,0, y-1, int(x/2)-1)
    curses.napms(1000)
    text_pad.addstr(msg)
    try: 
        text_pad.refresh(text_pad_pos, 0, 0, int(x/2), y-1, x)
    except:
        pass




    
    

