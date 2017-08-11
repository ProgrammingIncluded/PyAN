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

    with inp.Listener(on_press = inp.on_press, on_release = inp.on_release) as listener:
        display = [infs, chat]
        for mod in display:
            mod.set_state()

        # chat.set_state()
        while True:
            try:
                for mod in display:
                    mod.update_state()
                    # Clear the terminal for next display
                    mod.display_state()
                time.sleep(0.01)
                cmd.display_buffer()
            except:
                # Flush all prints
                sys.stdout.flush()
                traceback.print_exc()
                break

        pg.PROGRAM_CLOSE = True
        
    listener.join()

if __name__ == '__main__':
    main()