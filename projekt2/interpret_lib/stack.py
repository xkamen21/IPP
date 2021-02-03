####  AUTHOR: Daniel Kamenicky ( xkamen21 )  ####
####  PROJECT: IPP 2019/2020                 ####
####  DATE: 14. 4. 2020                      ####
####  SUBJECT: stack.py                      ####

import re

from interpret_lib.error import Error

class Stack(Error):
    def __init__(self):
        self.Data_Stack = []

    #metoda vkladajici data na datovy zasobnik
    def Push(self, value, type):
        self.Data_Stack.append((value, type))

    #metoda popujici data z datoveho zasobniku
    def Pop(self):
        #kontrola prazdnosti zasobniku
        if len(self.Data_Stack) > 0:
            return self.Data_Stack.pop()
        else:
            self.Print_Error(56, "ERROR: datovy zasobnik je prazdny")
