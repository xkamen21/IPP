####  AUTHOR: Daniel Kamenicky ( xkamen21 )  ####
####  PROJECT: IPP 2019/2020                 ####
####  DATE: 14. 4. 2020                      ####
####  SUBJECT: xml_parser.py                 ####

import sys
import re
import xml.etree.ElementTree as ET

from interpret_lib.error import Error
from interpret_lib.arg_instruction import Arg_Instruction

class XmlParser(Error):

    def __init__(self, input_file, Inst, Inst_List):
        self.input_file = input_file #input file
        self.Inst = Inst
        self.Inst_List = Inst_List #list of instructions
        pass

    def Check_XML_File(self):
        try:
            tree = ET.parse(self.input_file)
            self.root = tree.getroot()
        #chybny XML format souboru
        except ET.ParseError:
            self.Print_Error(31, "ERROR: Chybny XML format")
        #spatny vstupni soubor
        except FileNotFoundError:
            self.Print_Error(11, "ERROR: spatny vstupni soubor")
        #kontrola korenoveho elementu program
        if self.root.tag != 'program':
                self.Print_Error(32, "ERROR: korenovy element musi byt 'program'")
        #kontrola zda program neobsahuje nepovoleny atribut
        for attribute in self.root.attrib:
            if attribute not in ['language', 'name', 'description']:
                self.Print_Error(32, "ERROR: nepovoleny atribut korenoveho elementu")
        #kontrola parametru language
        if 'language' not in self.root.attrib:
            self.Print_Error(32, "ERROR: v korenovem elementu chybi atribut 'language'")
        #kontrola IPPcode20
        if str(self.root.attrib['language']).upper() != 'IPPCODE20':
            self.Print_Error(32, "ERROR: atribut 'language' postrada IPPcode20")
        number_of_orders = []
        #kontrola elementu v program
        for element in self.root:
            #testovani zda se jedna o element instrukce
            if element.tag != 'instruction':
                self.Print_Error(32, "ERROR: element v 'programu' musi byt instruction")
            #testovani zda nechybi atribut opcode
            if 'opcode' not in element.attrib:
                self.Print_Error(32, "ERROR: chybi opcode v instruction")
            #testovani zda nechybi atribut order
            if 'order' not in element.attrib:
                self.Print_Error(32, "ERROR: chybi order v instruction")
            #testovani zda se order rovna cislu
            if not re.search(r'^[0-9]+$', str(element.attrib['order'])):
                self.Print_Error(32, "ERROR: order musi byt kladne cislo")
            #testovani duplicitnich order
            if element.attrib['order'] not in number_of_orders:
                number_of_orders.append(element.attrib['order'])
            else:
                self.Print_Error(32, "ERROR: duplicitni cislo order")
            #testovani stringu mimo instrukci
            if re.search(r'\w', element.tail):
                self.Print_Error(32, "ERROR: string mezi instructions")
            #testovani argumentu instrukce
            check_atr = []
            for atribut in element:
                #kontrola arg1, arg2, arg3
                if not re.search('^(arg)(1|2|3)$', str(atribut.tag)):
                    self.Print_Error(32, "ERROR: argument muze byt pouze arg1, arg2, arg3")
                #kontroloa duplicity arg
                if atribut.tag in check_atr:
                    self.Print_Error(32, "ERROR: duplicitni nazev argumentu")
                check_atr.append(atribut.tag)

                #testovani zda nechybi atribut type
                if 'type' not in atribut.attrib:
                    self.Print_Error(32, "ERROR: chybi atribut type")
                #testovani atributu type
                if atribut.attrib['type'] not in ['int', 'bool', 'string', 'label', 'type', 'var', 'nil']:
                    self.Print_Error(32, "ERROR: chybna hodnota atributu type")
    #kontrola promenne
    def Check_Var(self, element):
        if element.attrib['type'] != 'var':
            self.Print_Error(32, "ERROR: chybna hodnota atributu type u promenne")
        if not re.search('^(LF|TF|GF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$', str(element.text)):
            self.Print_Error(32, "ERROR: chybny nazev promenne")

    #kontrola konstanty
    def Check_Symb(self, element):
        if element.attrib['type'] not in ['int', 'nil', 'bool', 'string']:
            self.Print_Error(32, "ERROR: chybna hodnota atributu type u promenne")
        if element.attrib['type'] == 'nil':
            if not re.search('^nil$', str(element.text)):
                self.Print_Error(32, "ERROR: chybna data v konstante nil")
        if element.attrib['type'] == 'bool':
            if not re.search('^(true|false)$', str(element.text)):
                self.Print_Error(32, "ERROR: chybna data v konstante bool")
        if element.attrib['type'] == 'int':
            if not re.search('^[+-]?[0-9]+$', str(element.text)):
                self.Print_Error(32, "ERROR: chybna data v konstante int")
        if element.attrib['type'] == 'string':
            if re.search('(\\\\[0-9]{0,2}($|[a-zA-Z]|/|<|_|-|&|%|\*|!|\?))|(#|\s)', str(element.text)):
                self.Print_Error(32, "ERROR: chybna data v konstante string")

    #kontrola promenne a konstanty
    def Check_Both(self, element):
        if element.attrib['type'] not in ['var', 'int', 'nil', 'bool', 'string']:
            self.Print_Error(32, "ERROR: chybna hodnota atributu type u promenne")
        if element.attrib['type'] == 'var':
            self.Check_Var(element)
        else:
            self.Check_Symb(element)

    #kontrola typu Type
    def Check_Type(self, element):
        if element.attrib['type'] != 'type':
            self.Print_Error(32, "ERROR: chybna hodnota atributu type u promenne")
        if not re.search('^(int|bool|string)$', str(element.text)):
            self.Print_Error(32, "ERROR: chybny datovy typ")

    #kontrola Labelu
    def Check_Label(self, element):
        if element.attrib['type'] != 'label':
            self.Print_Error(32, "ERROR: chybna hodnota atributu type u promenne")
        if not re.search('^[a-zA-Z0-9_\-$&%*!?]+$', str(element.text)):
            self.Print_Error(32, "ERROR: chybny nazev label")

    #syntakticka kontrola xml
    def Check_Syntax(self):

        Arg_Inst = Arg_Instruction()
        #pro kazdou instrukci
        for element in self.root:
            if element.attrib['opcode'] in ['CREATEFRAME', 'PUSHFRAME', 'POPFRAME', 'RETURN', 'BREAK']:
                #kontrola poctu argumentu instrukce
                if len(list(element)) != 0:
                    self.Print_Error(32, "ERROR: spatny pocet argumentu")
                #pridani instrukce do listu instrukci
                self.Inst.add_list(element.attrib['order'], element.attrib['opcode'])

            elif element.attrib['opcode'] in ['DEFVAR', 'POPS']:
                #kontrola poctu argumentu instrukce
                if len(list(element)) != 1:
                    self.Print_Error(32, "ERROR: spatny pocet argumentu")
                if element[0].tag == 'arg1':
                    self.Check_Var(element[0])
                    #pridani argumentu do listu argumentu
                    Arg_Inst.add_list("arg1", element[0].attrib['type'], element[0].text)
                else:
                    self.Print_Error(32, "ERROR: spatny nazev parametru instrukce")
                #serazeni argumentu
                Arg_Inst.list_sort()
                #pridani instrukce do listu instrukci
                self.Inst.add_list(element.attrib['order'], element.attrib['opcode'] + " " + Arg_Inst.return_string())
                #vycisteni listu argumentu
                Arg_Inst.clear_list()

            elif element.attrib['opcode'] in ['MOVE', 'INT2CHAR', 'STRLEN', 'TYPE']:
                #kontrola poctu argumentu instrukce
                if len(list(element)) != 2:
                    self.Print_Error(32, "ERROR: spatny pocet argumentu")
                for value in element:
                    if value.tag == 'arg1':
                        self.Check_Var(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg1", value.attrib['type'], value.text)
                    elif value.tag == 'arg2':
                        self.Check_Both(value)
                        Arg_Inst.add_list("arg2", value.attrib['type'], value.text)
                    else:
                        self.Print_Error(32, "ERROR: spatny nazev parametru instrukce")
                #serazeni argumentu
                Arg_Inst.list_sort()
                #pridani instrukce do listu instrukci
                self.Inst.add_list(element.attrib['order'], element.attrib['opcode'] + " " + Arg_Inst.return_string())
                #vycisteni listu argumentu
                Arg_Inst.clear_list()

            elif element.attrib['opcode'] in ['ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'AND', 'OR', 'STRI2INT', 'CONCAT', 'GETCHAR', 'SETCHAR']:
                #kontrola poctu argumentu instrukce
                if len(list(element)) != 3:
                    self.Print_Error(32, "ERROR: spatny pocet argumentu")
                for value in element:
                    if value.tag == 'arg1':
                        self.Check_Var(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg1", value.attrib['type'], value.text)
                    elif value.tag == 'arg2':
                        self.Check_Both(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg2", value.attrib['type'], value.text)
                    elif value.tag == 'arg3':
                        self.Check_Both(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg3", value.attrib['type'], value.text)
                    else:
                        self.Print_Error(32, "ERROR: spatny nazev parametru instrukce")
                #serazeni argumentu
                Arg_Inst.list_sort()
                #pridani instrukce do listu instrukci
                self.Inst.add_list(element.attrib['order'], element.attrib['opcode'] + " " + Arg_Inst.return_string())
                #vycisteni listu argumentu
                Arg_Inst.clear_list()

            elif element.attrib['opcode'] in ['READ']:
                #kontrola poctu argumentu instrukce
                if len(list(element)) != 2:
                    self.Print_Error(32, "ERROR: spatny pocet argumentu")
                for value in element:
                    if value.tag == 'arg1':
                        self.Check_Var(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg1", value.attrib['type'], value.text)
                    elif value.tag == 'arg2':
                        self.Check_Type(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg2", value.attrib['type'], value.text)
                    else:
                        self.Print_Error(32, "ERROR: spatny nazev parametru instrukce")
                #serazeni argumentu
                Arg_Inst.list_sort()
                #pridani instrukce do listu instrukci
                self.Inst.add_list(element.attrib['order'], element.attrib['opcode'] + " " + Arg_Inst.return_string())
                #vycisteni listu argumentu
                Arg_Inst.clear_list()

            elif element.attrib['opcode'] in ['CALL', 'LABEL', 'JUMP']:
                #kontrola poctu argumentu instrukce
                if len(list(element)) != 1:
                    self.Print_Error(32, "ERROR: spatny pocet argumentu")
                if element[0].tag == 'arg1':
                    self.Check_Label(element[0])
                    #pridani argumentu do listu argumentu
                    Arg_Inst.add_list("arg1", element[0].attrib['type'], element[0].text)
                else:
                    self.Print_Error(32, "ERROR: spatny nazev parametru instrukce")
                #serazeni argumentu
                Arg_Inst.list_sort()
                #pridani instrukce do listu instrukci
                self.Inst.add_list(element.attrib['order'], element.attrib['opcode'] + " " + Arg_Inst.return_string())
                #vycisteni listu argumentu
                Arg_Inst.clear_list()

            elif element.attrib['opcode'] in ['JUMPIFEQ', 'JUMPIFNEQ']:
                #kontrola poctu argumentu instrukce
                if len(list(element)) != 3:
                    self.Print_Error(32, "ERROR: spatny pocet argumentu")
                for value in element:
                    if value.tag == 'arg1':
                        self.Check_Label(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg1", value.attrib['type'], value.text)
                    elif value.tag == 'arg2':
                        self.Check_Both(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg2", value.attrib['type'], value.text)
                    elif value.tag == 'arg3':
                        self.Check_Both(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg3", value.attrib['type'], value.text)
                    else:
                        self.Print_Error(32, "ERROR: spatny nazev parametru instrukce")
                #serazeni argumentu
                Arg_Inst.list_sort()
                #pridani instrukce do listu instrukci
                self.Inst.add_list(element.attrib['order'], element.attrib['opcode'] + " " + Arg_Inst.return_string())
                #vycisteni listu argumentu
                Arg_Inst.clear_list()

            elif element.attrib['opcode'] in ['PUSHS', 'WRITE', 'EXIT', 'DPRINT']:
                #kontrola poctu argumentu instrukce
                if len(list(element)) != 1:
                    self.Print_Error(32, "ERROR: spatny pocet argumentu")
                if element[0].tag == 'arg1':
                    self.Check_Both(element[0])
                    #pridani argumentu do listu argumentu
                    Arg_Inst.add_list("arg1", element[0].attrib['type'], element[0].text)
                else:
                    self.Print_Error(32, "ERROR: spatny nazev parametru instrukce")
                #serazeni argumentu
                Arg_Inst.list_sort()
                #pridani instrukce do listu instrukci
                self.Inst.add_list(element.attrib['order'], element.attrib['opcode'] + " " + Arg_Inst.return_string())
                #vycisteni listu argumentu
                Arg_Inst.clear_list()

            elif element.attrib['opcode'] in ['NOT']:
                #kontrola poctu argumentu instrukce
                if len(list(element)) != 2:
                    self.Print_Error(32, "ERROR: spatny pocet argumentu")
                for value in element:
                    if value.tag == 'arg1':
                        self.Check_Var(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg1", value.attrib['type'], value.text)
                    elif value.tag == 'arg2':
                        self.Check_Both(value)
                        #pridani argumentu do listu argumentu
                        Arg_Inst.add_list("arg2", value.attrib['type'], value.text)
                    else:
                        self.Print_Error(32, "ERROR: spatny nazev parametru instrukce")
                #serazeni argumentu
                Arg_Inst.list_sort()
                #pridani instrukce do listu instrukci
                self.Inst.add_list(element.attrib['order'], element.attrib['opcode'] + " " + Arg_Inst.return_string())
                #vycisteni listu argumentu
                Arg_Inst.clear_list()

            else:
                self.Print_Error(32, "ERROR: nepodporovany opcode instrukce")

        #serazeni instrukci podle order
        self.Inst.list_sort()
        #vlozeni instrukci do ListInstruction
        for object in self.Inst.list_return():
            self.Inst_List.insert_instruction(object.content)
