import input_buffer as ib
import connect as cnt
from command import print_buf

import asyncio
from datetime import datetime
from aiohttp import ClientSession

# File to handle chats.
# For now, very simple handling and flushing of chat.

# High Chat Check
# Two Conditions for checking chat to be more than normal.
# A Message was recently sent.
# Inactively over HCC_INACT. 
# Once HCC starts, chat checks every HCC_CHAT_PERIOD.
HCC = False
HCC_INACT = 30 # 30 seconds.
HCC_CHAT_PERIOD = 2
NON_HCC_CHAT_PERIOD = 3

CHAT_DATA = []
DISPLAY_BUF = ""

MAX_CHAT = 1000
MAX_DISPLAY = 10

# Value to store text buffer
CUR_BUF = ""

# From left to right
CURSOR = 0

CHANG = True

LAST_SEND = datetime.now()

def move_cursor(x):
    global CURSOR
    if CURSOR + x < 0:
        CURSOR = 0
    elif CURSOR + x > len(CUR_BUF):
        CURSOR = len(CUR_BUF)
    else:
        CURSOR += x
    global CHANG
    CHANG = True

def move_end():
    global CURSOR
    global CHANG
    CURSOR = len(CUR_BUF)
    CHANG = True

def move_start():
    global CURSOR
    global CHANG
    CURSOR = 0
    CHANG = True

def delete_back():
    global CURSOR
    if CURSOR != 0:
        global CUR_BUF
        CUR_BUF = CUR_BUF[0:CURSOR - 1] + CUR_BUF[CURSOR:]
        CURSOR -= 1

def delete_forward():
    global CURSOR
    if CURSOR != len(CUR_BUF):
        global CUR_BUF
        CUR_BUF = CUR_BUF[0:CURSOR] + CUR_BUF[CURSOR+1:]

async def chat_update_task():
    # Do all chates under one session
    async with ClientSession() as session:
        # Keep sending responses
        while True:
            # Calculate time elapsed before next send.
            global LAST_SEND
            later = datetime.now()
            diff = (later - LAST_SEND).total_seconds()
            if diff >= HCC_CHAT_PERIOD:
                LAST_SEND = datetime.now()
            else:
                await asyncio.sleep(HCC_CHAT_PERIOD - diff)
            
            param = cnt.PARAM
            param["apicall"] = "chatbox"
            param["limit"] = 50
            async with session.get(cnt.URL, params = param) as response:
                response = await response.read()
                global CHAT_DATA
                CHAT_DATA = response
                print_buf(CHAT_DATA)

            



def set_state():
    # Get the first 50 chat data.
    global CHAT_DATA
    CHAT_DATA = cnt.send_get("chatbox", {"limit":50})
    global DISPLAY_BUF
    DISPLAY_BUF = ""

    count = 0
    for elm in CHAT_DATA["messages"]:
        if count >= MAX_DISPLAY:
            break
        count += 1
        DISPLAY_BUF += elm["message"] + "\n"   
    
    # Set up chat update task.
    asyncio.ensure_future(chat_update_task())

    
def update_state():
    if not ib.INPUT_BUFFER.empty():
        global CHANG
        global CUR_BUF
        while not ib.INPUT_BUFFER.empty():
            global CURSOR
            if CURSOR == len(CUR_BUF):
                CURSOR += 1
                CUR_BUF += ib.INPUT_BUFFER.get(False)
            else:
                CUR_BUF = CUR_BUF[0:CURSOR] + ib.INPUT_BUFFER.get(False) + CUR_BUF[CURSOR:]
        CHANG = True
    # CHANG = True

def display_state():
    global CHANG
    if CHANG:
        CHANG = False
        print_buf(DISPLAY_BUF)
        print_buf("> : " + CUR_BUF[0:CURSOR] + "|" + CUR_BUF[CURSOR:])

