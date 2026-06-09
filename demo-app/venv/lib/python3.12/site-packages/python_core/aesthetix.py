
import json
import requests

def prettify(__collection, __indent=4):
    return json.dumps(__collection, indent=__indent)
    
def pretty_print(__collection, __indent=4):
    print(prettify(__collection, __indent=__indent))

def asciify(text, font=None):
    """ puts 2 lines of spaces
         after the modified text. """
    if type(text) != str:
        try:
            text = str(text)
        except:
            raise TypeError("@text cant be converted to string")
    
    text = "+".join(text.split())
    
    url_parameters = f"/make?text={text}"
    if font:
        url_parameters = f"/make?text={text}&font={font}"
        
    url = "http://artii.herokuapp.com"
    response = requests.get(url + url_parameters)
    if response.status_code != 200:
        raise ConnectionError(
            "status code: {}".format(response.status_code)
        )
    ascii_art = response.text
    items = ascii_art.split("\n")
    
    # deleting last 2 lines from the big text
    items = items[:len(items) - 2]
    # inserting "\n" because in original text it didnt exist
    items[len(items) - 1] += "\n"
    # reconstructing
    ascii_art = "\n".join(items)
    return ascii_art

def shift_left_ascii(ascii_text, size):
    """ left shift the big text with specified
        before:
        BIG_TEXT
        after:
        --------->(size) BIG_TEXT
    """
    if type(size) != int:
        raise TypeError
    
    if type(ascii_text) != str:
        raise TypeError
    
    if not "\n" in ascii_text:
        raise ValueError
    
    lines = ascii_text.split("\n")
    lines = [" " * size + line for line in lines]
    lines = "\n".join(lines)
    return lines
    
def shift_right_ascii(ascii_text, size):
    if type(size) != int:
        raise TypeError
    
    if type(ascii_text) != str:
        raise TypeError

    if not "\n" in ascii_text:
        raise ValueError
    
    lines = ascii_text.split("\n")
    lines = [line[size:] for line in lines]
    lines = "\n".join(lines)
    return lines
    
# colors
purple = "\033[95m"
blue = "\033[94m"
green = "\033[92m"
yellow = "\033[93m"
red = "\033[91m"
white = "\u001b[37;1m"
cyan = "\x1b[38;5;44m"
darkcyan = "\033[36m"
magenta = "033[35m"
black = "\033[30m"
grey = "\x1b[38;5;246m"
orange = "\x1b[38;5;208m"

# font effects
endc = "\033[0m"
# bold = "\033[1m"
# underlined = "\033[4m"

