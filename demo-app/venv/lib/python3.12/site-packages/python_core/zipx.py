
import os
import zipfile

def unzip(zipfilePATH, folder):
    if not os.path.isfile(zipfilePATH):
        raise ValueError
    if not os.path.isdir(folder):
        raise ValueError
    
    with zipfile.ZipFile(zipfilePATH, "r") as file:
        file.extractall(folder)
    
def ZIPFiles(files, zipname):
    if type(files) == list:
        for file in files:
            if not os.path.isfile(file):
                raise ValueError
    elif type(files) == str:
        if not os.path.isfile(files):
            raise ValueError
        files = [files]
        
    sep = "/" if "/" in files[0] else "\\" 
    working_directory = files[0].split(sep)
    working_directory = sep.join(working_directory[:len(working_directory) - 1])
    
    
    wd_name = working_directory.split(sep)
    wd_name = wd_name[len(wd_name) - 1]
    for file in files:
        items = file.split(sep)
        folder_name = items[len(items) - 2]
        if folder_name != wd_name:
            print(folder_name)
            print(working_directory)
            raise ValueError("files should be from the same directory.")
    
    originalWD = os.getcwd()
    os.chdir(working_directory)
    
    items = [file.split(sep) for file in files]
    # just the filename
    files = [item[len(item) - 1] for item in items]
            
    with zipfile.ZipFile("{}.zip".format(zipname), "w") as filesZIP:
        for file in files:
            filesZIP.write(file)
    print("{}.zip created successfully.".format(zipname))
    return working_directory + "\\" + zipname + ".zip"

def ZIPFolder(folder, zipname):
    if not os.path.isdir(folder):
        raise ValueError
    
    originalWD = os.getcwd()
    os.chdir(folder)
    files = os.listdir(folder)
    
    with zipfile.ZipFile("{}.zip".format(zipname), "w") as file_zip:
        for file in files:
            file_zip.write(file)
    os.chdir(originalWD)
    
    print("{}.zip created successfully.".format(zipname))
    return folder + "\\" + zipname + ".zip"