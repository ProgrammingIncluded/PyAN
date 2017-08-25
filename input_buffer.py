############################################
# Project: PyAN
# File: input_buffer.py
# By: SuperKaitoKid
# Website: superkaitokid.github.io
# Desc: File to deal with input.
###########################################

import command as cmd
import chat_state as cs
import queue
import sys
from pynput.keyboard import Key, Listener


INPUT_BUFFER = queue.Queue()
LOCK = False
SHIFT = False

def on_press(key):
    global INPUT_BUFFER
    global LOCK
    global SHIFT

    # Listen to Fx keys.
    if key == Key.f12:
        LOCK = ~LOCK
        return

    if LOCK:
        return

    # Check if there is anything regarding spaces
    if key == Key.space:
        INPUT_BUFFER.put(" ", False)
        return
    elif key == Key.enter:
        cs.clear()
        return
    elif key == Key.backspace:
        cs.delete_back()
        return
    elif key == Key.delete:
        cs.delete_forward()
        return
    elif key == Key.shift or key == Key.shift_l or key == Key.shift_r:
        SHIFT = True
        return
    elif key == Key.up:
        return
    elif key == Key.down:
        return
    elif key == Key.right:
        cs.move_cursor(1)
        return
    elif key == Key.left:
        cs.move_cursor(-1)
        return
    elif key == Key.home:
        cs.move_start()
        return
    elif key == Key.end:
        cs.move_end()
        return

    try:
        if SHIFT:
            INPUT_BUFFER.put(key_map(key.char), False)
        else:
            INPUT_BUFFER.put(key.char, False)
    except:
        INPUT_BUFFER.put("*", False)

def on_release(key):
    if key == Key.shift or key == Key.shift_l or key == Key.shift_r:
        global SHIFT
        SHIFT = False
    cmd.CALLED = True
    cmd.flush_input()


def key_map(val):
    # Check if keys are special.
    if val == "1":
        return  "!"
    elif val == "2":
        return  "@"
    elif val == "3":
        return  "#"
    elif val == "4":
        return  "$"
    elif val == "5":
        return  "%"
    elif val == "6":
        return  "^"
    elif val == "7":
        return  "&"
    elif val == "8":
        return  "*"
    elif val == "9":
        return  "("
    elif val == "0":
        return  ")"
    elif val == "-":
        return  "_"
    elif val == "=":
        return  "+"
    elif val == "`":
        return  "~"
    elif val == ";":
        return  ":"
    elif val == "'":
        return  '"'
    elif val == ",":
        return  '<'
    elif val == ".":
        return  '>'
    elif val == "/":
        return  '?'
    elif val == "[":
        return  '{'
    elif val == "]":
        return  '}'
    elif val == "\\":
        return  '|'
    else:
        return val.upper()
