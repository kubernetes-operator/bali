
import os
from core.system import *
from time import sleep
from string import Template
from core.aesthetix import *
from core.exceptionx import *
from win32com.client import Dispatch

current_file_path = Template("[file: {} ]".format(__file__))

def get_path_separator(source_path: str):
    """ return path separator (\\ or /) from @source_path """
    
    # means that it doesnt contains "\\"
    if source_path.split("\\")[0] == source_path:
        return "/"
        
    return "\\"

def read_from_copy_to(source_path: str, destination_path: str):
    """ reads from @source_path in binary and writes in binary to @destination_path""" 
    
    with open(source_path, "rb") as source_binary:
        with open(destination_path, "wb") as dest_binary:
            dest_binary.truncate(0)
            dest_binary.write(source_binary.read())
            
def copy_file(source_path: str, destination_path: str, __print=False):
    """ copys from source to destination (available only for FILES) 
        return True (means that code was executed successfully)
        
        prints output of code=0 to the screen if __print
    """
    
    # validation
    if not os.path.isfile(source_path):
        raise ValueError
    if not os.path.isabs(destination_path):
        raise ValueError
    
    # path separator
    path_separator = get_path_separator(source_path)
    __path_separator = get_path_separator(destination_path)
    if path_separator != __path_separator:
        raise PathSeparatorsDiffersError(current_file_path)
    
    del __path_separator
    
    # extensions
    source_filename_ext = source_path.split(path_separator)[-1]
    destination_filename_ext = destination_path.split(path_separator)[-1]
    
    # validation
    if source_filename_ext != destination_filename_ext:
        raise ValueError("not the same extension")
    
    # dest folder should exist in the first place
    # after that you can copy the file successfully
    try:
        read_from_copy_to(source_path, destination_path)
    except FileNotFoundError:
        # we need to create the folder
        folders = path_separator.join(destination_path.split(path_separator)[:-1])
        os.makedirs(folders)
        read_from_copy_to(source_path, destination_path)
        
    except Exception as error:
        # some error
        print_red_bold("something was wrong")
        print_red_bold(error)
        print_red_bold(type(error))
        return False
    
    if __print:
        print()
        print("[" + "=" * 50 + "]")
        print("source: {}".format(blue(source_path)))
        print("[~]")
        print("dest: {}".format(cyan(destination_path)))
        print("[~]")
        print(green_bold("file copied successfully!"))
        print("[" + "=" * 50 + "]")
        print()

    # true means that everything is working
    return True

def copy_folder(source_folder: str, destination_folder: str, __print=False, __folderignore=[]):
    """ copys from @source_folder to @destination_folder (available only for FOLDERS) 
    
        prints output of code=0 to the screen if __print
    """
    
    # validation
    if not os.path.isabs(source_folder) or not os.path.isabs(destination_folder):
        raise ValueError
    
    # path separator
    path_separator = get_path_separator(source_folder)
    __path_separator = get_path_separator(destination_folder)
    if path_separator != __path_separator:
        raise PathSeparatorsDiffersError(current_file_path)
    
    del __path_separator
    
    # iterating through __items in that folder
    for __item in os.listdir(source_folder):
        source_fullpath = source_folder + path_separator + __item
        dest_fullpath = destination_folder + path_separator + __item
        
        if os.path.isfile(source_fullpath):
            # copy process
            copy_file(source_fullpath, dest_fullpath, __print)
            
        elif os.path.isdir(source_fullpath):
            # recursivity here
            if __print:
                print()
                print("[" + "=" * 50 + "]")
                print("source: {}".format(blue(source_fullpath)))
                print("[~]")
                print("dest: {}".format(cyan(dest_fullpath)))
                print("[~]")
                print(green_bold("folder copied successfully!"))
                print("[" + "=" * 50 + "]")
                print()
            
            if __folderignore:
                __folderignore = [item for item in __folderignore if item != ""]
                if __item in __folderignore:
                    continue
            
            copy_folder(source_fullpath, dest_fullpath, __print, __folderignore)
        
    # if everything is ok
    return True
            

def is_file(source_path: str):
    """ is file and exists """
    return os.path.isfile(source_path)
    
def is_folder(source_path: str):
    """ is folder and exists """
    return os.path.isdir(source_path)

def is_abs(source_path: str):
    """ file or folder and doesnt need to exist """
    return os.path.isabs(source_path)
    
def exists(source_path: str):
    """ exists """
    return os.path.exists(source_path)

