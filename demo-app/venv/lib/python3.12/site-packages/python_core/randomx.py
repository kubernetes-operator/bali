
"""
    useful random stuff to import in your scripts
    contents (random):
        lowchar
        upperchar
        digit
        number
        lowerstring
        upperstring
        string
        date
"""

# Unicode codes
# a-z 97-122
# A-Z 65-90
# 0-9 48 57

from random import randint, choice, random
from datetime import datetime
import time

random_lowerchar = lambda : chr(randint(97, 122))
random_upperchar = lambda : chr(randint(65, 90))
random_digit = lambda : randint(0, 9)

def RandomDigits(dimension):
    if dimension is None:
        raise TypeError
    if dimension <= 0:
        raise ValueError
    return "".join([str(randint(0, 9)) for _ in range(dimension)])

def RandomNumber(dimension):
    if dimension is None:
        raise TypeError
    if dimension <= 0:
        raise ValueError
    return int(str(randint(1, 9)) + "".join([str(randint(0, 9)) for _ in range(dimension - 1)]))

def RandomLowerString(dimension):
    if dimension is None:
        raise TypeError
    return "".join([
        chr(randint(ord("a"), ord("z"))) for _ in range(dimension)
    ])
    
def RandomUpperString(dimension):
    if dimension is None:
        raise TypeError
    return "".join([
        chr(randint(ord("A"), ord("Z"))) for _ in range(dimension)
    ])
    
def RandomString(dimension):
    if dimension is None:
        raise TypeError
    return "".join([
        choice([
            chr(randint(ord("a"), ord("z"))), 
            chr(randint(ord("A"), ord("Z")))
        ]) for _ in range(dimension)
    ])

def RandomDateString(starting_date="01.01.1971", ending_date=datetime.now().strftime("%d.%m.%Y")):
    if starting_date is None or ending_date is None:
        raise TypeError
    datetime_format = "%d.%m.%Y"
    start_time = time.mktime(time.strptime(starting_date, datetime_format))
    stop_time = time.mktime(time.strptime(ending_date, datetime_format))
    random_time = start_time + random() * (stop_time - start_time)
    return time.strftime(datetime_format, time.localtime(random_time))

def RandomDateStruct(starting_date="01.01.1971", ending_date=datetime.now().strftime("%d.%m.%Y")):
    if starting_date is None or ending_date is None:
        raise TypeError
    datetime_format = "%d.%m.%Y"
    start_time = time.mktime(time.strptime(starting_date, datetime_format))
    stop_time = time.mktime(time.strptime(ending_date, datetime_format))
    random_time = start_time + random() * (stop_time - start_time)
    return time.strptime(time.strftime(datetime_format, time.localtime(random_time)), datetime_format)