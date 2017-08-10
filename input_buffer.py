import program_global as pg
import getch
import sys, traceback
import multiprocessing

INPUT_BUFFER = multiprocessing.Queue()

class InputBuffer(multiprocessing.Process):

    def __init__(self, buffer):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.buffer = buffer

    # Function for reading input
    def run(self):
        while not self.exit.is_set():
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
                else:
                    self.buffer.put(char, False)

            except:
                # Early kill.
                # sys.stdout.flush()
                # traceback.print_exc()
                continue

    def shutdown(self):
        self.exit.set()


IBP = InputBuffer(INPUT_BUFFER)
