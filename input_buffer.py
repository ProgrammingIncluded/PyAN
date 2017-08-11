import program_global as pg
import getch
import sys, traceback
from multiprocessing import Process, RLock, Event, Pipe
from threading import Thread
from ctypes import c_wchar_p

class InputBuffer(Process):

    def __init__(self, pipe):
        Process.__init__(self)
        self.exit = Event()
        self.pipe_in, self.pipe_out = pipe

    # Function for reading input
    def run(self):
        while not self.exit.is_set():
            try:
                char = getch.getch()
                order = ord(char)
                if order == 3:
                    break
                elif order > 127 or order < 0:
                    print order
                    continue
                else:
                    self.pipe_out.send(char) 

            except:
                # Early kill.
                # sys.stdout.flush()
                # traceback.print_exc()
                break

    def shutdown(self):
        self.pipe_out.close()
        self.exit.set()

INPUT_BUFFER = ""
INPUT_LOCK = RLock()
INPUT_PIPE = Pipe()

# Thread needed for listening to input from another process.
class InputListener(Thread):
    def __init__(self, pipe):
        Thread.__init__(self)
        self.exit = Event()
        self.pipe_in, self.pipe_out = pipe
    
    def run(self):
        while not self.exit.is_set():
            try:
                global INPUT_BUFFER
                INPUT_BUFFER += self.pipe_in.recv()
            except:
                break

    def shutdown(self):
        self.exit.set()

IBP = InputBuffer(INPUT_PIPE)
IBT = InputListener(INPUT_PIPE)