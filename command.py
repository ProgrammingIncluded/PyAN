# File to Work with Platform Dependent Commandline Interfacing

import os
import subprocess

clear = None

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

# Custom overriden print for buffer optimization.
def print_buf(val):
    global BUF
    global CALLED
    CALLED = True
    BUF += val
    

def display_buffer():
    global CALLED
    if CALLED:
        global BUF
        CALLED = False
        clear()
        print BUF
        BUF = u""

    