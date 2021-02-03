####  AUTHOR: Daniel Kamenicky ( xkamen21 )  ####
####  PROJECT: IPP 2019/2020                 ####
####  DATE: 14. 4. 2020                      ####
####  SUBJECT: instruction.py                ####

import sys
import operator


class Instruction():
    def __init__(self, order=None, content=None):
        self.order = order #cislo order
        self.content = content #cela instrukce i s parametri
        self.list = [] #list instrukci

    #vraceni listu instrukci
    def list_return(self):
        return self.list

    #serazeni listu podle cisla order
    def list_sort(self):
        self.list.sort(key=operator.attrgetter('order'))

    #pridani listu
    def add_list(self, arg, text):
        self.list.append(Instruction(int(arg), text))
