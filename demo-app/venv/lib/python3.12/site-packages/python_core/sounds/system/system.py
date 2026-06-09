
import os
from time import sleep
from core.audiox import *
from core.jsonx import *
from core.aesthetix import ConsoleColored
from core.pathx import *
import threading
from getpass import getuser
from core.sounds.update import *


username = getuser()
# this path is indepedent on windows
# can be called no matter what value of current working directory
system_path = "C:/Users/{}/sounds/system".format(username)


# audio folders
original_remote_folder = system_path + "/original"
modified_remote_folder = system_path + "/modified"


# database
remote_sounds_json_path = system_path + "/sounds.json"

# if the remote location doesnt exist
Initialize(
    system_path, 
    original_remote_folder, 
    modified_remote_folder, 
    remote_sounds_json_path,
    "system")
    

# reading remote database
sounds_json = read_json_from_file(remote_sounds_json_path)

# importing play function
from core.sounds.play import *

# =========== variety of system sounds ===============

def allahu_akbar():
    play_commands(sounds_json, "allahu")
    
def windows98_error():
    play_commands(sounds_json, "error")
    
def electric_pulse():
    play_commands(sounds_json, "pulse")
    
def windows98_remix():
    play_commands(sounds_json, "remix")

def shutdown_sound():
    play_commands(sounds_json, "shutdown")

def welcome_back():
    play_commands(sounds_json, "welcome")


# testing project
if __name__ == '__main__':
    windows98_error()
    windows98_error()
    windows98_error()
    windows98_remix()