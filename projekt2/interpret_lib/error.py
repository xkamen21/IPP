####  AUTHOR: Daniel Kamenicky ( xkamen21 )  ####
####  PROJECT: IPP 2019/2020                 ####
####  DATE: 14. 4. 2020                      ####
####  SUBJECT: error.py                      ####

import sys

class Error:

    def __init__(slef):
        pass

    #vypis chybove halsky a ukonceni programu pod navratovym kodem
    def Print_Error(self, number, message):
        print(message, file = sys.stderr)
        exit(number)
