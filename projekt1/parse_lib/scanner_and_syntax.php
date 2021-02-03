<?php

$NOT_flag = 0;

function GetNumberOfInstruction($word)
{
    global $instruction;
    $counter = 0;
    foreach ($instruction as $tmp)
    {
        if(preg_match("~^" . $tmp . "$~i", $word))
        {
            return $counter;
        }
        $counter++;
    }
    exit(22);
}

function Check_VAR($word)
{
    if(preg_match('/^(LF|TF|GF)@.*/', $word))
    {
        if(!preg_match('/^(LF|TF|GF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/', $word))
        {
            exit(23); #chyba zapsani promenne
        }
    }
    else
    {
        exit(23); #nejedna se o variable
    }
}

function Check_SYMB($word)
{
    global $NOT_flag;
    if(preg_match('/^(LF|TF|GF)@.*/', $word))
    {
        if(!preg_match('/^(LF|TF|GF)@[a-zA-Z0-9_\-$&%*!?]+$/', $word))
        {
            exit(23); #chyba zapsani promenne
        }
    }
    else
    {
        if ($NOT_flag == 1) {
            exit(23);
        }
        if(preg_match('/^nil@nil$/', $word))
        {
            return;
        }
        if(preg_match('/^(int|bool|string)/', $word))
        {
            if( preg_match('/^int@[+-]?[0-9]+$/', $word)|
                preg_match('/^bool@(true|false)$/', $word))
            {
                return;
            }
            elseif(preg_match("/^string@/", $word))
            {
                if(preg_match('/(\\\[0-9]{0,2}($|\p{L}|<|_|-|&|%|\*|!|\?))/u', $word)) #(\\\[0-9]{0,2}($|\p{L}|<|_|-|&|%|\*|!|\?)|\\\[0-9]{4,}) kdyby se nepodporovalo ahoj\1234ahoj pouziju zakomentovany regex
                {
                    exit(23);
                }
                else
                {
                    return;
                }
            }
            else
            {
                exit(23);
            }
        }
        else
        {
            exit(23);
        }
    }
}

function Check_LABEL($word)
{
    if(!preg_match('/^[a-zA-Z0-9_\-$&%*!?]+$/', $word))
    {
        exit(23); #chyba zapsani labelu
    }
}

function scan_and_check()
{
    global $generator_index;
    global $NOT_flag;
    $counter = 0;
    $index = 0;

    $array_line = array(); //radek jako array
    $array_edit = array(0 => ""); // pro upraveni array ze vstupu (odstraneni prebytecnych veci)

    $line = fgets(STDIN); //nacte radek z STDIN

    $line = str_replace("\n", "", $line); //ze stringu vyhodu EOL, delalo to tam bordel


    //samostatny komentar na radku
    while (preg_match('/^[ ]*#|^[ ]*$/', $line))
    {
        $line = fgets(STDIN);
        if(feof(STDIN))
            return;
    }

    //upraveni stringu na array
    $array_line = explode(" ", $line);

    //odstraneni prebytecnych veci ve stringu jako sou mezery a EOL
    $array_line = array_values(array_diff($array_line,$array_edit));

    //kontrola EOF
    if(feof(STDIN))
    {
        if($line == '')
            return;
    }

    //kontrola komentare na radku s instrukci
    foreach ($array_line as $word) {
        if(preg_match("/^[#]+.*/", $word))
        {
            $array_line = array_slice($array_line, 0, $counter);
            $counter = 0;
            break;
        }

        if((preg_match("/[#]+.*/", $word)) )//&& !preg_match("/STRING.*/", strtoupper($array_line[1])))
        {
            while(true)
            {
                if( $word[$index] == '#')
                {
                    $array_line[$counter] = substr($word, 0, $index);
                    $index = 0;
                    break;
                }
                $index++;
            }
            $array_line = array_slice($array_line, 0, $counter+1);
            break;
        }
        $counter++;
    }


    //print_r($array_line);

    $cislo_instrukce = GetNumberOfInstruction($array_line[0]);

    switch ($cislo_instrukce) {
        case 1:
        case 2:
        case 3:
        case 6:
        case 34:
            if(count($array_line) != 1)
            {
                exit(23);
            }
            $generator_index = 1;
            break;

        case 4:
        case 8:
            if(count($array_line) != 2)
            {
                exit(23);
            }
            Check_VAR($array_line[1]);
            $generator_index = 2;
            break;

        case 0:
        case 19:
        case 24:
        case 27:
            if(count($array_line) != 3)
            {
                exit(23);
            }
            Check_VAR($array_line[1]);
            Check_SYMB($array_line[2]);
            $generator_index = 3;
            break;

        case 9:
        case 10:
        case 11:
        case 12:
        case 13:
        case 14:
        case 15:
        case 16:
        case 17:
        case 20:
        case 23:
        case 25:
        case 26:
            if(count($array_line) != 4)
            {
                exit(23);
            }
            Check_VAR($array_line[1]);
            Check_SYMB($array_line[2]);
            Check_SYMB($array_line[3]);
            $generator_index = 4;
            break;

        case 21:
            if(count($array_line) != 3)
            {
                exit(23);
            }
            Check_VAR($array_line[1]);
            if(!preg_match('/^(int|bool|string)$/', $array_line[2]))
            {
                exit(23);
            }
            $generator_index = 5;
            break;

        case 5:
        case 28:
        case 29:
            if(count($array_line) != 2)
            {
                exit(23);
            }
            Check_LABEL($array_line[1]);
            $generator_index = 6;
            break;

        case 30:
        case 31:
            if(count($array_line) != 4)
            {
                exit(23);
            }
            Check_LABEL($array_line[1]);
            Check_SYMB($array_line[2]);
            Check_SYMB($array_line[3]);
            $generator_index = 7;
            break;

        case 7:
        case 22:
        case 32:
        case 33:
            if(count($array_line) != 2)
            {
                exit(23);
            }
            Check_SYMB($array_line[1]);
            $generator_index = 8;
            break;

        case 18:
            if(count($array_line) != 3)
            {
                exit(23);
            }
            $NOT_flag = 1;
            Check_SYMB($array_line[1]);
            Check_SYMB($array_line[2]);
            $generator_index = 9;
            break;


        default:
            error_log("Spatne predana hodnota z GetNumberOfInstruction()");
            exit(99);
            break;
    }

    return $array_line;
}


?>
