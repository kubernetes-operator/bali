

from datetime import datetime
date_format = "%d.%m.%Y"
time_format = "%H:%M:%S"

datetime_format = "{} - {}".format(date_format, time_format)
timedate_format = "{} - {}".format(time_format, date_format)

def is_valid_date(date_str: str):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except:
        return False
        
def is_valid_time(time_str: str):
    try:
        datetime.strptime(time_str, time_format)
        return True
    except:
        return False