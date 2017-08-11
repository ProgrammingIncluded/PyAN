# File to Work with Platform Dependent Commandline Interfacing

from colorama import init
import os
import subprocess

clear = None
init()

if os.name in ('linux', 'osx', 'posix'):
    clear = lambda: subprocess.call("clear")
elif os.name in ('nt','dos'):
    clear = lambda: os.system("cls")
else:
    clear = printfunc

def printfunc():
    print "\n" * 120

# String Buffer.
BUF = u""
CALLED = False
CURSOR = (0, 0)

# Custom overriden print for buffer optimization.
def print_buf(val):
    global BUF
    global CALLED
    CALLED = True
    BUF += val
    

def display_buffer():
    if CALLED:
        global BUF
        global CALLED
        CALLED = False
        clear()
        print BUF
        BUF = u""
        # Reposition cursor
        print "\x1b[%d; %dH" % CURSOR
    

    