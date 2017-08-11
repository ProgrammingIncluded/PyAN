import command as cmd
import Queue
from pynput.keyboard import Key, Listener


INPUT_BUFFER = Queue.Queue()
LOCK = False
SHIFT = False

def on_press(key):
    global INPUT_BUFFER
    global LOCK
    global SHIFT

    # Listen to Fx keys.
    if key == Key.f1:
        LOCK = ~LOCK
        return

    if LOCK:
        return

    # Check if there is anything regarding spaces
    if key == Key.space:
        INPUT_BUFFER.put(" ")
        return
    elif key == Key.shift or key == Key.shift_l or key == Key.shift_r:
        SHIFT = True
        return
    elif key == Key.up:
        cmd.CURSOR = (cmd.CURSOR[0] - 1, cmd.CURSOR[1])
        print "\x1b[%d; %dH" % cmd.CURSOR
        return

    try:
        if SHIFT:
            INPUT_BUFFER.put(key_map(key.char))
        else:
            INPUT_BUFFER.put(key.char)
    except:
        INPUT_BUFFER.put("*")

def on_release(key):
    if key == Key.shift or key == Key.shift_l or key == Key.shift_r:
        global SHIFT
        SHIFT = False

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
