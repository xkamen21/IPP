####  AUTHOR: Daniel Kamenicky ( xkamen21 )  ####
####  PROJECT: IPP 2019/2020                 ####
####  DATE: 14. 4. 2020                      ####
####  SUBJECT: arguments.py                  ####

import sys
import re

from interpret_lib.error import Error

class Arguments(Error):

    def __init__(self):
        self.source_file = '' #zdrojovy soubor
        self.input_file = ''  #vstupni soubor
        pass

    #kontrola argumentu skriptu
    def Arguments_check(self):
        #skript nema zadne argumenty chyba (nemuze nikdy nastat, samotny skript je zapocitan take)
        if len(sys.argv) == 0:
            self.Print_Error(31, "ERROR")

        if len(sys.argv)>1:
            #preskoceni jmena skriptu
            skip_first = 1
            for argument in sys.argv:
                #preskoceni na argumenty
                if skip_first == 1:
                    skip_first = 0
                    continue

                #kontrola argumentu --help
                if str(argument) == '--help':
                    #kontrola zda argument --help je jedinym argumentem
                    if len(sys.argv)!=2:
                        self.Print_Error(10, "ERROR: argument --help nemuze byt kombinovan s ostatnimi")
                    else:
                        #vypis pomocne zpravy
                        print(" _   _      _            _____________________________________________________________________\n", end='')
                        print("| | | | ___| |_ __    _  | interpret.py - program nacte XML reprezentaci z daneho souboru,\n", end='')
                        print("| |_| |/ _ \ | '_ \  (_) |                nebo ze standardniho vstupu a dany kod interpretuje\n", end='')
                        print("|  _  |  __/ | |_) |  _  | Parametry - --source=file vstupni soubor s XML reprezentaci kodu\n", end='')
                        print("|_| |_|\___|_| .__/  (_) |           - --input=file soubor se vstupy pro samotnou interpretaci\n", end='')
                        print("             |_|         |           - bez parametru je bran standardni vstup (stdin)\n", end='')
                        print("                         ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n", end='')
                        exit(0)
                #zjisteni argumentu --source=
                elif re.search(r'^--source=', str(argument)):
                    self.source_file = str(argument[9:])
                #zjisteni argumentu --input=
                elif re.search(r'^--input=', str(argument)):
                    self.input_file = str(argument[8:])
                else:
                    self.Print_Error(10, "ERROR: parametr neni podporovan")
                pass

        #neni-li zdrojovy souboru, je pouzit standardni vstup
        if self.source_file == '':
            self.source_file = sys.stdin

        #neni-li vstupni souboru, hodnota je nastavena na None
        if self.input_file == '':
            self.input_file = None

    #vraceni zdrojoveho souboru
    def Get_Source_File(self):
        return self.source_file

    #vraceni vstupniho souboru
    def Get_Input_File(self):
        return self.input_file
