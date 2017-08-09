# File to handle chats.
# For now, very simple handling and flushing of chat.

CHAT_DATA = []

MAX_CHAT = 1000

def add_chat(usr, chat):
    if len(CHAT_DATA) >= MAX_CHAT:
        CHAT_DATA.pop(0)
    CHAT_DATA.append((usr, chat))