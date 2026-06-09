
import os
import json
from core.system import *

def json_dumps(__json: dict, __indent=4):
    return json.dumps(__json, indent=__indent)

def read_json_from_file(source_path: str):
    """ reads .json from @source_path"""
    
    # validation
    if not os.path.isfile(source_path):
        raise ValueError
    
    # read
    return json.loads(open(source_path, "r", encoding="utf-8").read())
        
def write_json_to_file(__json: dict, destination_path: str):
    """ writes dict or list from @dumped_json to @destination_path"""
    
    # validation
    if not os.path.exists(destination_path):
        raise ValueError
    if type(__json) not in [dict, list]:
        raise TypeError
    
    # write
    open(destination_path, "w", encoding="utf-8").write(json.dumps(__json, indent=4))
    
def prettify(__collection, __indent=4):
    return json.dumps(__collection, indent=__indent)
    
def print_pretty(__collection, __indent=4):
    print(prettify(__collection, __indent=__indent))