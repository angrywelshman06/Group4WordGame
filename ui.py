import curses
from curses import *
from curses import wrapper
from curses import textpad
from curses import panel

x = 0
y = 0

def init_screen(): # initialise the screen
    global stdscreen
    start_color()
    stdscreen = curses.initscr()

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


def close(): # return terminal to normal
    stdscreen.keypad(0)
    stdscreen.clear()
    stdscreen.refresh()
    echo()
    nocbreak()
    endwin()
    print("\nwindow closed\n")





    
    