ANSICodesDICT = {
    'purple': '\033[95m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'endc': '\033[0m',
    'bold': '\033[1m',
    'underlined': '\033[4m',
    'white': "\u001b[37;1m",
    "cyan": '\x1b[38;5;44m',
    "darkcyan": '\033[36m',
    "magenta": "\033[35m",
    "black": "\033[30m",
    "grey": "\x1b[38;5;246m",
    "orange": "\x1b[38;5;208m"
}

def ansicode(red, green, blue, string):
    if type(red) != int or \
       type(green) != int or \
       type(blue) != int or \
       type(string) != str:
        raise TypeError
    
    return "\x1b[{};{};{}m{}{}".format(red, green, blue, string, endc)

def underlined(string):
    if type(string) != str:
        try:
            string = str(string)
        except:
            raise TypeError
    return ANSICodesDICT["underlined"] + string + endc

def bold(string):
    if type(string) != str:
        try:
            string = str(string)
        except:
            raise TypeError
    return ANSICodesDICT["bold"] + string + endc

def ConsoleColored(string, color, bold=0, underlined=0):
    if type(string) != str:
        try:
            string = str(string)
        except Exception as error:
            print(error)
            message = red + ANSICodesDICT["bold"] + 'type of param @string should be str.' + endc
            raise TypeError(message)
            del message
    
    # incorrect color
    if color not in ANSICodesDICT and color != 'random':
        message = red + ANSICodesDICT["bold"] + 'this color "{}" is not in ANSICodesDICT.'.format(color) + endc
        raise NotImplementedError(message)
        del message
        
    # bold == 0 and underlined == 0
    if not bold and not underlined:
        if color == "random":
            from random import choice
            return ANSICodesDICT[choice(list(ANSICodesDICT.keys()))] + string + endc
            
        return ANSICodesDICT[color] + string + endc
    
    # bold == 0 and underlined == 1
    elif not bold and underlined:
        if color == "random":
            from random import choice
            return ANSICodesDICT[choice(list(ANSICodesDICT.keys()))] + \
                ANSICodesDICT["underlined"] + string + endc
                
        return ANSICodesDICT[color] + ANSICodesDICT["underlined"] + string + endc
    
    # bold == 1 and underlined == 0
    elif bold and not underlined:
        if color == "random":
            from random import choice
            return ANSICodesDICT[choice(list(ANSICodesDICT.keys()))] + \
                ANSICodesDICT["bold"] + string + endc
                
        return ANSICodesDICT[color] + ANSICodesDICT["bold"] + string + endc
    
    # bold == 1 and underlined == 1
    if color == "random":
        from random import choice
        return ANSICodesDICT[choice(list(ANSICodesDICT.keys()))] + \
            ANSICodesDICT["bold"] + ANSICodesDICT["underlined"] + string + endc
            
    return ANSICodesDICT[color] + ANSICodesDICT["bold"] + ANSICodesDICT["underlined"] + string + endc
    
def PrintANSITable():
    import sys
    print("\n")
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        print (u"\u001b[0m")
    print("\n")
    
left_bracket_cyan = ConsoleColored("[", "cyan", bold=1)
right_bracket_cyan = ConsoleColored("]", "cyan", bold=1)
dash_orange = ConsoleColored("-", "red", bold=1)

left_arrow_yellow = ConsoleColored("<", "blue", bold=1)
left_arrow_yellow = ConsoleColored("<", "yellow", bold=1)

right_arrow_blue = ConsoleColored(">", "blue", bold=1)
right_arrow_yellow = ConsoleColored(">", "yellow", bold=1)

import re
ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

def delete_ansi_escape_codes(string):
    if type(string) != str:
        try:
            string = str(string)
        except:
            raise TypeError
        
    return ansi_escape.sub("", string)
    

# ---------------------------------------------------------
# printing colored 

def print_red(__string):
    print(ConsoleColored(__string, "red"))

def print_blue(__string):
    print(ConsoleColored(__string, "blue"))
    
def print_yellow(__string):
    print(ConsoleColored(__string, "yellow"))
    
def print_orange(__string):
    print(ConsoleColored(__string, "orange"))
    
def print_purple(__string):
    print(ConsoleColored(__string, "purple"))
    
def print_cyan(__string):
    print(ConsoleColored(__string, "cyan"))
    
def print_green(__string):
    print(ConsoleColored(__string, "green"))

# ---------------------------------------------------------
# printing colored UNDERLINED

def print_red_underlined(__string):
    print(ConsoleColored(__string, "red", underlined=1))

def print_blue_underlined(__string):
    print(ConsoleColored(__string, "blue", underlined=1))
    
def print_yellow_underlined(__string):
    print(ConsoleColored(__string, "yellow", underlined=1))
    
def print_orange_underlined(__string):
    print(ConsoleColored(__string, "orange", underlined=1))
    
def print_purple_underlined(__string):
    print(ConsoleColored(__string, "purple", underlined=1))
    
def print_cyan_underlined(__string):
    print(ConsoleColored(__string, "cyan", underlined=1))
    
def print_green_underlined(__string):
    print(ConsoleColored(__string, "green", underlined=1))


# ---------------------------------------------------------
# printing colored BOLD

def print_red_bold(__string):
    print(ConsoleColored(__string, "red", bold=1))

def print_blue_bold(__string):
    print(ConsoleColored(__string, "blue", bold=1))
    
def print_yellow_bold(__string):
    print(ConsoleColored(__string, "yellow", bold=1))
    
def print_orange_bold(__string):
    print(ConsoleColored(__string, "orange", bold=1))
    
def print_purple_bold(__string):
    print(ConsoleColored(__string, "purple", bold=1))
    
def print_cyan_bold(__string):
    print(ConsoleColored(__string, "cyan", bold=1))
    
def print_green_bold(__string):
    print(ConsoleColored(__string, "green", bold=1))

# ---------------------------------------------------------
# printing colored  BOLD + UNDERLINED

def print_red_bold_underlined(__string):
    print(ConsoleColored(__string, "red", bold=1, underlined=1))

def print_blue_bold_underlined(__string):
    print(ConsoleColored(__string, "blue", bold=1, underlined=1))
    
def print_yellow_bold_underlined(__string):
    print(ConsoleColored(__string, "yellow", bold=1, underlined=1))
    
def print_orange_bold_underlined(__string):
    print(ConsoleColored(__string, "orange", bold=1, underlined=1))
    
def print_purple_bold_underlined(__string):
    print(ConsoleColored(__string, "purple", bold=1, underlined=1))
    
def print_cyan_bold_underlined(__string):
    print(ConsoleColored(__string, "cyan", bold=1, underlined=1))
    
def print_green_bold_underlined(__string):
    print(ConsoleColored(__string, "green", bold=1, underlined=1))

# ---------------------------------------------------------
# returning colored 

def yellow(__string):
    return ConsoleColored(__string, "yellow")
    
def orange(__string):
    return ConsoleColored(__string, "orange")
    
def purple(__string):
    return ConsoleColored(__string, "purple")
    
def cyan(__string):
    return ConsoleColored(__string, "cyan")
    
def green(__string):
    return ConsoleColored(__string, "green")
    
def red(__string):
    return ConsoleColored(__string, "red")
    
def blue(__string):
    return ConsoleColored(__string, "blue")
    
# ---------------------------------------------------------
# returning colored UNDERLINED

def yellow_underlined(__string):
    return ConsoleColored(__string, "yellow", underlined=1)
    
def orange_underlined(__string):
    return ConsoleColored(__string, "orange", underlined=1)
    
def purple_underlined(__string):
    return ConsoleColored(__string, "purple", underlined=1)
    
def cyan_underlined(__string):
    return ConsoleColored(__string, "cyan", underlined=1)
    
def green_underlined(__string):
    return ConsoleColored(__string, "green", underlined=1)
    
def red_underlined(__string):
    return ConsoleColored(__string, "red", underlined=1)
    
def blue_underlined(__string):
    return ConsoleColored(__string, "blue", underlined=1)

# ---------------------------------------------------------
# returning colored BOLD

def yellow_bold(__string):
    return ConsoleColored(__string, "yellow", bold=1)
    
def orange_bold(__string):
    return ConsoleColored(__string, "orange", bold=1)
    
def purple_bold(__string):
    return ConsoleColored(__string, "purple", bold=1)
    
def cyan_bold(__string):
    return ConsoleColored(__string, "cyan", bold=1)
    
def green_bold(__string):
    return ConsoleColored(__string, "green", bold=1)
    
def red_bold(__string):
    return ConsoleColored(__string, "red", bold=1)
    
def blue_bold(__string):
    return ConsoleColored(__string, "blue", bold=1)

# ---------------------------------------------------------
# returning colored BOLD + UNDERLINED

def yellow_bold_underlined(__string):
    return ConsoleColored(__string, "yellow", bold=1, underlined=1)
    
def orange_bold_underlined(__string):
    return ConsoleColored(__string, "orange", bold=1, underlined=1)
    
def purple_bold_underlined(__string):
    return ConsoleColored(__string, "purple", bold=1, underlined=1)
    
def cyan_bold_underlined(__string):
    return ConsoleColored(__string, "cyan", bold=1, underlined=1)
    
def green_bold_underlined(__string):
    return ConsoleColored(__string, "green", bold=1, underlined=1)
    
def red_bold_underlined(__string):
    return ConsoleColored(__string, "red", bold=1, underlined=1)
    
def blue_bold_underlined(__string):
    return ConsoleColored(__string, "blue", bold=1, underlined=1)
    
    
if __name__ == '__main__':
    print(asciify("hello"))