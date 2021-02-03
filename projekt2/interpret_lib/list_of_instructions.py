####  AUTHOR: Daniel Kamenicky ( xkamen21 )  ####
####  PROJECT: IPP 2019/2020                 ####
####  DATE: 14. 4. 2020                      ####
####  SUBJECT: list_of_instructions.py       ####

import re

from interpret_lib.error import Error

class List_Instructions(Error):
    def __init__(self):
        self.Main_List = {} #hlavni telo kodu
        self.list_of_labels = {} #uchovam si label pro pripad skoku v kodu
        self.number_of_inst = 0 #cisla instrukci, dalo by se chapat jako cisla radku
        self.call_stack = [] #zasobnik volani

    #vlozeni instrukce do Main_List, pokud se jedna o label, vlozu i do list_of_labels
    def insert_instruction(self, inst):
        #inkrementace pocitadla instrukci
        self.number_of_inst += 1
        #vlozeni instrukce do listu
        self.Main_List[self.number_of_inst] = inst
        #kontrola labelu
        if re.search('^LABEL.*', inst):
            name_of_label = inst[12:]
            if name_of_label in self.list_of_labels:
                self.Print_Error(52, "ERROR: Duplicitni nazev Labelu")
            #vlozeni labelu do listu
            self.list_of_labels[name_of_label] = self.number_of_inst

    #pracce s call stackem
    def insert_into_call_stack(self, label, position):
        #neni label v stacku, chyba
        if label not in self.list_of_labels:
            self.Print_Error(52, "ERROR: skok na nezname navesti")
        else:
            #vlozeni pozice volani do stacku
            self.call_stack.append(position)
            #vraceni pozice labelu
            return self.list_of_labels[label]

    #vraceni hodnoty ze stacku
    def get_from_call_stack(self):
        if not self.call_stack:
            self.Print_Error(56, "ERROR: zasobnik volani je prazdny")
        else:
            #vraceni posledni pushnute pozice ze stacku
            return self.call_stack.pop()

    #provedeni skoku
    def Do_Jump(self, label):
        if label not in self.list_of_labels:
            self.Print_Error(52, "ERROR: skok na nezname navesti")
        else:
            #vraceni pozice labelu
            return self.list_of_labels[label]
