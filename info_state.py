# File to hold info_state
import command as cmd
import connect as cnt
import progressbar

from datetime import datetime

INFO = {}

LAST_FETCH = datetime.now()

# High Chat Check
# Two Conditions for checking chat to be more than normal.
# A Message was recently sent.
# Inactively over HCC_INACT. 
# Once HCC starts, chat checks every HCC_CHAT_PERIOD.
HCC = False
HCC_INACT = 30 # 30 seconds.
HCC_CHAT_PERIOD = 1
NON_HCC_CHAT_PERIOD = 3

# Progress bar
bar = progressbar.ProgressBar(redirect_stdout = True)

# Call function to setup state.
def set_state():
    # Call first to get info.
    update_state()
    display_state()

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
# TODO: Make more efficient by calling print only once.
def display_state():
    cmd.clear()
    cur = INFO["nowPlayingSong"]
    print_song_data(cur)
    delta = datetime.now() - LAST_FETCH
    perc = 100.0 - ((float(INFO["timeLeft"]) - delta.total_seconds()) * 100.0 / float(cur["totalseconds"]))
    bar.update(perc)

def print_song_data(song_info):
    res = "Title: " + str(song_info["title"]) + "\n"
    res += "Album: " + str(song_info["album"]) + "\n"
    res += "Artist: " + str(song_info["artist"]) + "\n"
    res += "Comp: " + str(song_info["composers"]) + "\n"
    print res