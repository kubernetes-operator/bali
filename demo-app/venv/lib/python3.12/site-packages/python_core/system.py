
"""
    essential variables and functions that can be imported in other scripts
"""

import os
import sys
import cv2
import pyzbar
import platform
from time import sleep, time
from core.aesthetix import *
from core.numx import *

def colored_traceback():
    import colored_traceback
    colored_traceback.add_hook(always=True)

def clearscreen():
    os.system("cls")

def pauseprogram():
    enter = ConsoleColored("<enter>", "green", bold=1, underlined=1)
    input("press {} to continue...".format(enter))
    
def check_module(module_name: str):
    try:
        exec("import {}".format(module_name))
    except ImportError:
        print("ERROR: module {} not installed.\n".format(module_name))
        print("INFO: installing {}...".format(module_name))
        install_module(module_name)

def install_module(module_name: str):
    """ pip install @module_name """
    os.system("python -m pip install --upgrade pip")
    os.system("pip install {}".format(module_name))

def GetSourceCode(absolute_path):
    source_code = ""
    with open(absolute_path, 'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            source_code += line
            line = file.readline()
    return source_code

def PrintSourceCode(absolute_path):
    source_code = GetSourceCode(absolute_path)
    print(f"Source code for '{absolute_path}':")
    print("~" * 100)
    print(source_code)
    print("~" * 100)

def getIPinformation(ip_address):
    import ipinfo
    api = ipinfo.getHandler(access_token="9b88ceeca546c9")
    ip_information = api.getDetails(ip_address)
    content = ip_information.all
    return content

def get_device_name():
    return platform.node()
    
def get_operating_system():
    return platform.system()
    
def get_arhitecture():
    return platform.architecture()[0]
    
def get_python_version():
    return platform.python_version()
    
def get_python_implementation():
    return platform.python_implementation()
    
def get_processor():
    return platform.processor()

def get_python_interpreter_path():
    return sys.executable
    
def ProgressBar(iteration, length, decimals=2, progressbar_length=40, fill_symbol="█", color="yellow"):
    progress_percent = 100 * (iteration / float(length))
    progress_percent = fixed_set_precision_str(progress_percent, decimals)
    filled_length = int(progressbar_length * iteration // length)
    completed = fill_symbol * filled_length + "_" * (progressbar_length - filled_length)
    
    progressbar = f"[Progress]: |{completed}| [{progress_percent}] [Complete]"
    
    if iteration == length:
        progressbar = ConsoleColored(progressbar, "green")
    progressbar = ConsoleColored(progressbar, color)
    return progressbar
    
def LoadProgressBar(length=100, sleep_duration=0.045, color="yellow"):
    for i in range(length + 1):
        p = ProgressBar(i, length, color=color)
        print(p, end="\r")
        sleep(sleep_duration)
    print()
    
def DecodeQRcodeBARcode(absolute_path):
    if type(absolute_path) != str:
        raise TypeError("type should be string")
    
    if not os.path.isabs(absolute_path):
        raise ValueError("parametere is not absolute path")
    
    if not os.path.isfile(absolute_path):
        raise ValueError("something is wrong with this file")
    
    cv2image = cv2.imread(absolute_path)
    decoded = pyzbar.decode(cv2image)
    return decoded