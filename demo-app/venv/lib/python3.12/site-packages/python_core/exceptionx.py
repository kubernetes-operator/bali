
from core.system import *
from core.aesthetix import ConsoleColored

class CustomException(Exception):
    def __init__(self, message=None):
        if type(message) != str:
            raise TypeError
        self.message = message
    
    def __str__(self):
        if self.message:
            return ConsoleColored(self.message, "yellow", bold=1)
        else:
            return "<no message available>"
        
class RuntimeError(CustomException):
    """ error during execution """
    pass

class HTTP_RequestError(CustomException):
    """ handles the http stuff"""
    pass

class NotFound_404_Error(HTTP_RequestError):
    """ 404 http error """
    pass

class Forbidden_403_Error(HTTP_RequestError):
    """ 403 http error """
    pass

class PathLibraryError(CustomException):
    pass

class PathSeparatorsDiffersError(PathLibraryError):
    """ when there are 2 different paths and their folder separator differs """
    pass

class NotAFileError(PathLibraryError):
    """ is not a folder """
    pass

class FileError(CustomException):
    """ deals with files """
    pass

class NotAnImageError(FileError):
    """ file is not an image """
    pass
    
class StupidCodeError(CustomException):
    pass


if __name__ == '__main__':
    # raise RuntimeError("some random message")
    try:
        raise RuntimeError("some random message")
    except CustomException as error:
        print(error)
    