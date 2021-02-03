####  AUTHOR: Daniel Kamenicky ( xkamen21 )  ####
####  PROJECT: IPP 2019/2020                 ####
####  DATE: 14. 4. 2020                      ####
####  SUBJECT: arg_instruction.py            ####

import sys
import operator

class Arg_Instruction():
    def __init__(self, id=None, type=None, content=None):
        self.list = [] #list argumentu
        self.id = id #poradi argumentu (arg1, arg2 ...)
        self.type = type #typ argumentu
        self.content = content #obsah typu

    #vraceni listu argumentu
    def list_return(self):
        return self.list

    #pridani do listu
    def add_list(self, arg, type, text):
        #jedna-li se o string a string je prazdny
        if type == 'string' and text == None:
            text = ""
        self.list.append(Arg_Instruction(arg, type, text))

    #serazeni listu podle cisla argumentu
    def list_sort(self):
        self.list.sort(key=operator.attrgetter('id'))

    #vraceni argumentu jako string pro ulozeni jako 'content' v modulu instruction
    def return_string(self):
        string = ""
        i=0
        for obj in self.list:
            if i==1:
                string += " "
            string = string + obj.type + " " + obj.content
            i = 1

        return string

    #vycisteni listu
    def clear_list(self):
        self.list.clear()
