import input_buffer as ib
import connect as cnt
from command import print_buf
import command as cmd

import asyncio
from datetime import datetime
from aiohttp import ClientSession
import json

# File to handle chats.
# Keeps track of new chat data, currently written chat info,
# as well as submitting chat to server.
# Right tightly coupled with input_buffer in order to allow proper processing
# of input. input_buffer calls chat_state functions directly.

# TODO: High Chat Check
# Feature to allow checking of chat to be based of need, not fixed rate.
# Two Conditions for checking chat to be more than normal.
# A Message was recently sent.
# Inactively over HCC_INACT. 
# Once HCC starts, chat checks every HCC_CHAT_PERIOD.
HCC = False
HCC_INACT = 30 # 30 seconds.
HCC_CHAT_PERIOD = 3
NON_HCC_CHAT_PERIOD = 3

CHAT_DATA = []
DISPLAY_BUF = ""

MAX_CHAT = 1000
MAX_DISPLAY = 10

# Value to store text buffer
CUR_BUF = ""

# From left to right
CURSOR = 0

LAST_SEND = datetime.now()

def move_cursor(x):
    global CURSOR
    if CURSOR + x < 0:
        CURSOR = 0
    elif CURSOR + x > len(CUR_BUF):
        CURSOR = len(CUR_BUF)
    else:
        CURSOR += x
    cmd.CALLED = True

def move_end():
    global CURSOR
    CURSOR = len(CUR_BUF)
    CHANG = True

def move_start():
    global CURSOR
    CURSOR = 0
    cmd.CALLED = True

# Function to delete backward in the input chat state.
def delete_back():
    global CURSOR
    if CURSOR != 0:
        global CUR_BUF
        CUR_BUF = CUR_BUF[0:CURSOR - 1] + CUR_BUF[CURSOR:]
        CURSOR -= 1
        cmd.CALLED = True

# Function to delete forward in the input chat state.
def delete_forward():
    global CURSOR
    global CUR_BUF
    if CURSOR != len(CUR_BUF):
        CUR_BUF = CUR_BUF[0:CURSOR] + CUR_BUF[CURSOR+1:]
        cmd.CALLED = True

# Function to clear the input of the chat state.
def clear():
    global CURSOR
    global CUR_BUF
    CURSOR = 0
    CUR_BUF = ""
    cmd.CALLED = True

async def update_chat_screen():
    global CHAT_DATA
    global DISPLAY_BUF
    DISPLAY_BUF = ""
    count = 0
    for elm in CHAT_DATA["messages"]:
        if count >= MAX_DISPLAY:
            break
        count += 1
        DISPLAY_BUF += elm["time"] + " "+ str(elm["userId"]) + "> " + ascii(elm["message"])[1:-1] + "\n"   

    cmd.CALLED = True

async def chat_update_task():
    # Do all chates under one session
    async with ClientSession() as session:
        # Keep sending responses
        while True:
            # Calculate time elapsed before next send.
            global LAST_SEND
            later = datetime.now()
            diff = (later - LAST_SEND).total_seconds()
            if diff < HCC_CHAT_PERIOD:
                await asyncio.sleep(HCC_CHAT_PERIOD - diff)
            LAST_SEND = datetime.now()
            
            param = cnt.PARAM
            param["apicall"] = "chatbox"
            param["limit"] = 50
            async with session.get(cnt.URL, params = param) as response:
                response_t = await response.text()
                global CHAT_DATA
                CHAT_DATA = json.loads(response_t)

                # Since chat data changed, we want to update the screen.
                await update_chat_screen()

def set_state():
    # Get the first 50 chat data.
    global CHAT_DATA
    CHAT_DATA = cnt.send_get("chatbox", {"limit":50})
    global DISPLAY_BUF
    DISPLAY_BUF = ""

    update_chat_screen()

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
        # Set global flag to let all states know we will update screen.
        CHANG = True
        cmd.CALLED = True
    # CHANG = True

def display_state():
    # Chang is used for chat state internally if someone does input
    # CHANG is set true. Howvever, if an external state draws, 
    # we also need to dump our state to display, so cmd.called is also checked.
    global CHANG
    if cmd.CALLED:
        print_buf(DISPLAY_BUF)
        print_buf("> : " + CUR_BUF[0:CURSOR] + "|" + CUR_BUF[CURSOR:])

