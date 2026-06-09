
import pytesseract
from PIL import Image
from core.aesthetix import *
from core.system import *
from core.paths import *

pytesseract.pytesseract.tesseract_cmd = tess_path = r"C:\Applications__\pytesseract_ocr\tesseract.exe"

def ImageToString(image_path: str):
    """ returns a string from image """
    return pytesseract.image_to_string(Image.open(image_path))

def SavePDFromImageTo(image_path: str, destination_folder: str):
    """ saves pdf from image to destination specified by user """
    image_name = image_path.split("\\")[-1].split(".")[0]
    binary_pdf = pytesseract.image_to_pdf_or_hocr(Image.open(image_path))
    
    with open(destination_folder + "\\{}.pdf".format(image_name), "wb") as bin_file:
        bin_file.truncate(0)
        bin_file.write(binary_pdf)

def ImageToPDF(image_path: str):
    """ raw binary content of a pdf file from image file """
    return pytesseract.image_to_pdf_or_hocr(Image.open(image_path))


def create_gif(destination, images, fps=1):
    if type(images) != list:
        raise TypeError("param @images should be type list.")
    if type(destination) != str:
        raise TypeError("param @destination should be type str.")
    
    if not destination.endswith(".gif"):
        raise ValueError("param @destinaion should end with .gif extension.")
    
    import imageio
    images = [imageio.imread(image_abspath) for image_abspath in images]
    imageio.mimsave(destination, images, fps=fps)
    

def ImageInConsole(path):
    from PIL import Image
    import numpy as np
    def get_ansi_color_code(r, g, b):
        if r == g and g == b:
            if r < 8:
                return 16
            if r > 248:
                return 231
            return round(((r - 8) / 247) * 24) + 232
        return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)


    def get_color(r, g, b):
        return "\x1b[48;5;{}m \x1b[0m".format(int(get_ansi_color_code(r,g,b)))

    img = Image.open(path)
    print(img.size)

    height = 80
    width = int((img.width / img.height) * height)

    img = img.resize((width, height), Image.ANTIALIAS)
    img_array = np.asarray(img)
    print(img_array.shape)

    for h_index in range(height):
        for w_index in range(width):
            pix = img_array[h_index][w_index]
            print(get_color(pix[0], pix[1], pix[2]), sep='', end='')
        print()

if __name__ == '__main__':
    x = ImageToString("code.jpeg")
    print(x)