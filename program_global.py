import threading

# Flag to check if program is closed
PROGRAM_CLOSE = False
# Lock for modifying flag.
PROGRAM_FLAG_LOCK = threading.Lock()