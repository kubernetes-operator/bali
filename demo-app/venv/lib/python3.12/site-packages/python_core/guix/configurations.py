
from tkinter import *

# font configs
consolas_20_bold = ('Consolas', 20, 'bold')
consolas_30_bold = ('Consolas', 30, 'bold')
consolas_40_bold = ('Consolas', 40, 'bold')
consolas_50_bold = ('Consolas', 50, 'bold')
consolas_60_bold = ('Consolas', 60, 'bold')
abadi_45_bold = ("Abadi", 45, 'bold')

# colors
red = "red"
white = "white"
yellow = "yellow"
blue = "blue"
black = "black"
lightgreen = 'lightgreen'
gray32 = "gray32"
light_golden_rod = "light goldenrod"
gold="gold"
state_blue = "state blue"
indian_red = "indian red"

# window size
general_size = 600
screen_width = general_size
screen_height = general_size

# positioning on the screen
left_to_right = 700
up_to_down = 300
pos = (left_to_right, up_to_down)


def ConfigGUIObject(gui_object, just=CENTER, 
                    font=consolas_20_bold, back=white,
                    fore=blue):
    """ custom configs by andrew for gui objects """
    
    gui_object.config(justify=just)
    gui_object.config(font=font)
    gui_object.config(
        background=back, 
        foreground=fore
    )