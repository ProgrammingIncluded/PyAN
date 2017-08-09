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