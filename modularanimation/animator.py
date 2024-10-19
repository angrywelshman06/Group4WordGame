import itertools
import time
import curses
import os
from ani_sprites import *
from curses import wrapper
from operator import attrgetter

clear = lambda: os.system('cls')

os.system("") # I need to remember why I put this here, I believe it was escape code related (which may be obsolete soon)

def adjust_to_max(list_framelists, max_frame): # adjusts to max frame
    for list in list_framelists:
        if len(list) < max_frame: # extends frames by last frame
            list.extend([list[-1]]*(max_frame - len(list)))
    return list_framelists
        
#### CURSES #############################################################################
#### WIP
def print_stillshot_curses(framenumlist,win, *args): # [1,4], dude, backpillars
    max_frame = max(args, key=attrgetter('frames')).frames
    list_framelists = [i.frameslist for i in args]
    list_framelists = adjust_to_max(list_framelists, max_frame)
    frames_to_print = []
    for i in range(len(args)):
        frames_to_print.append(list_framelists[i][framenumlist[0]])
        del framenumlist[0]
    for framelist in zip(*frames_to_print): # * unpacks list_framelists into n different lists (objs)
        print_frame_curses(framelist,win,args)
        
def print_frame_curses(framelist,win, args):
    for chars in zip(*framelist): # framelist unpacked into char number of different characters
        z_char_color = {}
        compare = []
        if all(" " in t for t in chars): # if all 3 chars are " " 
            win.addstr(" ")
            continue
        for i in range(len(chars)): # zlevel: [char, color]
            z_char_color[args[i].zlevel] = [chars[i], args[i].color]
        for i in z_char_color:
            if z_char_color[i][0] != " ":
                compare.append(i)
        to_print=compare[0]
        for i in compare:
            if i > to_print:
                to_print = i
        # print(z_char_color[to_print][1]+z_char_color[to_print][0], end="") # color + char
        win.addstr(z_char_color[to_print][0])
        win.scrollok(1) # This helps to prevent a curses-related crash

def main(stdscr): ### WIP ### JUST FOR TESTING PURPOSES
    stdscr.clear()
    display_win = curses.newwin(36, 110, 5, 5)
    display_win.clear()
    # print_stillshot_curses([22,3,10],stdscr, dude, backpillars, frontpillars) ## ([frames to print for each arg], curses window, unlimited args..) #b4 commit
    print_stillshot_curses([22,3,10],display_win, dude, backpillars, frontpillars) ## ([frames to print for each arg], curses window, unlimited args..)
    display_win.refresh()
    display_win.getch()

wrapper(main)

clear()