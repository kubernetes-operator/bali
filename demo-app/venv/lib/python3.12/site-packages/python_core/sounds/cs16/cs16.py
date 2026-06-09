
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
cs16_path = "C:/Users/{}/sounds/cs16".format(username)


# audio folders
original_remote_folder = cs16_path + "/original"
modified_remote_folder = cs16_path + "/modified"


# database
remote_sounds_json_path = cs16_path + "/sounds.json"

# if the remote location doesnt exist
Initialize(
    cs16_path, 
    original_remote_folder, 
    modified_remote_folder, 
    remote_sounds_json_path,
    "cs16")
    
# reading remote database
sounds_json = read_json_from_file(remote_sounds_json_path)

# importing play function
from core.sounds.play import *

# =========== variety of cs16 sounds ===============

def arcade_sound():
    play_commands(sounds_json, "arcade")

def break_sound():
    play_commands(sounds_json, "break")

def davai_sound():
    play_commands(sounds_json, "davai")

def dominating_sound():
    play_commands(sounds_json, "dominating")

def doublekill_sound():
    play_commands(sounds_json, "doublekill")

def eagleeye_sound():
    play_commands(sounds_json, "eagleeye")

def excellent_sound():
    play_commands(sounds_json, "excellent")

def explosion_sound():
    play_commands(sounds_json, "explosion")

def firstblood_sound():
    play_commands(sounds_json, "firstblood")

def flawless_sound():
    play_commands(sounds_json, "flawless")

def godlike_sound():
    play_commands(sounds_json, "godlike")

def hattrick_sound():
    play_commands(sounds_json, "hattrick")

def headhunter_sound():
    play_commands(sounds_json, "headhunter")

def headshot_sound():
    play_commands(sounds_json, "headshot")

def here_comes_the_money_sound():
    play_commands(sounds_json, "here_comes_the_money")

def holyshit_sound():
    play_commands(sounds_json, "holyshit")

def humiliating_defeat_sound():
    play_commands(sounds_json, "humiliating_defeat")

def humiliating_sound():
    play_commands(sounds_json, "humiliating")

def humiliation_sound():
    play_commands(sounds_json, "humiliation")

def killingmachine_sound():
    play_commands(sounds_json, "killingmachine")

def killingspree_sound():
    play_commands(sounds_json, "killingspree")

def ludicrouskill_sound():
    play_commands(sounds_json, "ludicrouskill")

def massacre_sound():
    play_commands(sounds_json, "massacre")

def megakill_sound():
    play_commands(sounds_json, "megakill")

def monsterkill_sound():
    play_commands(sounds_json, "monsterkill")

def moonlight_sound():
    play_commands(sounds_json, "moonlight")

def multikill_sound():
    play_commands(sounds_json, "multikill")

def ownage_sound():
    play_commands(sounds_json, "ownage")

def payback_sound():
    play_commands(sounds_json, "payback")

def pick_up_your_weapons_and_fight_sound():
    play_commands(sounds_json, "pick_up_your_weapons_and_fight")

def play_sound():
    play_commands(sounds_json, "play")

def prepare_for_battle_sound():
    play_commands(sounds_json, "prepare_for_battle")

def prepare_to_fight_sound():
    play_commands(sounds_json, "prepare_to_fight")

def rampage_sound():
    play_commands(sounds_json, "rampage")

def respect_sound():
    play_commands(sounds_json, "respect")

def retribution_sound():
    play_commands(sounds_json, "retribution")

def suka_sound():
    play_commands(sounds_json, "suka")

def suprise_motafaca_sound():
    play_commands(sounds_json, "suprise_motafaca")

def triplekill_sound():
    play_commands(sounds_json, "triplekill")

def ultrakill_sound():
    play_commands(sounds_json, "ultrakill")

def unstoppable_loud_sound():
    play_commands(sounds_json, "unstoppable_loud")

def unstoppable_sound():
    play_commands(sounds_json, "unstoppable")

def where_the_hood_at_sound():
    play_commands(sounds_json, "where_the_hood_at")

def whickedsick_sound():
    play_commands(sounds_json, "whickedsick")

# testing project
if __name__ == '__main__':
    
    godlike_sound()
    unstoppable_sound()