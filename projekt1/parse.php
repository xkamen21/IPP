<?php

include 'parse_lib/scanner_and_syntax.php';
include 'parse_lib/generator.php';

$instruction = array(
    0 => "MOVE",
    1 => "CREATEFRAME",
    2 => "PUSHFRAME",
    3 => "POPFRAME",
    4 => "DEFVAR",
    5 => "CALL",
    6 => "RETURN",
    7 => "PUSHS",
    8 => "POPS",
    9 => "ADD",
    10 => "SUB",
    11 => "MUL",
    12 => "IDIV",
    13 => "LT",
    14 => "GT",
    15 => "EQ",
    16 => "AND",
    17 => "OR",
    18 => "NOT",
    19 => "INT2CHAR",
    20 => "STRI2INT",
    21 => "READ",
    22 => "WRITE",
    23 => "CONCAT",
    24 => "STRLEN",
    25 => "GETCHAR",
    26 => "SETCHAR",
    27 => "TYPE",
    28 => "LABEL",
    29 => "JUMP",
    30 => "JUMPIFEQ",
    31 => "JUMPIFNEQ",
    32 => "EXIT",
    33 => "DPRINT",
    34 => "BREAK");

$generator_index = 0; // muze nabyvat hodnoty 1-9 jinka error

function CheckParamas($argc, $argv)
{
    if($argc==1)
    {
        return 0;
    }
    elseif ($argc == 2 && $argv[1]=="--help")
    {
        echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HELP <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n".
        "Pro správné spuštění musíte zadat do příkazové řádky: \n\n         php parse.php <%nazev_souboru%\n\n" .
        "         %nazev_souboru% - soubor ktery obsahuje vas vstupni kod IPPcode20\n\n" .
        "Pro napovedu zadejte: \n\n         php parse.php --help\n".
        ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n";
        exit(0);
    }
    else
    {
        error_log("Pro napovedu zadejte jediny parametr '--help'");
        exit(10);
    }
}

if(CheckParamas($argc, $argv) != 0)
{
    exit(10); //spatny pocet parametru
}

//////////////////////////// KONTROLA HLAVICKY A KOMENTARU NAD NI //////////////////////////////
do {
    $line = fgets(STDIN);
    if(feof(STDIN) && $line == '')
        exit(21);
} while (preg_match('/^[ ]*#|^[ ]*$/', $line)); //kontrola komentaru a prazdnych radku pred hlavickou .IPPCode20

if(!preg_match('/^[ ]*[.]+[iI]{1}+[pP]{2}+[cC]{1}+[oO]{1}+[dD]{1}+[eE]{1}+[2]{1}+[0]{1}[ ]*([#]+.*)*$/', $line)) : //REGEX pro .IPPCode20 i s komentarem
    error_log("Error: spatne zadana hlavicka IPPcode20");
    exit(21); // soubor nezacal s hlavickou .IPPCode20 nebo se zde vyskytla jina chyba
endif;
///////////////////////////////////////////////////////////////////////////////////////////////

generate();

?>
