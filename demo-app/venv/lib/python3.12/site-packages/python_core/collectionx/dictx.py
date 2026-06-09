
"""
    This module contains an upgraded version of the 
        primitive built-in dict from python.
    This module also contains a custom-built error 
        used only for the class Dict.
    
    Current state: in development.
"""
from sys import getsizeof

class EmptyDictError(CustomError):
    pass

class Dict(dict):
    def __init__(self, *arguments, **keywordArguments):
        self.dictionary = {}
        if len(arguments) == 1:
            if type(arguments[0]) != dict:
                raise TypeError
            self.dictionary.update(arguments[0])
            
        elif len(arguments) > 1:
            if not all(type(x) == dict for x in arguments):
                raise TypeError
                
            for argument in arguments:
                self.dictionary.update(argument)
                
        if keywordArguments != {}:
            temporary = {}
            for key, argument in keywordArguments.items():
                temporary.update({key: argument})
            self.dictionary.update(temporary)
            
    def update(self, *arguments, **keywordArguments):
        if not all(type(x) == dict for x in arguments):
            raise TypeError
        
        for argument in arguments:
            self.dictionary.update(argument)
 
        if keywordArguments != {}:
            temporary = {}
            for key, argument in keywordArguments.items():
                temporary.update({key: argument})
            self.dictionary.update(temporary)
    
    def isempty(self):
        return self.dictionary == {}

    def copy(self):
        if self.isempty():
            raise EmptyDictError
        
        return self.dictionary.copy()
        
    def clear(self):
        self.dictionary.clear()