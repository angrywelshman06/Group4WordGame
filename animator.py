import itertools
import time
import curses
import os
from ani_sprites import *
#from combat import *
from curses import wrapper
from operator import attrgetter
import threading
from threading import Thread, Lock

clear = lambda: os.system('cls')

os.system("") # I need to remember why I put this here, I believe it was escape code related (which may be obsolete soon)

def adjust_to_max(list_framelists, max_frame): # adjusts to max frame
    for list in list_framelists:
        if len(list) < max_frame: # extends frames by last frame
            list.extend([list[-1]]*(max_frame - len(list)))
    return list_framelists

def preliminary_adjustments(args): # Grabs max frame, duplicates last frame.
    max_frame = max(args, key=attrgetter('frames')).frames # Gets the highest value of the spritesheet with most frames in args.
    list_framelists = [i.frameslist for i in args] # A list containing len(args) amount of lists, with each containing the frames of its respective spritesheet.
    list_framelists = adjust_to_max(list_framelists, max_frame) # Duplicates the final frame of every framelist to the amount of max_frame.
    return list_framelists
    
def run_animation_curses(win, *args): # Runs the animation, the parameters are the curses window and ani_sprites tuple.
    list_framelists = preliminary_adjustments(args) # Duplicates final frames if needed.
    for framelist in zip(*list_framelists): # * unpacks list_framelists into n different lists
        print_frame_curses(framelist,win,args)
        win.move(0,0) # Moves printing cursor back to position 0,0
        win.refresh()
        time.sleep(0.05) # Frame rate of the animation

def run_animation_curses_pad(win, pad_args, ui_lock, *args): #First arg should be edge/bg.
    list_framelists = preliminary_adjustments(args) # Duplicates final frames if needed.
    for framelist in zip(*list_framelists): # * unpacks list_framelists into n different lists
        ui_lock.acquire()
        print_frame_curses(framelist,win,args)
        win.move(0,0)
        win.refresh(pad_args[0], pad_args[1], pad_args[2], pad_args[3], pad_args[4], pad_args[5])
        ui_lock.release()
        time.sleep(0.05)
        
def print_stillshot_curses(framenumlist,win,*args):
    list_framelists = preliminary_adjustments(args)
    frames_to_print = []
    counter = 0
    for i in range(len(args)):
        frames_to_print.append(list_framelists[i][framenumlist[counter]])
        counter += 1
    for framelist in zip(*frames_to_print): # * unpacks list_framelists into n different lists
        print_frame_curses(framelist,win,args)

def print_stillshot_curses_pad(win, pad_args,ui_lock,*args): # [1,4], dude, backpillars
    list_framelists = preliminary_adjustments(args) # Duplicates final frames if needed.
    frames_to_print = []
    counter = 0
    for i in range(len(args)):
        frames_to_print.append(list_framelists[i][0])
        counter += 1
    for framelist in zip(*frames_to_print): # * unpacks list_framelists into n different lists
        ui_lock.acquire()
        print_frame_curses(framelist,win,args)
        win.refresh(pad_args[0], pad_args[1], pad_args[2], pad_args[3], pad_args[4], pad_args[5])
        ui_lock.release()
        
def print_frame_curses(framelist,win,args): # Prints frame on the screen
    for chars in zip(*framelist): # framelist unpacked into char number of different characters
        z_char_color = {} # Dictionary that stores zlevel: [ascii character to print, color]
        compare = [] # zlevel of every ascii char
        if all(" " in t for t in chars): # if all 3 chars are " " 
            win.addstr(" ") # prints empty space 
            continue
        for i in range(len(chars)): # zlevel of current arg: [current ascii char, color of current arg]
            z_char_color[args[i].zlevel] = [chars[i], args[i].color]
        for i in z_char_color:
            if z_char_color[i][0] != " ": # Appending empty space to the comparison list is pointless.
                compare.append(i)
        to_print=compare[0]
        for i in compare: # assigns the highest zlevel to to_print, and it is then used in z_char_color to access the char and color to print.
            if i > to_print:
                to_print = i
        win.addstr(z_char_color[to_print][0], curses.color_pair(z_char_color[to_print][1]))

def main(stdscr): ### TESTING PURPOSES ## Uncomment whichever path you need in the gather_framelist method in ani_sprites.py.
    stdscr.clear()
    print(" ANIMATOR MAIN FUNCTION CALLED ANIMATOR MAIN FUNCTION CALLED ANIMATOR MAIN FUNCTION CALLED\n")
    display_win = curses.newwin(36, 110, 0, 0)
    display_win.clear()
    display_win.scrollok(1) # This helps to prevent a curses-related crash.
    # curses.start_color()
    curses_setcolors() # imported from ani_sprites.py
    # print(cutscene_1_1, "WORKING")
    # run_animation_curses(display_win,*cutscene_1)
    # zombies = (("zombie", 2),("zombie", 1), ("zombie", 1),("zombie", 1),("zombie", 1),("zombie", 1),("zombie", 1),("zombie", 1)) #this tuple will be what's returned from the random battle generator
    #fight = initiate_combat(display_win,*zombies)
    # print(fight.draw_on_window(), "NOT WORKING")
    #print_stillshot_curses([0,0,0,0,0,0,0,0,0], display_win, *fight.draw_on_window())
    # print_stillshot_curses([0,0], display_win, holder1, holder2)
    # print_stillshot_curses([0,0], display_win, fight.creatures_dict["Enemy_1"].spritesheet, fight.creatures_dict["Enemy_2"].spritesheet)
    # fight = initiate_combat()
    #run_animation_curses(display_win,*cutscene_1)
    # run_animation_curses(display_win,*intro_2)    
    # print_stillshot_curses([22,3,10],display_win, dude, backpillars, frontpillars) ## ([frames to print for each arg], curses window, unlimited args..) #b4 commit
    # print_stillshot_curses([0,0], display_win, randomobj,general_bg)
    display_win.refresh()
    display_win.getch()
    display_win.clear()
    # print_stillshot_curses([0,0,0,0,0,0,0,0,0],display_win, *room_tutorial) ## ([frames to print for each arg], curses window, unlimited args..)
    display_win.refresh()
    display_win.getch()

wrapper(main)

input()
clear()