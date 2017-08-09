# File to hold info_state
import connect as cnt
import command as cmd
import progressbar

from datetime import datetime

INFO = {}

LAST_FETCH = datetime.now()


# Progress bar
bar = progressbar.ProgressBar(redirect_stdout = True)

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
        INFO = cnt.send_get("now-playing")
        LAST_FETCH = datetime.now()

# Call function to draw
def display_state():
    cur = INFO["nowPlayingSong"]
    print_song_data(cur)
    delta = datetime.now() - LAST_FETCH
    perc = 100.0 - ((float(INFO["timeLeft"]) - delta.total_seconds()) * 100.0 / float(cur["totalseconds"]))
    if perc > 100.0:
        perc = 100.0
    elif perc < 0.0:
        perc = 0.0
    bar.update(perc)

    
    

def print_song_data(song_info):
    res = "Title: " + str(song_info["title"]) + "\n"
    res += "Album: " + str(song_info["album"]) + "\n"
    res += "Artist: " + str(song_info["artist"]) + "\n"
    res += "Comp: " + str(song_info["composers"]) + "\n"
    print res