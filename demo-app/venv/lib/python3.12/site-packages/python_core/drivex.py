
from core.system import *
import os
import string
from win32 import win32api
from core.pathx import *
from core.aesthetix import *
import threading
from time import time, sleep
import multiprocessing
from core.WindowsAPIX import *
from core.numx import *
from core.exceptionx import *

def get_available_drives():
    """ gets all available drives that you can put files on """
    
    # drives = []
    # bitmask = win32api.GetLogicalDrives()
    # for letter in string.ascii_uppercase:
    #     if bitmask & 1:
    #         drives.append("{}:\\".format(letter))
    #     bitmask >>= 1
    return win32api.GetLogicalDriveStrings().split("\000")[:-1]

def is_flash_drive(path: str):
    """ checks if a drive is USB-drive or NOT """
    
    try:
        os.listdir(path)
        return True
    except PermissionError:
        return False
        
def get_available_drives_non_usb():
    drives = []
    for d in get_available_drives():
        if is_flash_drive(d):
            drives.append(d)
    return drives
    
def open_folder(source_path: str):
    """ opens folder in file explorer"""

    # validation
    if not is_abs(source_path):
        raise ValueError
    if not is_folder(source_path):
        raise NotADirectoryError
    
    ops = get_operating_system()
    if ops == "Windows":
        os.system("explorer.exe {}".format(source_path))
    elif ops == "Linux":
        pass
    elif ops == "Mac":
        pass
    
def open_file(source_path: str):
    """ opens file in file explorer """
    
    # validation
    if not is_abs(source_path):
        raise ValueError
    if not is_file(source_path):
        raise NotAFileError
    
    ops = get_operating_system()
    if ops == "Windows":
        os.system(source_path)
    elif ops == "Linux":
        pass
    elif ops == "Mac":
        pass

class FileFoundError(Exception):
    pass

def find_file_on_drive(wanted_file: str, path: str):
    return_path = ""

    search_threads = []
    try:
        __items = os.listdir(path)
        for item in __items:
            full_path = path + "\\" + item
            
            if is_folder(full_path):
                print_red(full_path)
                search_thread = threading.Thread(target=__find_file_on_drive, args=(wanted_file, full_path, return_path))
                
                search_threads.append(search_thread)
                
                # search_process = multiprocessing.Process(target=__find_file_on_drive, args=(wanted_file, full_path, return_path))
                # search_process.start()
                
            elif is_file(full_path):
                if wanted_file == item:
                    print_green("\nfile found!\n")
                    print("located on: {}".format(blue_underlined(path)))
                    
                    return full_path
                
    except NotADirectoryError:
        if wanted_file == path.split("\\")[-1]:
            print_green_bold("\nfile found!\n")
            print("located on: {}".format(blue_underlined(path)))
            return path
            
    except PermissionError:
        pass
    
    if search_threads != []:
        for st in search_threads:
            print(st)
        
        try:
            for st in search_threads:
                st.start()
                
            for st in search_threads:
                st.join()
                
        except FileFoundError:
                    
            pass
        
    return False

def __find_file_on_drive(wanted_file: str, path: str, return_path: str=""):
    try:
        __items = os.listdir(path)
        for item in __items:
            full_path = path + "\\" + item
            
            if is_folder(full_path):
                print_red(full_path)
                # sleep(1)
                __find_file_on_drive(wanted_file, full_path)
                
            elif is_file(full_path):
                if wanted_file == item:
                    print_green(full_path)
                    
                    print_green_bold("\n\nfile found!")
                    print("located on: {}\n\n".format(blue_underlined(full_path)))
                    
                    return_path = full_path
                    Windows10Notification("drive", "{}".format(green_bold(full_path)), 20, "")
                    
                
                else:
                    print_red(full_path)
                    pass
            
    except NotADirectoryError:
        if wanted_file == path.split("\\")[-1]:
            print_green_bold("\nfile found!\n")
            print("located on: {}".format(blue_underlined(path)))
            return
            
    except PermissionError:
        # this is a system folder
        pass

    # this function didnt succeeded
    # in finding the wanted file

# testing
if __name__ == '__main__':
    starting_folder = "D:/"
    wanted_file = "FileFinder.py"
    
    before = time()
    
    path = find_file_on_drive(wanted_file, starting_folder)
    print(path)
    
    execution_time = time() - before
    execution_time = fixed_set_precision_float(execution_time, 2)
    print("execution time: [ {} second(s) ]".format(yellow_bold(execution_time)))