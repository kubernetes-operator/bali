
import os
from core.audiox import ModifyVolume
from core.jsonx import *
from core.pathx import *


def UpdateSounds(original_remote_folder: str, 
                 modified_remote_folder: str, 
                 remote_sounds_json_path: str):
    """ 
        modifies every original sound with -15 dB and puts all the files into modified folder.
        
        if modified folder has items inside, will be deleted and replaced with brand new ones.
    """
    
    # verifying if is empty
    __items = os.listdir(modified_remote_folder)
    if __items != []:
        for file in __items:
            os.remove(modified_remote_folder + "/" + file)
    
    # saving all paths from original folder
    files = [
        original_remote_folder + "/" + file for file in os.listdir(original_remote_folder) if is_file((original_remote_folder + "/" + file))
    ]
    
    # -15 dB for every file in the original folder
    for f in files:
        ModifyVolume(f, modified_remote_folder, quantity=-15)
    
    # creating a json with paths for every modified sound
    sounds_modified_json = {}
    for file in os.listdir(modified_remote_folder):
        name = file.split("_")[0]
        sounds_modified_json[name] = modified_remote_folder + "/" + file
        
    # writing sounds json to disk
    write_json_to_file(sounds_modified_json, remote_sounds_json_path)


def Initialize(remote_path: str, original_remote_folder: str, modified_remote_folder: str, remote_sounds_json_path: str, type: str):
    
    # creation of sounds files and folder for the first time
    if not exists(remote_path):
        # creating folders
        os.makedirs(original_remote_folder)
        os.makedirs(modified_remote_folder)
        
        # creating sounds.json in current C:/Users/$username/sounds/$type
        with open(remote_sounds_json_path, "x+", encoding="utf-8") as f:
            f.truncate(0)
            f.write("{}")
            
        # copy the files from type/original to C:/Users/$username/sounds/$type/original
        sep = get_path_separator(__file__)
        original_folder = sep.join(__file__.split(sep)[:-1]) + f"/{type}/original"
        
        __sounds = os.listdir(original_folder)
        for s in __sounds:
            copy_file(original_folder + sep + s, original_remote_folder + sep + s, __print=True)
        
        # after creating the folders for the first time
        # also create the modified sounds
        # in order to be ready with everything
        UpdateSounds(
            original_remote_folder,
            modified_remote_folder,
            remote_sounds_json_path
        )