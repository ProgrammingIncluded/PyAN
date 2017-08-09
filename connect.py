# File incharge of establishing connection and communicating with server.

import requests
import threading
import time
import ConfigParser
import json

import chat as ch

# Constants #
URL = "https://www.animenfo.com/radio/api.php"
TOKEN_FILE = "token.txt"
USR = "PUT IN TOKEN_FILE"
DEV_KEY = "PUT IN TOKEN_FILE"
API_KEY = "PUT IN TOKEN_FILE"
# Max requests per minute.
MAX_ACTION = 60
# Action count.
ACTION_CNT = 0

# Cooldown time, i.e. API limit request (seconds).
TIME_WAIT = 1

# Var to check last sent command.
LAST_SEND = time.time()

# Lock in charge of time resource.
# TIME_L = Lock()

# Command to get response.
def send_get(cmd, param = {}):
    json_d = {"devkey":DEV_KEY, "apiusr":USR, "apikey":API_KEY, "apicall":cmd}.copy()
    json_d.update(param)
    print json_d
    return json.loads(requests.get(URL, params = json_d).text)

def send_post(cmd, param):
    pass

def parseToken():
    config = ConfigParser.ConfigParser()
    config.read(TOKEN_FILE)
    global USR
    global DEV_KEY
    global API_KEY
    USR = config.get("Settings", "USR")
    DEV_KEY = config.get("Settings", "DEV")
    API_KEY = config.get("Settings", "API")


# Parse the token file and get data.
parseToken()

# Function to unlock flag.