import connect as cnt
import info_state as infs
import chat_state as chat
import program_global as pg
import input_buffer as inp
import command as cmd

import sys,codecs
import time
import multiprocessing
import traceback

def main():
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    sys.stderr = codecs.getwriter('utf8')(sys.stderr)

    # Prep input thread
    #input_thread = multiprocessing.Process(target = inp.input_read)
    input_thread = inp.IBP
    input_thread.start()
    chat.set_state()

    # chat.set_state()
    while True:
        try:
            # Check if we want to quit
            pg.PROGRAM_FLAG_LOCK.acquire()
            if pg.PROGRAM_CLOSE:
                pg.PROGRAM_FLAG_LOCK.release()
                break
            pg.PROGRAM_FLAG_LOCK.release()

            chat.update_state()
            # Clear the terminal for next display
            cmd.clear()
            chat.display_state()
        except:
            # Flush all prints
            sys.stdout.flush()
            traceback.print_exc()
            break

    pg.PROGRAM_FLAG_LOCK.acquire()
    pg.PROGRAM_CLOSE = True
    pg.PROGRAM_FLAG_LOCK.release()
    input_thread.shutdown()
    input_thread.join()


if __name__ == '__main__':
    main()