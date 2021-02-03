<?php

    //funkce ktera vytvori hlavicku
    function create_XMLheader_of_instruciton($xml, $string, $number)
    {
        xmlwriter_start_element($xml, "instruction");
        xmlwriter_start_attribute($xml, "order");
        xmlwriter_text($xml, $number);
        xmlwriter_end_attribute($xml);
        xmlwriter_start_attribute($xml, "opcode");
        xmlwriter_text($xml, $string);
        xmlwriter_end_attribute($xml);
    }

    function create_XMLargument($xml, $argument, $type, $string)
    {
        xmlwriter_start_element($xml, $argument);
        xmlwriter_start_attribute($xml, "type");
        xmlwriter_text($xml, $type);
        xmlwriter_end_attribute($xml);
        xmlwriter_text($xml, $string);
        xmlwriter_end_element($xml);
    }

    function create_XMLvariable($xml, $argument, $type, $string)
    {
        if(preg_match("/^(STRING|INT|BOOL|NIL).*/", strtoupper($string)))
        {
            $array_tmp = explode("@", $string);
            xmlwriter_start_element($xml, $argument);
            xmlwriter_start_attribute($xml, "type");
            xmlwriter_text($xml, $array_tmp[0]);
            xmlwriter_end_attribute($xml);
            xmlwriter_text($xml, $array_tmp[1]);
            xmlwriter_end_element($xml);
        }
        else
        {
            xmlwriter_start_element($xml, $argument);
            xmlwriter_start_attribute($xml, "type");
            xmlwriter_text($xml, $type);
            xmlwriter_end_attribute($xml);
            xmlwriter_text($xml, $string);
            xmlwriter_end_element($xml);
        }
    }

    function generate() {
        global $generator_index;
        $instruction_counter = 1;
        $array = array();

        $xw = xmlwriter_open_memory();
        xmlwriter_set_indent($xw, 1);
        $res = xmlwriter_set_indent_string($xw, '    ');

        xmlwriter_start_document($xw, '1.0', 'UTF-8');

        xmlwriter_start_element($xw, 'program');
        xmlwriter_start_attribute($xw, 'language');
        xmlwriter_text($xw, 'IPPcode20');
        xmlwriter_end_attribute($xw);

        while (!feof(STDIN)) {

            $array = scan_and_check();

            switch ($generator_index) {
                case 1:
                    create_XMLheader_of_instruciton($xw, $array[0], $instruction_counter);
                    xmlwriter_end_element($xw);
                    break;

                case 2:
                    create_XMLheader_of_instruciton($xw, $array[0], $instruction_counter);

                    create_XMLargument($xw, "arg1", "var", $array[1]);

                    xmlwriter_end_element($xw);
                    break;

                case 3:
                    create_XMLheader_of_instruciton($xw, $array[0], $instruction_counter);

                    create_XMLargument($xw, "arg1", "var", $array[1]);

                    create_XMLvariable($xw, "arg2", "var", $array[2]);

                    xmlwriter_end_element($xw);

                    break;

                case 4:
                    create_XMLheader_of_instruciton($xw, $array[0], $instruction_counter);

                    create_XMLargument($xw, "arg1", "var", $array[1]);

                    create_XMLvariable($xw, "arg2", "var", $array[2]);

                    create_XMLvariable($xw, "arg3", "var", $array[3]);


                    xmlwriter_end_element($xw);

                    break;

                case 5:
                    create_XMLheader_of_instruciton($xw, $array[0], $instruction_counter);

                    create_XMLargument($xw, "arg1", "var", $array[1]);

                    create_XMLargument($xw, "arg2", "type", $array[2]);

                    xmlwriter_end_element($xw);

                    break;

                case 6:
                    create_XMLheader_of_instruciton($xw, $array[0], $instruction_counter);

                    create_XMLargument($xw, "arg1", "label", $array[1]);

                    xmlwriter_end_element($xw);

                    break;

                case 7:
                    create_XMLheader_of_instruciton($xw, $array[0], $instruction_counter);

                    create_XMLargument($xw, "arg1", "label", $array[1]);

                    create_XMLvariable($xw, "arg2", "var", $array[2]);

                    create_XMLvariable($xw, "arg3", "var", $array[3]);


                    xmlwriter_end_element($xw);

                    break;

                case 8:
                    create_XMLheader_of_instruciton($xw, $array[0], $instruction_counter);

                    create_XMLvariable($xw, "arg1", "var", $array[1]);

                    xmlwriter_end_element($xw);

                    break;

                case 9:
                    create_XMLheader_of_instruciton($xw, $array[0], $instruction_counter);

                    create_XMLvariable($xw, "arg1", "var", $array[1]);

                    create_XMLvariable($xw, "arg2", "var", $array[2]);

                    xmlwriter_end_element($xw);

                    break;

                default:
                    if(feof(STDIN))
                    {
                        break; //ukonceni cyklu kdyz dojdem k EOF
                    }
                    error_log("Spatne predana hodnota z funkce scan_and_check");
                    exit(99);
                    break;
            }
            $generator_index = 0;
            $instruction_counter++;
            if(feof(STDIN))
            {
                break; //ukonceni cyklu kdyz dojdem k EOF
            }

        }

        xmlwriter_end_element($xw);

        xmlwriter_end_document($xw);

        echo xmlwriter_output_memory($xw);

    }
 ?>
