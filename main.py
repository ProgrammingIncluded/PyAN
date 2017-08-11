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

    inp.IBP.start()
    inp.IBT.start()

    chat.set_state()

    # chat.set_state()
    while True:
        try:
            chat.update_state()
            # Clear the terminal for next display
            chat.display_state()
            cmd.display_buffer()
        except:
            # Flush all prints
            sys.stdout.flush()
            traceback.print_exc()
            break

    pg.PROGRAM_CLOSE = True
    inp.IBT.shutdown()
    inp.IBP.shutdown()
    inp.IBT.join()
    inp.IBP.join()


if __name__ == '__main__':
    main()