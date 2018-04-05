############################################
# Project: PyAN
# File: info_state.py
# By: ProgrammingIncluded
# Website: ProgrammingIncluded.com
# Desc: File to hold info state that
#       displays song information.
############################################

import chat_state as cs
import connect as cnt
import command as cmd

from datetime import datetime

INFO = {}

LAST_FETCH = datetime.now()
LAST_PRINT = datetime.now()

PREV_PERC = 0.0



# Call function to setup state.
def set_state():
    # Call first to get info.
    update_state()

def update_state():
    # Prepare the info state by getting necessary info.
    # For now do a simple grab from website. Later figure out smart way of doing things.
    global LAST_FETCH
    global INFO
    delta = datetime.now() - LAST_FETCH
    if "nowPlayingSong" not in INFO or float(INFO["timeLeft"]) <= delta.total_seconds():
        # Use manual sending because we only want to get info when we need it.
        INFO = cnt.send_get("now-playing")
        LAST_FETCH = datetime.now()
        cmd.CALLED = True

# Call function to draw
def display_state():
    global LAST_PRINT

    # We need to check CALLED because other states may have drawn
    if cmd.CALLED or ((datetime.now() - LAST_PRINT).total_seconds() > 1):
        cur = INFO["nowPlayingSong"]
        print_song_data(cur)
        delta = datetime.now() - LAST_FETCH
        perc = 100.0 - ((float(INFO["timeLeft"]) - delta.total_seconds()) * 100.0 / float(cur["totalseconds"]))
        if perc > 100.0:
            perc = 100.0
        elif perc < 0.0:
            perc = 0.0
        
        cmd.print_buf("Percent: " + str(int(perc)) + "%\n\n")
        LAST_PRINT = datetime.now()

    
    

def print_song_data(song_info):
    res = "Title: " + str(song_info["title"]) + "\n"
    res += "Album: " + str(song_info["album"]) + "\n"
    res += "Artist: " + str(song_info["artist"]) + "\n"
    res += "Comp: " + str(song_info["composers"]) + "\n"
    cmd.print_buf(res)