####  AUTHOR: Daniel Kamenicky ( xkamen21 )  ####
####  PROJECT: IPP 2019/2020                 ####
####  DATE: 14. 4. 2020                      ####
####  SUBJECT: interpret.py                  ####

import sys
import re

from interpret_lib.error import Error
from interpret_lib.xml_parser import XmlParser
from interpret_lib.arguments import Arguments
from interpret_lib.instruction import Instruction
from interpret_lib.list_of_instructions import List_Instructions
from interpret_lib.frames import Frames
from interpret_lib.stack import Stack


def Main():
    Err = Error() #instance na chybove stavy
    Arg = Arguments() #instance na kontrolu argumentu
    Arg.Arguments_check() #kontorla argumentu

    Inst = Instruction() #instance pro instrukci

    List_Inst = List_Instructions() #instance pro lsit instrukci

    Xml_Parser = XmlParser(Arg.Get_Source_File(), Inst, List_Inst) #instance kontroli XML
    Xml_Parser.Check_XML_File() #kontrola XML
    Xml_Parser.Check_Syntax() #kontrola syntaxe a lexemu

    frame = Frames() #instance zastupujici ramce
    stack = Stack() #instance zastupujici datovy ramec

    #metoda pro prevedeni unixcode na string
    def get_string(first):
        for x in range(0, 1000):
            if x<10:
                compare = "\\" + "00" + str(x)
                first = first.replace(compare, chr(x))
            elif x>9 and x<100:
                compare = "\\" + "0" + str(x)
                first = first.replace(compare, chr(x))
            else:
                compare = "\\" + str(x)
                first = first.replace(compare, chr(x))
        return first;

    #metoda zjisteni typu a hodnoty symbolu
    def type_and_value(type, value):
        if type == 'var':
            return_type = frame.get_type(value)
            return_value = frame.get_value(value)
        else:
            return_type = type
            return_value = value
        if return_type == 'string':
            return_value = get_string(return_value)
        return (return_type, return_value)


    #pocitadlo provedenych radku ve vstupnim souboru
    line_done_counter = 0
    #flag na standradni vtup
    Stdin_Flag = 0
    #pomocnna na pocet radku v vstupnim souboru
    line_count = 0
    #kontrola vstupniho souboru
    if Arg.Get_Input_File() == None:
        Stdin_Flag = 1
    else:
        try:
            Input_File = open(Arg.Get_Input_File(), 'r')
        except FileNotFoundError:
            Err.Print_Error(11, "ERROR: spatny vstupni soubor")

    #zjisteni poctu radku souboru
    if Stdin_Flag ==0:
        with Input_File as f:
            for line in f:
                line_count += 1
        Input_File.close()
        Input_File = open(Arg.Get_Input_File(), 'r')

    #iterator pro iterovani v Main_List
    iterator = 1
    #counter na pocet provedenych instrukci
    instruction_done = 0

    #nekonecy cyklus
    while True:
        #kontrola prazdnosti listu
        if not List_Inst.Main_List:
            exit(0)
        #kontrola neni-li iterator vetsi jak pocet instrukci v listu
        if iterator > List_Inst.number_of_inst:
            exit(0)

        #ziskani instrukce z Main_List
        instruction = List_Inst.Main_List[iterator].split(" ")

        #instrukce PUSHS
        if instruction[0] == 'PUSHS':
            stack.Push(instruction[2], instruction[1])

        #instrukce POPS
        elif instruction[0] == 'POPS':
            value, type = stack.Pop()
            frame.insert_into_var(instruction[2], value, type)

        #instrukce CREATEFRAME
        elif instruction[0] == 'CREATEFRAME':
            frame.create_temporary_frame()

        #instrukce PUSHSFRAME
        elif instruction[0] == 'PUSHFRAME':
            frame.push_temporary_to_stack()

        #instrukce POPFRANE
        elif instruction[0] == 'POPFRAME':
            frame.pop_lf_to_tf_from_stack()

        #instrukce DEFVAR
        elif instruction[0] == 'DEFVAR':
            frame.insert_var(instruction[2])

        #instrukce CALL
        elif instruction[0] == 'CALL':
            iterator = List_Inst.insert_into_call_stack(instruction[2], iterator)

        #instrukce RETURN
        elif instruction[0] == 'RETURN':
            iterator = List_Inst.get_from_call_stack()

        #instrukce LABEL
        elif instruction[0] == 'LABEL':
            pass

        #instrukce ADD, SUB, MUL, IDIV
        elif instruction[0] in ['ADD', 'SUB', 'MUL', 'IDIV']:
            #kontrola typu parametru instrukce
            if instruction[3] == 'int':
                first = instruction[4]
            elif instruction[3] == 'var':
                if frame.get_type(instruction[4]) != 'int':
                    if frame.get_type(instruction[4]) == None:
                        Err.Print_Error(56, "ERROR: nemuzeme scitat hodnotu neinicializovane promenne")
                    else:
                        Err.Print_Error(53, "ERROR: pri ADD musi byt datovy typ int")
                else:
                    first = frame.get_value(instruction[4])
            else:
                Err.Print_Error(53, "ERROR: pri ADD musi byt datovy typ int")

            #kontrola typu parametru instrukce
            if instruction[5] == 'int':
                second = instruction[6]
            elif instruction[5] == 'var':
                if frame.get_type(instruction[6]) != 'int':
                    if frame.get_type(instruction[6]) == None:
                        Err.Print_Error(56, "ERROR: nemuzeme scitat hodnotu neinicializovane promenne")
                    else:
                        Err.Print_Error(53, "ERROR: pri ADD musi byt datovy typ int")
                else:
                    second = frame.get_value(instruction[6])
            else:
                Err.Print_Error(53, "ERROR: pri ADD musi byt datovy typ int")

            #instrukce ADD
            if instruction[0] == 'ADD':
                result = int(first) + int(second)
                frame.insert_into_var(instruction[2], result, "int")
            #instrukce SUB
            elif instruction[0] == 'SUB':
                result = int(first) - int(second)
                frame.insert_into_var(instruction[2], result, "int")
            #instrukce MUL
            elif instruction[0] == 'MUL':
                result = int(first) * int(second)
                frame.insert_into_var(instruction[2], result, "int")
            #instrukce IDIV
            else:
                if int(second) == 0:
                    Err.Print_Error(57, "ERROR: deleni nulou")
                else:
                    result = int(first) // int(second)
                    frame.insert_into_var(instruction[2], result, "int")

        #instrukce LT, GT, EQ
        elif instruction[0] in ['LT', 'GT', 'EQ']:
            #zjisteni typu a obsahu parametru
            type1, first = type_and_value(instruction[3], instruction[4])
            type2, second = type_and_value(instruction[5], instruction[6])
            #kontrola parametru
            if first == None or second == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            #instrukce EQ
            if instruction[0] == 'EQ':
                if type1 == 'nil':
                    if type2 == 'nil':
                        result = 'true';
                    else:
                        result = 'false';
                elif type2 == 'nil':
                    result = 'false';
                else:
                    if type1 != type2:
                        Err.Print_Error(53, "ERROR: nelze porovnavat dve promenne ruzneho typu")
                    else:
                        if first != second:
                            result = 'false'
                        else:
                            result = 'true'
            else:
                #kontrola datovych typu
                if type1 != type2:
                    Err.Print_Error(53, "ERROR: typy promennych se museji rovnat")
                if type1 == 'int':
                    first = int(first)
                    second = int(second)
                #instrukce LT
                if instruction[0] == 'LT':
                    if type1 == 'nil' or type2 == 'nil':
                        Err.Print_Error(53, "ERROR: LT nepodporuje datovy typ nil")
                    else:
                        if first < second:
                            result = 'true'
                        else:
                            result = 'false'
                #instrukce GT
                else:
                    if type1 == 'nil' or type2 == 'nil':
                        Err.Print_Error(53, "ERROR: GT nepodporuje datovy typ nil")
                    else:
                        if first > second:
                            result = 'true'
                        else:
                            result = 'false'
            #vlozeni do promenne
            frame.insert_into_var(instruction[2], result, "bool")

        #instrukce AND, OR
        elif instruction[0] in ['AND', 'OR']:
            #zjisteni typu a obsahu parametru
            type1, first = type_and_value(instruction[3], instruction[4])
            type2, second = type_and_value(instruction[5], instruction[6])
            #kontrola parametru
            if first == None or second == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type1 != 'bool' or type2 != 'bool':
                Err.Print_Error(53, "ERROR: logicke operace podporuji pouze datovy typ bool")
            else:
                #instrukce AND
                if instruction[0] == 'AND':
                    if first == 'true' and second == 'true':
                        result = 'true'
                    else:
                        result = 'false'
                #instrukce OR
                else:
                    if first == 'false' and second == 'false':
                        result = 'false'
                    else:
                        result = 'true'
            #vlozeni do promenne
            frame.insert_into_var(instruction[2], result, "bool")

        #instrukce NOT
        elif instruction[0] == 'NOT':
            #zjisteni typu a obsahu parametru
            type, first = type_and_value(instruction[3], instruction[4])
            #kontrola parametru
            if first == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type != 'bool':
                Err.Print_Error(53, "ERROR: logicke operace podporuji pouze datovy typ bool")
            else:
                if first == 'false':
                    result = 'true'
                else:
                    result = 'false'
            #vlozeni do promenne
            frame.insert_into_var(instruction[2], result, "bool")

        #instrukce INT2CHAR
        elif instruction[0] == 'INT2CHAR':
            #zjisteni typu a obsahu parametru
            type, first = type_and_value(instruction[3], instruction[4])
            #kontrola parametru
            if first == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type != 'int':
                Err.Print_Error(53, "ERROR: spatny datovy typ")
            elif int(first) < 0 or int(first) > 1114111:
                Err.Print_Error(58, "ERROR: cilso mimo rozsah Unicode")
            else:
                result = chr(int(first))
                #vlozeni do promenne
                frame.insert_into_var(instruction[2], result, "string")

        #instrukce STRI2INT
        elif instruction[0] == 'STRI2INT':
            #zjisteni typu a obsahu parametru
            type1, first = type_and_value(instruction[3], instruction[4])
            type2, second = type_and_value(instruction[5], instruction[6])
            #kontrola parametru
            if first == None or second == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type1 != 'string' or type2 != 'int':
                Err.Print_Error(53, "ERROR: spatny datovy typ")
            elif len(first) <= int(second):
                Err.Print_Error(58, "ERROR: outrange STRI2INT")
            else:
                result = ord(first[int(second)])
                #vlozeni do promenne
                frame.insert_into_var(instruction[2], result, "int")

        #instrukce CONCAT
        elif instruction[0] == 'CONCAT':
            #zjisteni typu a obsahu parametru
            type1, first = type_and_value(instruction[3], instruction[4])
            type2, second = type_and_value(instruction[5], instruction[6])
            #kontrola parametru
            if first == None or second == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type1 != 'string' or type2 != 'string':
                Err.Print_Error(53, "ERROR: spatny datovy typ")
            else:
                result = first + second
                #vlozeni do promenne
                frame.insert_into_var(instruction[2], result, "string")

        #instrukce STRLEN
        elif instruction[0] == 'STRLEN':
            type, first = type_and_value(instruction[3], instruction[4])
            #kontrola parametru
            if first == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type != 'string':
                Err.Print_Error(53, "ERROR: spatny datovy typ")
            else:
                result = len(first)
                #vlozeni do promenne
                frame.insert_into_var(instruction[2], result, "int")

        #instrukce GETCHAR
        elif instruction[0] == 'GETCHAR':
            #zjisteni typu a obsahu parametru
            type1, first = type_and_value(instruction[3], instruction[4])
            type2, second = type_and_value(instruction[5], instruction[6])
            #kontrola parametru
            if first == None or second == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type1 != 'string' or type2 != 'int':
                Err.Print_Error(53, "ERROR: spatny datovy typ")
            else:
                if len(first) <= int(second):
                    Err.Print_Error(58, "ERROR: outrange GETCHAR")
                else:
                    result = first[int(second)]
                    #vlozeni do promenne
                    frame.insert_into_var(instruction[2], result, "string")

        #instrukce SETCHAR
        elif instruction[0] == 'SETCHAR':
            #zjisteni typu a obsahu parametru
            type1, first = type_and_value(instruction[3], instruction[4])
            type2, second = type_and_value(instruction[5], instruction[6])
            #kontrola parametru
            if first == None or second == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type1 != 'int' or type2 != 'string':
                Err.Print_Error(53, "ERROR: spatny datovy typ")
            else:
                if len(second) == 0:
                    Err.Print_Error(58, "ERROR: prazdny retezec SETCHAR")
                else:
                    #vlozeni do promenne
                    frame.setchar_on_position(instruction[2], second[0], int(first))

        #instrukce TYPE
        elif instruction[0] == 'TYPE':
            #zjisteni typu a obsahu parametru
            type, first = type_and_value(instruction[3], instruction[4])
            #kontrola parametru
            if first == None:
                #vlozeni do promenne
                frame.insert_into_var(instruction[2], "", "string")
            else:
                #vlozeni do promenne
                frame.insert_into_var(instruction[2], type, "string")

        #instrukce MOVE
        elif instruction[0] == 'MOVE':
            #zjisteni typu a obsahu parametru
            type, first = type_and_value(instruction[3], instruction[4])
            #kontrola parametru
            if first == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            #vlozeni do promenne
            frame.insert_into_var(instruction[2], first, type)

        #instrukce JUMP
        elif instruction[0] == 'JUMP':
            iterator = List_Inst.Do_Jump(instruction[2])

        #instrukce JUMPIFEQ
        elif instruction[0] == 'JUMPIFEQ':
            #zjisteni typu a obsahu parametru
            type1, first = type_and_value(instruction[3], instruction[4])
            type2, second = type_and_value(instruction[5], instruction[6])
            #kontrola parametru
            if first == None or second == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type1 == 'nil':
                if type2 == 'nil':
                    iterator = List_Inst.Do_Jump(instruction[2])
                else:
                    pass
            else:
                if type2 == 'nil':
                    pass
                elif type1 == type2:
                    if str(first) == str(second):
                        iterator = List_Inst.Do_Jump(instruction[2])
                    else:
                        pass
                else:
                    Err.Print_Error(53, "ERROR: typy promennych se museji rovnat")

        #instrukce JUMPIFNEQ
        elif instruction[0] == 'JUMPIFNEQ':
            #zjisteni typu a obsahu parametru
            type1, first = type_and_value(instruction[3], instruction[4])
            type2, second = type_and_value(instruction[5], instruction[6])
            #kontrola parametru
            if first == None or second == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type1 == 'nil':
                if type2 == 'nil':
                    pass
                else:
                    iterator = List_Inst.Do_Jump(instruction[2])
            else:
                if type2 == 'nil':
                    iterator = List_Inst.Do_Jump(instruction[2])
                elif type1 == type2:
                    if str(first) != str(second):
                        iterator = List_Inst.Do_Jump(instruction[2])
                    else:
                        pass
                else:
                    Err.Print_Error(53, "ERROR: typy promennych se museji rovnat")

        #instrukce EXIT
        elif instruction[0] == 'EXIT':
            #zjisteni typu a obsahu parametru
            type, first = type_and_value(instruction[1], instruction[2])
            #kontrola parametru
            if first == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type != 'int':
                Err.Print_Error(53, "ERROR: spatny datovy typ")
            else:
                if int(first) < 0 or int(first) > 49:
                    Err.Print_Error(57, "ERROR: navratova hodnota mimo rozsah")
                else:
                    exit(int(first))

        #instrukce WRITE
        elif instruction[0] == 'WRITE':
            #zjisteni typu a obsahu parametru
            type, first = type_and_value(instruction[1], instruction[2])
            #kontrola parametru
            if first == None:
                Err.Print_Error(56, "ERROR: neinicializovana promenna")
            if type == 'string':
                print(first, end='')
            elif type == 'nil':
                print("", end='')
            else:
                print(first, end='')

        #instrukce READ
        elif instruction[0] == 'READ':
            if Stdin_Flag == 1:
                result = input()
            else:
                line_done_counter += 1
                result = Input_File.readline()
                result = result.rstrip("\n")
            if result == None:
                #vlozeni do promenne
                frame.insert_into_var(instruction[2], "nil", "nil")
            elif line_count < line_done_counter:
                #vlozeni do promenne
                frame.insert_into_var(instruction[2], "nil", "nil")
            elif instruction[4] == 'string':
                #vlozeni do promenne
                frame.insert_into_var(instruction[2], result, "string")
            elif instruction[4] == 'int':
                if not re.search('^[+-]?[0-9]+$', result):
                    #vlozeni do promenne
                    frame.insert_into_var(instruction[2], "nil", "nil")
                else:
                    #vlozeni do promenne
                    frame.insert_into_var(instruction[2], result, "int")
            else:
                if not re.search('^[T|t][R|r][u|U][e|E]$', result):
                    #vlozeni do promenne
                    frame.insert_into_var(instruction[2], "false", "bool")
                else:
                    #vlozeni do promenne
                    frame.insert_into_var(instruction[2], "true", "bool")


        #instrukce BREAK
        elif instruction[0] == 'BREAK':
            print("\n\t\t\tSyntax: %Typ_Ramce%: %jmeno_promenne% -> %datovy_typ% %nazev%\n\t\t\tSyntax: Pozice kodu: %pocet_radku%\n", file = sys.stderr, end='')
            print("                        ________________________________________________________________\n", file = sys.stderr, end='')
            print(" _        __            |", file = sys.stderr, end='')
            print("Globalni Ramec(GF): ", file = sys.stderr, end='')
            frame.print_frame_content("GF")
            print("(_)_ __  / _| ___    _  |", file = sys.stderr, end='')
            print("Lokalni Ramec(LF): ", file = sys.stderr, end='')
            frame.print_frame_content("LF")
            print("| | '_ \| |_ / _ \  (_) |", file = sys.stderr, end='')
            print("Docasny Ramec(TF): ", file = sys.stderr, end='')
            frame.print_frame_content("TF")
            print("| | | | |  _| (_) |  _  |", file = sys.stderr, end='')
            print("Pocet vykonanych instrukci: ", file = sys.stderr, end='')
            print(instruction_done, "\n" , file = sys.stderr, end='')
            print("|_|_| |_|_|  \___/  (_) |", file = sys.stderr, end='')
            print("Pozice v kodu: ", file = sys.stderr, end='')
            print(iterator, "\n" , file = sys.stderr, end='')
            print("\t\t\t‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n", file = sys.stderr, end='')

        #instrukce DPRINT
        elif instruction[0] == 'DPRINT':
            type, first = type_and_value(instruction[1], instruction[2])
            if first != None:
                print(first, file = sys.stderr)
            else:
                Err.Print_Error(56, "ERROR: chyba vypisu neinicializovane promenne")

        #inkrementace iteratoru a poctu provedenych instrukci
        iterator += 1
        instruction_done += 1

    #zavreni vstupniho souboru
    if Stdin_Flag == 0:
        Input_File.close()

Main()