def create_shortcut(source_path: str, destination_folder: str,
                    shortcut_name: str, __print=False):
    """ 
        creates shortcut of @source_path and puts it into 
        @destination_folder with name @shortcut_name
        
        prints output of code=0 to the screen if __print
    """
    
    # path separator
    path_separator = get_path_separator(source_path)
    __path_separator = get_path_separator(destination_folder)
    if path_separator != __path_separator:
        raise PathSeparatorsDiffersError(current_file_path.safe_substitute(index=48))
    
    del __path_separator
    
    working_directory = path_separator.join(source_path.split(path_separator)[:-1])

    # modifications
    if destination_folder.endswith(path_separator):
        # @destination_folder has a "" at the end
        destination_folder = destination_folder[:-1]
        
    destination_folder += path_separator + shortcut_name + ".lnk"

    # creation of shortcut
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(destination_folder)
    shortcut.TargetPath = source_path
    shortcut.WorkingDirectory = working_directory
    shortcut.IconLocation = source_path
    shortcut.save()
    
    if __print:
        print()
        print("[" + "=" * 50 + "]")
        print("source: {}".format(blue(source_path)))
        print("[~]")
        print("destination: {}".format(cyan(destination_folder)))
        print("[~]")
        print(green_bold("was made shortcut successfully!"))
        print("[" + "=" * 50 + "]")
        print()

def get_path_from_absolute(source_path: str):
    """ extracts the path from @source_path
    
        "folder1/folder2/folder3/folder4/file_name.extension" =>
        => "folder1/folder2/folder3/folder4"
    """
    
    # validation
    if type(source_path) != str:
        raise TypeError("param @source_path should be type str.")
    if not os.path.isabs(source_path):
        raise ValueError("param @source_path should be an absolute path.")
    
    path_separator = get_path_separator(source_path)
    return path_separator.join(source_path.split(path_separator)[:-1])
    
def is_folder_empty(source_folder: str):
    """ tests whether the @source_folder is empty or not
    
        return True or False
    """
    
    # validation
    if type(source_folder) != str:
        raise TypeError("param @source_folder should be type str.")
    if not is_folder(source_folder):
        raise NotADirectoryError(current_file_path.safe_substitute(index=216))
    
    return os.listdir(source_folder) == 0

def get_file_name(source_path: str):
    """ "folder1/folder2/folder3/folder4/file_name.extension" => file_name """
    
    # validation
    if type(source_path) != str:
        raise TypeError("param @source_folder should be type str.")
    if is_folder(source_path):
        raise NotAFileError(current_file_path.safe_substitute(index=237))
    
    path_separator = get_path_separator(source_path)
    
    # noisnetxe.eman_elif
    full_file_name_rev = source_path.split(path_separator)[-1][::-1]
    # file_name
    file_name = full_file_name_rev[full_file_name_rev.index(".") + 1: ][::-1]
    
    return file_name
            
def get_file_extension(source_path: str):
    """ "folder1/folder2/folder3/folder4/file_name.extension" => extension """
    
    # validation
    if type(source_path) != str:
        raise TypeError("param @source_path should be type str.")
    if not is_file(source_path):
        raise NotAFileError(current_file_path.safe_substitute(index=235))
    
    # reading backwards
    extension = ""
    for char in source_path[::-1]:
        if char == ".":
            break
        extension += char
    
    return extension[::-1]
    
def get_filename_plus_extension(source_path: str):
    """ "folder1/folder2/folder3/folder4/file_name.extension" => file_name.extension """
    
    # validation
    if type(source_path) != str:
        raise TypeError("param @source_path should be type str.")
    if not is_file(source_path):
        raise NotAFileError(current_file_path.safe_substitute(index=253))
    
    path_separator = get_path_separator(source_path)
    return source_path.split(path_separator)[-1]
    




class File:
    def __init__(self, absolutePATH):
        if not os.path.isfile(absolutePATH):
            message = "your file doesnt exist.\n"
            message += absolutePATH + "\n"
            raise InterruptedError(ConsoleColored(message, "red", bold=1))
            del message
        
        self.contains_backslash = True
        self.separator = "\\"
        if "/" in absolutePATH:
            self.contains_backslash = False
            self.separator = "/"
        
        # full path
        self.absolutePATH = absolutePATH
        
        __items = self.absolutePATH.split(self.separator)
        
        # __folder of provenience
        self.__folder = self.separator.join(__items[:len(__items) - 1])
        
        # filename + extension
        self.full_filename = __items[len(__items) - 1]
        
        __items = self.full_filename.split(".")
        
        # just filename
        self.filename = __items[0]
        # just extension
        self.extension = get_file_extension(self.full_filename)
        
    def TestCorruption(self):
        # testing corruption in file
        originalWD = os.getcwd()
        os.chdir(self.__folder)
        
        from zipfile import ZipFile
        with ZipFile("{}.zip".format(self.filename), "w") as file_zip:
            file_zip.write(self.filename)
            if file_zip.testzip() is None:
                self.corrupted = False
            else:
                self.corrupted = True
                
        os.remove("{}.zip".format(self.filename))
        os.chdir(originalWD)
        return self.corrupted
        
    def __str__(self):
        content = "<class '{}'>\n".format(ConsoleColored("File", "yellow", bold=1))
        content += "\tfile from path: {}\n".format(ConsoleColored(self.absolutePATH, "blue", bold=1, underlined=1))
        content += "</class '{}'>\n".format(ConsoleColored("File", "yellow", bold=1))
        return content

