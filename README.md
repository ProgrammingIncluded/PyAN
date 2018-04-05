# PyAN
A simple Python interface for the AnimeNfo website.
Requires Python 3.5+

F12 to lock the commandline to prevent listening of global input.
This is a bug right now that occurs in Windows where input is received from global input.
So a lock option is provided.

## Setup Files
In order for the program to work, the user needs to provide a username, dev key, and write key.
Create a file named token.txt and write the following:
```
[Settings]
USR=username
DEV=developer_key
API=api_key
```

Replace username, developer_key, and api_key with your username and keys generated under account settngs on AnimeNfo.