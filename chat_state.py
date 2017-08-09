import connect as cnt

# File to handle chats.
# For now, very simple handling and flushing of chat.

# High Chat Check
# Two Conditions for checking chat to be more than normal.
# A Message was recently sent.
# Inactively over HCC_INACT. 
# Once HCC starts, chat checks every HCC_CHAT_PERIOD.
HCC = False
HCC_INACT = 30 # 30 seconds.
HCC_CHAT_PERIOD = 1
NON_HCC_CHAT_PERIOD = 3

CHAT_DATA = []

MAX_CHAT = 1000
MAX_DISPLAY = 10

def set_state():
    # Get the first 50 chat data.
    global CHAT_DATA

    CHAT_DATA = cnt.send_get("chatbox", {"limit":50})
    

def update_state():
    pass
    

def display_state():
    buf = ""
    
    count = 0
    for elm in CHAT_DATA["messages"]:
        if count >= MAX_DISPLAY:
            break
        count += 1
        buf += elm + "\n"

    print buf

def add_chat(usr, chat):
    if len(CHAT_DATA) >= MAX_CHAT:
        CHAT_DATA.pop(0)
    CHAT_DATA.append((usr, chat))