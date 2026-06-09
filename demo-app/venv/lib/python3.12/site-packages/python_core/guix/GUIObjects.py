
from tkinter import *

def NewFrame(tkinter_object, position, expand=YES, fill=BOTH):
    frame = Frame(tkinter_object)
    frame.pack(side=position, expand=expand, fill=fill)
    return frame

def NewButton(tkinter_object, button_text, function, position, expand=YES, fill=BOTH):
    button = Button(tkinter_object, text=button_text, command=function)
    button.pack(side=position, expand=expand, fill=fill)
    return button

def NewLabel(tkinter_object, label_text, position, expand=YES, fill=BOTH):
    label = Label(tkinter_object, text=label_text)
    label.pack(side=position, expand=expand, fill=fill)
    return label

def NewLabelWithBorder(tkinter_object, label_text, position, borderwidth=2, relief="solid", expand=YES, fill=BOTH):
    label = Label(tkinter_object, text=label_text, borderwidth=borderwidth, relief=relief)
    label.pack(side=position, expand=expand, fill=fill)
    return label