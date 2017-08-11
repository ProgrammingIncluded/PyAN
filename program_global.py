import threading

# Flag to check if program is closed
# Should be READ ONLY for everythread not main.
PROGRAM_CLOSE = False