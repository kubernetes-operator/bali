
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
vox_path = "C:/Users/{}/sounds/vox".format(username)


# audio folders
original_remote_folder = vox_path + "/original"
modified_remote_folder = vox_path + "/modified"


# database
remote_sounds_json_path = vox_path + "/sounds.json"


# if the remote location doesnt exist
Initialize(
    vox_path, 
    original_remote_folder, 
    modified_remote_folder, 
    remote_sounds_json_path,
    "vox")


# reading remote database
sounds_json = read_json_from_file(remote_sounds_json_path)

# importing play function
from core.sounds.play import *


# =========== variety of vox sounds system ===============

def access_denied():
    print(ConsoleColored("Access denied!", "red", bold=1))
    commands = ["access", "denied"]
    play_commands(sounds_json, *commands)

def access_granted():
    print(ConsoleColored("Access granted!", "green", bold=1))
    commands = ["access", "granted"]
    play_commands(sounds_json, *commands)
    
def you_are_authorized_to(action="proceed", __not=0):
    commands = ["you", "are", "authorized", "to", action]
    if __not:
        print(ConsoleColored("You are unauthorized to {}.".format(action), "red", bold=1))
        commands[2] = "unauthorized"
    else:
        print(ConsoleColored("You are authorized to {}.".format(action), "green", bold=1))

    play_commands(sounds_json, *commands)

def system_is_down():
    print(ConsoleColored("System is down.", "red", bold=1))
    commands = ["system", "is", "down"]
    play_commands(sounds_json, *commands)

def command_is_forbidden():
    print(ConsoleColored("Command is forbidden.", "yellow", bold=1))
    commands = ["command", "is", "forbidden"]
    play_commands(sounds_json, *commands)

def command_is_invalid():
    print(ConsoleColored("Command is invalid.", "yellow", bold=1))
    play_commands("command", "is", "invalid")

def intruder_is_detected():
    print(ConsoleColored("Intruder is detected.", "yellow", bold=1))
    commands = ["Intruder", "is", "detected"]
    play_commands(sounds_json, *commands)

digits = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten"
}

def countdown(start=10, color="yellow", __pause=.4):
    if start > 10:
        raise ValueError("this cannot be > 10")
    
    for i in range(start, -1, -1):
        print("[  {}  ]".format(ConsoleColored(str(i), color, bold=1)))
            
        playaudio(sounds_json[digits[i]])
        sleep(__pause)

def countdown_allarm(start=10, color="yellow", __pause=.4):
    if start > 10:
        raise ValueError("this cannot be > 10")
    
    allarm_thread = threading.Thread(target=play_commands, args=("death-star-allarm",))
    allarm_thread.start()
    
    countdown(start, color, __pause)
        
    # i dont know how to kill the allarm thread
    # cuz has 22 seconds and the countdown has max 10 seconds
    # solution:
    # crop the allarm from 22 to 10 seconds, easy

def detonation_activated():
    print(ConsoleColored("[[[ Detonation activated ]]].", "red", bold=1))
    play_commands("detonation", "activated", "ten", "seconds", "remaining")
    countdown_allarm(color="red")

def computer_is_loading():
    print(ConsoleColored("Computer is loading...", "green", bold=1))
    play_commands("computer", "is", "loading")

def computer_is_under_control():
    print(ConsoleColored("Computer is under control.", "green", bold=1))
    play_commands("computer", "is", "under", "control")

def malfunction_detected():
    print(ConsoleColored("Malfunction detected.", "yellow", bold=1))
    play_commands("malfunction", "detected")
    
def you_are_an_idiot():
    print(ConsoleColored("You are an idiot.", "blue", bold=1))
    play_commands("you", "are", "an", "idiot")
    
def decompression_activated():
    print(ConsoleColored("Decompression activated...", "yellow", bold=1))
    play_commands("decompression", "activated")
    
def level_unlocked():
    print(ConsoleColored("Level unlocked.", "green", bold=1))
    play_commands("level", "unlocked")
    

# testing project
if __name__ == '__main__':
    
    # access_denied()
    
    
    pass