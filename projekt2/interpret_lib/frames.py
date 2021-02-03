####  AUTHOR: Daniel Kamenicky ( xkamen21 )  ####
####  PROJECT: IPP 2019/2020                 ####
####  DATE: 14. 4. 2020                      ####
####  SUBJECT: frames.py                     ####

import re
import sys

from interpret_lib.error import Error

class Frames(Error):
    def __init__(self):
        self.frame_stack = [] #stack lokalnich ramcu
        self.Global = {} #globalni ramec
        self.Temporary = {} #docasny ramec
        self.Temporary_def = False #promenna rikajici zda je docasny ramec definovan

    #vytvoreni docasneho ramce
    def create_temporary_frame(self):
        self.Temporary = {}
        self.Temporary_def = True

    #vlozeni docasneho ramce do stacku ramcu, TF na LF
    def push_temporary_to_stack(self):
        if self.Temporary_def == True:
            self.frame_stack.append(self.Temporary)
            #zruseni docasneho ramce
            self.Temporary_def = False
        else:
            self.Print_Error(55, "ERROR: nejde pushnout nedefinovany docasny ramec")

    #popnuti lokalniho ramce do docasneho ramce
    def pop_lf_to_tf_from_stack(self):
        #testovani neni-li stack prazdny
        if not self.frame_stack:
            self.Print_Error(55, "ERROR: ve stacku neni zadny ramec")
        else:
            self.Temporary = self.frame_stack.pop()
            self.Temporary_def = True;

    #pomocna funkce pro vraceni typu ramce (LF, GF, TF)
    def return_frame(self, frame):
        name = frame[:2]
        if name == 'GF':
            #vraceni globalniho ramce
            return self.Global
        elif name == 'TF':
            if self.Temporary_def == False:
                self.Print_Error(55, "ERROR: pokus o definici na nenedefinovanem ramci")
            else:
                #vraceni docasneho ramce
                return self.Temporary
        else:
            #kontrola zda-li stack ramcu neni prazdny
            if not self.frame_stack:
                self.Print_Error(55, "ERROR: ve stacku neni zadny ramec")
            else:
                #vraceni lokalniho ramce
                return self.frame_stack[len(self.frame_stack) - 1]

    #vraceni typu promenne ulozene v ramci
    def get_type(self, var):
        #jmeno promenne
        name = var[3:]
        #zjisteni v jakem ramci se nachazi
        frame = self.return_frame(var)
        #kontrola zda-li se skutecne nachazi v danem ramci
        if name not in frame:
            self.Print_Error(54, "ERROR: ziskani hodnoty z nezname promenne")
        else:
            #vraceni typu promenne
            return frame[var[3:]]['type']

    #vraceni hodnoty promenne ulozene v ramci
    def get_value(self, var):
        #jmeno promenne
        name = var[3:]
        #zjisteni v jakem ramci se nachazi
        frame = self.return_frame(var)
        #kontrola zda-li se skutecne nachazi v danem ramci
        if name not in frame:
            self.Print_Error(54, "ERROR: ziskani hodnoty z nezname promenne")
        else:
            #vraceni hodnoty promenne
            return frame[var[3:]]['value']

    #vlozeni hodnoty do promenne
    def insert_into_var(self, var, value, type):
        #jmeno promenne
        name = var[3:]
        #zjisteni v jakem ramci se nachazi
        frame = self.return_frame(var)
        #kontrola zda-li se skutecne nachazi v danem ramci
        if name not in frame:
            self.Print_Error(54, "ERROR: vlozeni hodnoty do nenadefinovane promenne")
        else:
            #jedna se o string prevedeme z unicode na string
            if type == 'string':
                for x in range(0, 1000):
                    if x<10:
                        compare = "\\" + "00" + str(x)
                        value = value.replace(compare, chr(x))
                    elif x>9 and x<100:
                        compare = "\\" + "0" + str(x)
                        value = value.replace(compare, chr(x))
                    else:
                        compare = "\\" + str(x)
                        value = value.replace(compare, chr(x))
                #vlozeni dat do ramce
                frame[name] = {'type': type, 'value': value}
            else:
                frame[name] = {'type': type, 'value': value}


    #zmena jednoho charkteru na urcite pozici
    def setchar_on_position(self, var, char, position):
        #jmeno promenne
        name = var[3:]
        #zjisteni v jakem ramci se nachazi
        frame = self.return_frame(var)
        #kontrola zda-li se skutecne nachazi v danem ramci
        if name not in frame:
            self.Print_Error(54, "ERROR: vlozeni hodnoty do nenadefinovane promenne")
        else:
            #jedna-li se o promennou ktera neni inicializovana, chyba
            if frame[name]['value'] == None:
                self.Print_Error(56, "ERROR: neinicializovana promenna")
            #kontrola zda pozice neni mimo rozsah stringu
            elif len(frame[name]['value']) <= position or position < 0:
                self.Print_Error(58, "ERROR: outrange SETCHAR")
            else:
                #vlozeni dat do stringu
                frame[name]['value'] = list(frame[name]['value'])
                frame[name]['value'][position] = char
                frame[name]['value'] = "".join(frame[name]['value'])

    #vlozeni nove promenne do stacku
    def insert_var(self, var):
        #jmeno promenne
        name = var[3:]
        #zjisteni v jakem ramci se nachazi
        frame = self.return_frame(var)
        #kontrola vyskytu promenne v ramci
        if name in frame:
            self.Print_Error(52, "ERROR: redefinice promenne")
        else:
            #vlozeni promenne do stacku
            frame[name] = {'type': None, 'value': None}

    #vraceni obsahu ramcu
    def print_frame_content(self, frame):
        if frame == 'GF':
            #kontrola zda ramec neni prazdny
            if self.Global:
                #pro kazdy prvek v ramci
                for key in self.Global:
                    #vypis na standardni chybovy vystup
                    print(key, "->", self.Global[key]['type'], self.Global[key]['value'], "\n", file = sys.stderr, end='')
            else:
                print("EMPTY\n", file = sys.stderr, end='')
        elif frame == 'TF':
            if self.Temporary_def == False:
                print("UNDEF\n", file = sys.stderr, end='')
            else:
                #kontrola zda ramec neni prazdny
                if self.Temporary:
                    #pro kazdy prvek v ramci
                    for key in self.Temporary:
                        #vypis na standardni chybovy vystup
                        print(key, "->", self.Temporary[key]['type'], self.Temporary[key]['value'], "\n", file = sys.stderr, end='')
                else:
                    print("EMPTY\n", file = sys.stderr, end='')
        else:
            #kontrola zda stack neni prazdny
            if not self.frame_stack:
                print("UNDEF\n", file = sys.stderr, end='')
            else:
                #kontrola zda ramec neni prazdny
                if self.frame_stack[len(self.frame_stack) - 1]:
                    #pro kazdy prvek v ramci
                    for key in self.frame_stack[len(self.frame_stack) - 1]:
                        #vypis na standardni chybovy vystup
                        print(key, "->", self.frame_stack[len(self.frame_stack) - 1][key]['type'], self.frame_stack[len(self.frame_stack) - 1][key]['value'], "\n", file = sys.stderr, end='')
                else:
                    print("EMPTY\n", file = sys.stderr, end='')
