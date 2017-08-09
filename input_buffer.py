import program_global as pg
import getch
import threading
import sys, traceback
import Queue

INPUT_BUFFER = ""
INPUT_LOCK = threading.Lock()

# Function for reading input
def input_read():
    while True:
        try:
            # Exit loop
            pg.PROGRAM_FLAG_LOCK.acquire()
            if pg.PROGRAM_CLOSE:
                pg.PROGRAM_FLAG_LOCK.release()
                break
            pg.PROGRAM_FLAG_LOCK.release()
            
            char = getch.getch()
            if ord(char) == 3:
                break

            global INPUT_BUFFER
            INPUT_LOCK.acquire()
            INPUT_BUFFER += char
            INPUT_LOCK.release()
        except:
            # Early kill.
            # sys.stdout.flush()
            # traceback.print_exc()
            break

    pg.PROGRAM_FLAG_LOCK.acquire()
    pg.PROGRAM_CLOSE = True
    pg.PROGRAM_FLAG_LOCK.release()
