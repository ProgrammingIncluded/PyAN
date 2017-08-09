import program_global as pg
import queue

INPUT_BUFFER = queue.Queue()

# Function for reading input
def input_read():
    while True:
        # Exit loop
        pg.PROGRAM_FLAG_LOCK.acquire()
        if pg.PROGRAM_CLOSE:
            break
        pg.PROGRAM_FLAG_LOCK.release()



    pg.PROGRAM_FLAG_LOCK.release()