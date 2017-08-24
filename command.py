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


if os.name in ('linux', 'osx', 'posix'):
    import curses
    def flush_input():
        curses.flushinp()
else:
    import msvcrt
    def flush_input():
        while msvcrt.kbhit():
            msvcrt.getch()

def printfunc():
    print("\n" * 120)

# String Buffer.
BUF = ""
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
        print(BUF)
        BUF = ""

    