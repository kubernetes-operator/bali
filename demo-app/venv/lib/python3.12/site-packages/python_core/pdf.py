

import os
import pdfplumber
from PIL import Image
from core.system import *
from string import ascii_letters, digits, punctuation
from core.aesthetix import ConsoleColored, underlined

def HasImageExtension(filename):
    ext = filename.split(".")[1]
    image_extensions = ["jpg", "jpeg", "png", "JPG", "JPEG", "PNG"]
    if ext in image_extensions:
        return True
    return False

def GetTextFromPDF(__pdfpath: str):
    human_readable_chars = ascii_letters + digits + punctuation
    human_readable_chars = list(human_readable_chars) + ["\n", "\t", " "]

    __pdftext = ""
    check_module("pdfplumber")
    with pdfplumber.open(__pdfpath) as pdf:
        for page in pdf.pages:
            modified_text = ""
            for char in page.extract_text():
                if char in human_readable_chars:
                    modified_text += char
            __pdftext += modified_text
    return __pdftext
    
def PythonPrintToPDF(images_paths, PDFName):
    print("PythonPrintToPDF: processing...")
    
    # list with different paths with images
    if type(images_paths) == list:
        folder_path = images_paths[0].split("\\")
        folder_path = "\\".join(folder_path[:len(folder_path) - 1])
        ImagesArray = [Image.open(img).convert("RGB") for img in images_paths]
        
        print(ConsoleColored("merging photo(s) into pdf...", "yellow", bold=1))
        
        ImagesArray[0].save(folder_path + f"\\{PDFName}.pdf", save_all=True, append_images=ImagesArray[1:])
        location = folder_path
    
    # string parameter
    elif type(images_paths) == str:
        
        # folder with images
        if os.path.isdir(images_paths):
            pdf_path = images_paths + "\\{}.pdf".format(PDFName)
            
            if os.path.isfile(pdf_path):
                print(ConsoleColored("warning: pdf already existent.", "red", bold=1))
                os.remove(pdf_path)
                print(ConsoleColored("Existent pdf was deleted.", "red", bold=1))
            
            del pdf_path
            
            photos = [file for file in os.listdir(images_paths) if os.path.isfile(images_paths + "\\" + file) and HasImageExtension(file)]
            
            if photos == []:
                raise ValueError(ConsoleColored("folder has no photos.", "red", bold=1))
            
            imgs = [images_paths + "\\" + p for p in photos]
            ImagesArray = [Image.open(img).convert("RGB") for img in imgs]
            
            print(ConsoleColored("merging photo(s) into pdf...", "yellow", bold=1))
            
            ImagesArray[0].save(images_paths + f"\\{PDFName}.pdf", save_all=True, append_images=ImagesArray[1:])
            location = images_paths
            
        # only one image
        elif os.path.isfile(images_paths):
            folder_path = images_paths.split("\\")
            folder_path = "\\".join(folder_path[:len(folder_path) - 1])
            image = Image.open(images_paths).convert("RGB")
            
            print(ConsoleColored("merging photo(s) into pdf...", "yellow", bold=1))
            
            image.save(folder_path + f"\\{PDFName}.pdf")
            location = folder_path
            
    PDFName += ".pdf"
    successfully = ConsoleColored("successfully", "green", bold=1)
    print("pdf with name {} created {}.".format(ConsoleColored(PDFName, "cyan", bold=1, underlined=1), successfully))
    location += "\\" + PDFName
    
    print("located on: {}".format(ConsoleColored(location, "yellow", bold=1, underlined=1)))
    os.system(location)
    
def PDFsMerger(pathx: str, pathy: str, dest_folder: str):
    from PyPDF2.merger import PdfFileMerger
    
    merger = PdfFileMerger()
    merger.append(pathx)
    merger.append(pathy)
    
    name_pathx = pathx.split("\\")[-1].split(".")[0]
    name_pathy = pathy.split("\\")[-1].split(".")[0]
    
    merger.write("{}\\{}_{}_merged.pdf".format(dest_folder, name_pathx, name_pathy))
    merger.close()