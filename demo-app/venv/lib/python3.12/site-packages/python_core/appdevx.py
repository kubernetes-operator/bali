
from core.aesthetix import *

def IntroductionMessage(message: str):
    if message == "":
        raise ValueError
    
    message = "\n" + message + "\n"
    print_red_bold(message)
    print_yellow_bold("[{}]\n\n".format("=" * 50))