
#################################################
# Project: PyAN
# File: connect.py
# By: ProgrammingIncluded
# Website: ProgrammingIncluded.com
# Desc: File in charge of establishing connection
#       to the server.
#################################################

import asyncio
import requests
import threading
import time
import configparser
import json

# Constants #
URL = "https://www.animenfo.com/radio/api.php"
PARAM = {}
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

# Lock in charge of time resource.
# TIME_L = Lock()

# Command to get response.
# Repeat_time to set timeout before next call.
def send_get(cmd, param = {}, repeat_time = -1):
    json_d = PARAM.copy()
    json_d["apicall"] = cmd
    json_d.update(param)
    print(json_d)
    return json.loads(requests.get(URL, params = json_d).text)


def send_post(cmd, param, repeat_time = -1):
    json_d = PARAM.copy()
    json_d["apicall"] = cmd
    json_d.update(param)
    print(json_d)
    return json.loads(requests.post(URL, params = json_d).text)

def parseToken():
    config = configparser.ConfigParser()
    config.read(TOKEN_FILE)
    global USR
    global DEV_KEY
    global API_KEY
    USR = config.get("Settings", "USR")
    DEV_KEY = config.get("Settings", "DEV")
    API_KEY = config.get("Settings", "API")


# Parse the token file and get data.
parseToken()
PARAM = {"devkey":DEV_KEY, "apiuser":USR, "apikey":API_KEY}

# Function to unlock flag.
