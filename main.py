import connect as cnt
import info_state as infs
import chat_state as chat
import program_global as pg
import input_buffer as inp
import command as cmd

import sys,codecs
from datetime import datetime
import time
import multiprocessing
import traceback
import asyncio
from contextlib import suppress

# Keep track of FPS
FPS = 1200.0
ELP = datetime.now()

async def main():
    with inp.Listener(on_press = inp.on_press, on_release = inp.on_release) as listener:
        display = [infs, chat]
        for mod in display:
            mod.set_state()

        # chat.set_state()
        while True:
            try:
                # Update all states first
                for mod in display:
                    mod.update_state()
                
                # Prepare all states for displaying.
                for mod in display:
                    mod.display_state()

                cmd.display_buffer()

                # Dispatch for async.
                global ELP
                later = datetime.now()
                diff = (later - ELP).total_seconds()
                if diff < (1/FPS):
                    await asyncio.sleep((1/FPS) - diff)
                else:
                    await asyncio.sleep(0)
                ELP = datetime.now()


            except:
                # Flush all prints
                sys.stdout.flush()
                traceback.print_exc()
                break

        pg.PROGRAM_CLOSE = True
        
    listener.join()

if __name__ == '__main__':
    # Start the main loop with async manager.
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    # Clean up tasks
    pending = asyncio.Task.all_tasks()
    for task in pending:
        task.cancel()
        with suppress(asyncio.CancelledError):
            loop.run_until_complete(task)
