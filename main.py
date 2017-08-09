import connect as cnt
import info_state as infs
import chat_state as chat
import program_global as pg
import input_buffer as inp
import command as cmd

import time
import queue
import threading

def main():
    chat.set_state()
    # Prep input thread
    #input_thread = threading.Thread(target = inp.input_read)
    #input_thread.start()

    # chat.set_state()
    while True:
        chat.update_state()
        # Clear the terminal for next display
        cmd.clear()
        chat.display_state()
        time.sleep(0.1)
    # input_thread.join()


if __name__ == '__main__':
    main()