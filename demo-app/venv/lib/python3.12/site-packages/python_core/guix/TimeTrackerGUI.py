
from datetime import datetime
from datedelta import datedelta
from tkinter import *
from core.guix.GUIObjects import *

date_selected = "01.10.2020"

# window size
screen_width = 340
screen_height = 150
dim = (screen_width, screen_height)

# positioning on the screen
left_to_right = 700
up_to_down = 300
pos = (left_to_right, up_to_down)

# <<<style>>>
# font: type and size and (bold or itallic)
font_config = ('Consolas', 20, 'bold')
background_color = "yellow"
foreground_color = "blue"

# buttons config
button_back = 'lightgreen'
button_fore = 'blue'
button_config = ('Consolas', 40, 'bold')

datetime_format = "%d.%m.%Y"

window = Tk()
window.title("TimeTracker")
window.geometry(f"{dim[0]}x{dim[1]}+{pos[0]}+{pos[1]}")

information_label0 = NewLabelWithBorder(window, "You have left", TOP, 3, "solid")
information_label0.config(font=font_config)
information_label0.config(justify=LEFT)
information_label0.config(foreground=foreground_color,
                                background=background_color)

information_label1 = NewLabelWithBorder(window, "__time until exam__", TOP, 3, "solid")
information_label1.config(font=font_config)
information_label1.config(justify=LEFT)
information_label1.config(foreground=foreground_color,
                                background=background_color)
current_time = datetime.now()
exam_date = datetime.strptime(date_selected, datetime_format)
remaining_days = (exam_date - current_time).days
remaining_hours = (exam_date - current_time).total_seconds() // 60 // 60
information = f"{remaining_days} days ||| {int(remaining_hours)} hours"
information_label1.config(text=information)

information_label0 = NewLabelWithBorder(window, f"until date: {date_selected}", TOP, 3, "solid")
information_label0.config(font=font_config)
information_label0.config(justify=LEFT)
information_label0.config(foreground=foreground_color,
                                background=background_color)

if __name__ == '__main__':
    window.mainloop()