def ColorExtension(ext: str):
    if ext == "json":
        return ConsoleColored(ext, "yellow", bold=1)
    elif ext == "py":
        p = ConsoleColored("p", "blue", bold=1)
        y = ConsoleColored("y", "yellow", bold=1)
        return p + y
    elif ext == "txt":
        return ConsoleColored(ext, "blue", bold=1)
    elif ext == "pyc":
        return ConsoleColored(ext, "darkcyan", bold=1)
    
    return ConsoleColored(ext, "white", bold=1)
    
def GetFileTypeColored(source_path):
    file = File(source_path)
    if file.extension == "py":
        python = ConsoleColored("Python", "blue", bold=1)
        file = ConsoleColored("File", "yellow", bold=1)
        left_bracket = ConsoleColored("[", "yellow", bold=1)
        right_bracket = ConsoleColored("]", "blue", bold=1)
        
        return "{}{} {}{}".format(left_bracket, python, file, right_bracket)
        
    elif file.extension == "txt":
        return ConsoleColored("[{}]".format("Text File"), "blue", bold=1)
        
    elif file.extension == "json":
        return ConsoleColored("[{}]".format("JSON File"), "orange", bold=1)
        
    elif file.extension == "jpg" or file.extension == "jpeg" or file.extension == "png":
        return ConsoleColored("[{}]".format("Image File"), "green", bold=1)
        
    elif file.extension == "pyc":
        return ConsoleColored("[{}]".format("Python Cache"), "grey", bold=1)
        
    elif file.extension == "pickle":
        return ConsoleColored("[{}]".format("Binary File"), "cyan", bold=1)
    
space  = " " * 4
branch = '│   '
tee    = '├───'
final  = '└───'

def tree__(__folder: str, prefix: str=" " * 4):
    representation = ""
    if os.path.isdir(__folder):
        contents = os.listdir(__folder)
        pointers = [tee] * (len(contents) - 1) + [final]
        
        for pointer, content in zip(pointers, contents):
            fullpath = __folder + "\\" + content
            
            if os.path.isdir(fullpath):
                content = ConsoleColored("[{}]".format(content), "yellow", bold=1)
            else: 
                filetype = GetFileTypeColored(fullpath)
                if filetype:
                    content += " " + filetype
                    
            representation += prefix + pointer + content + "\n"
            
            if os.path.isdir(fullpath):
                extension = branch if pointer == tee else space
                representation += tree__(fullpath, prefix + extension)
                
    return representation

def PrintTree(__folder: str, prefix: str=" " * 4):
    if os.path.isdir(__folder):
        try:
            contents = os.listdir(__folder)
            pointers = [tee] * (len(contents) - 1) + [final]
            
            for pointer, content in zip(pointers, contents):
                fullpath = __folder + "\\" + content
                
                if os.path.isdir(fullpath):
                    content = ConsoleColored("[{}]".format(content), "yellow", bold=1)
                else: 
                    filetype = GetFileTypeColored(fullpath)
                    if filetype:
                        content += " " + filetype
                        
                print(prefix + pointer + content)
                
                if os.path.isdir(fullpath):
                    extension = branch if pointer == tee else space
                    PrintTree(fullpath, prefix + extension)
                    
        except PermissionError:
            pass
        except FileNotFoundError:
            pass

def tree_representation(__folder):
    print(ConsoleColored("\ncomputing tree represenation...", "yellow", bold=1))
    represenation = ConsoleColored("[{}]\n".format(__folder), "blue", bold=1, underlined=1)
    
    represenation += tree__(__folder)
    # PrintYellowBOLD("\ndone.\n")
    sleep(.5)
    clearscreen()
    return represenation

class Folder:
    def __init__(self, __folder: str):
        if not os.path.isdir(__folder):
            raise InterruptedError
        
        self.__folder = __folder
        self.__items = os.listdir(self.__folder)
        
        self.contains_backslash = True
        self.separator = "\\"
        if "/" in __folder:
            self.contains_backslash = False
            self.separator = "/"
        
        self.__folderNAME = self.__folder.split(self.separator)
        self.__folderNAME = self.__folderNAME[len(self.__folderNAME) - 1]
        
    def TreeRepresentation(self):
        print(ConsoleColored("\ncomputing tree represenation...", "yellow", bold=1))
        represenation = ConsoleColored("[{}]\n".format(self.__folderNAME), "blue", bold=1, underlined=1)
        
        represenation += tree__(self.__folder)
        # PrintYellowBOLD("\ndone.\n")
        sleep(.5)
        clearscreen()
        return represenation
    
    def SaveTreeRepresentation(self, location: str):
        if not os.path.isabs(location):
            raise ValueError
        
        content = self.__folderNAME + "\n" + tree__(self.__folder)
        content = delete_ansi_escape_codes(content)
        
        with open(location, "w+", encoding="utf-8") as file:
            file.truncate(0)
            file.write(content)
            
        # PrintYellowBOLD("tree representation of __folder:")
        # PrintYellowBOLD("\t{}".format(self.__folder))
        # PrintYellowBOLD("saved successfully.")
    
    def __str__(self):
        return ConsoleColored(self.__folder, "yellow", bold=1, underlined=1)

# testing
if __name__ == '__main__':
    pass