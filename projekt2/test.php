<?php
####  AUTHOR: Daniel Kamenicky ( xkamen21 )  ####
####  PROJECT: IPP 2019/2020                 ####
####  DATE: 14. 4. 2020                      ####
####  SUBJECT: test.php                      ####

class Parameters
{
    public $recursive; #rekurzivni prohledavani
    public $parseOnly; #pouze parse.php
    public $intOnly; #pouze interpret.py

    public $directoryPath; #cesta k adresari
    public $parseScript; #cesta ke skriptu parse.php
    public $interpretScript; #cesta k skriptu interpret.py
    public $jexamPath; #cesta k A7Soft JExamXML


    public function __construct() {
        $this->recursive = false;
        $this->parseOnly = false;
        $this->intOnly = false;

        $this->directoryPath = getcwd();
        $this->parseScript = './parse.php';
        $this->interpretScript = './interpret.py';
        $this->jexamPath = './pub/courses/ipp/jexamxml/jexamxml.jar';
    }

    public function CheckParamas($argc, $argv) {
        #falgy pro kontrolu zakazane kombinace argumentu
        $ParseOnly_flag = 0;
        $ParseScript_flag = 0;
        $InterpretScript_flag = 0;
        $IntOnly_flag = 0;
        if ($argc==1) {
            return;
        }
        else {
            for ($i=1; $i < $argc; $i++) {
                #--help
                if ($argv[$i] == "--help" && $argc == 2) {
                    if($argc == 2) {
                        echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HELP <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n".
                        "Pro správné spuštění musíte zadat do příkazové řádky: \n\n         php7.4 test.php %arguments%{0,7}\n\n" .
                        "         %arguments%\n\n" .
                        "         --int-only - pro provedeni pouze interpetu, nesmi se kombinovat s --parse-only\n\n" .
                        "         --parse-only - pro provedeni pouze parseru, nesmi se kombinovat s --int-only\n\n" .
                        "         --recursive - pro provedeni vsech adresaru\n\n" .
                        "         --directory= - pro vlozeni cesty k danemu adresari s testy\n\n" .
                        "         --parse-script= - pro vlozeni cesty parse.php\n\n" .
                        "         --int-script= - pro vlozeni cesty interpret.py\n\n" .
                        "         --jexamxml= - pro vlozeni cesty k nastroji A7Soft JExamXML\n\n" .
                        "Pro napovedu zadejte: \n\n         php7.4 test.php --help\n".
                        ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n";
                        exit(0);
                    }
                    else {
                        error_log("parametr '--help' nesmi byt v kombinaci s zadnym jinym parametrem");
                        exit(10);
                    }

                }
                #--directory=
                elseif (preg_match('/^(--directory=).*$/', $argv[$i])) {
                    $this->directoryPath = substr($argv[$i], 12);
                    if (!file_exists($this->directoryPath)) {
                        error_log("zadana slozka neexistuje");
                        exit(10);
                    }
                }
                #--parse-script=
                elseif (preg_match('/^(--parse-script=).*$/', $argv[$i])) {
                    $this->parseScript = substr($argv[$i], 15);
                    if ($IntOnly_flag == 1)
                    {
                        error_log("zakazana kombinace parametru");
                        exit(10);
                    }
                    if (!file_exists($this->parseScript)) {
                        error_log("soubor parse.php neexistuje");
                        exit(10);
                    }
                    $ParseScript_flag = 1;
                }
                #--int-script=
                elseif (preg_match('/^(--int-script=).*$/', $argv[$i])) {
                    $this->interpretScript = substr($argv[$i], 13);
                    if ($ParseOnly_flag == 1)
                    {
                        error_log("zakazana kombinace parametru");
                        exit(10);
                    }
                    if (!file_exists($this->interpretScript)) {
                        error_log(" soubor interpret.py neexistuje");
                        exit(10);
                    }
                    $InterpretScript_flag = 1;
                }
                #--jexamxml=
                elseif (preg_match('/^(--jexamxml=).*$/', $argv[$i])) {
                    $this->jexamPath = substr($argv[$i], 11);
                    if (!file_exists($this->jexamPath)) {
                        error_log("soubor JexamXml.jar neexistuje");
                        exit(10);
                    }
                }
                #--parse-script=
                elseif (preg_match('/^(--parse-only)$/', $argv[$i])) {
                    if ($InterpretScript_flag == 1 || $IntOnly_flag == 1)
                    {
                        error_log("zakazana kombinace parametru");
                        exit(10);
                    }
                    $this->parseOnly = true;
                    $ParseOnly_flag = 1;
                }
                #--int-only=
                elseif (preg_match('/^(--int-only)$/', $argv[$i])) {
                    if ($ParseScript_flag == 1 || $ParseOnly_flag == 1)
                    {
                        error_log("zakazana kombinace parametru");
                        exit(10);
                    }
                    $this->intOnly = true;
                    $IntOnly_flag = 1;
                }
                #--recursive=
                elseif (preg_match('/^(--recursive)$/', $argv[$i])) {
                    $this->recursive = true;
                }
                #nepodporovany parametr
                else {
                    error_log("ERROR: argument neni podporovan");
                    exit(10);
                }
            }
        }
    }
}

class TemporaryFile
{
    public $file; #docasny soubor

    #vytvoreni docasneho souboru
    public function create(){
        $this->file = tmpfile();
    }

    #zruseni docasneho souboru
    public function end(){
        fclose($this->file);
    }

    #zjisteni cesty k docasnemu souboru
    public function get_path(){
        $path = stream_get_meta_data($this->file);
        return $path['uri'];
    }


}

class HTML
{
    public $html; #html kod
    public $successful; #kod uspesnych testu
    public $bad; #kod neuspesnych testu

    public function __construct() {
        $this->html = '';
        $this->successful = '';
        $this->bad = '';
    }

    #generator html kodu
    public function Generate_html($parse, $int, $counter, $counter_bad, $counter_suc) {
        if ($parse) {
            $head_text = "PARSE_ONLY";
        }
        elseif ($int) {
            $head_text = "INT_ONLY";
        }
        else {
            $head_text = "BOTH";
        }
        $this->html =
        '<!DOCTYPE html>
        <html lang="cs">
        <head>
            <meta charset="UTF-8">
            <title>IPP test.php parse.php interpret.py</title>
            <style>
                body{
                    background-color: black;
                    color: grey;
                }

                body li{
                    display: block;
                    max-width: 1240px;
                    min-width: 1150px;
                    line-height: 1.5em;
                    margin: auto;
                    height: auto;
                    border-style: solid;
                    border-width: thin;
                }

                .head{
                    text-align: center;
                    color: grey;
                    }
                .head h2{
                    font-size: 30px;
                }

                .head a{
                    text-decoration: none;
                    color: #fff;
                    font-family: Monoton;
                    -webkit-animation: color2 1.5s ease-in-out infinite alternate;
                    -moz-animation: color2 1.5s ease-in-out infinite alternate;
                    animation: color2 1.5s ease-in-out infinite alternate;
                }

                .head a:hover{
                    color: #FF1177;
                    -webkit-animation: none;
                    -moz-animation: none;
                    animation: none;
                }

                .end h2{
                    font-size: 30px;
                    color: white;
                     font-family: Monoton;
                     -webkit-animation: color1 1.5s ease-in-out infinite alternate;
                     -moz-animation: color1 1.5s ease-in-out infinite alternate;
                     animation: color1 1.5s ease-in-out infinite alternate;
                }

                .end{
                    text-align: center;
                }

                .dobre{
                    font-size: 20px;
                }

                .left{
                    float: right;
                    padding-right: 10px;
                }

                .successful{
                    color: green;
                    float: right;
                    padding-right: 10px;
                }

                .successful_number{
                    color: green;
                }

                .test{
                    padding-right: 50px;
                    padding-left: 10px;
                }

                .bad{
                    color: red;
                }

                .upper{
                    text-align: center;
                    color: green;
                }

                .middle{
                    text-align: center;
                    color: red;
                }
                .head h2{
                    color: #fff;
                     font-family: Monoton;
                     -webkit-animation: color1 1.5s ease-in-out infinite alternate;
                     -moz-animation: color1 1.5s ease-in-out infinite alternate;
                     animation: color1 1.5s ease-in-out infinite alternate;
                }


                @-webkit-keyframes color1 {
                    from {
                      text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #228DFF, 0 0 70px #228DFF, 0 0 80px #228DFF, 0 0 100px #228DFF, 0 0 150px #228DFF;
                    }
                    to {
                      text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #fff, 0 0 20px #228DFF, 0 0 35px #228DFF, 0 0 40px #228DFF, 0 0 50px #228DFF, 0 0 75px #228DFF;
                    }
                }

                @-webkit-keyframes color2 {
                    from {
                        text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #FF1177, 0 0 70px #FF1177, 0 0 80px #FF1177, 0 0 100px #FF1177, 0 0 150px #FF1177;
                    }
                    to {
                        text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #fff, 0 0 20px #FF1177, 0 0 35px #FF1177, 0 0 40px #FF1177, 0 0 50px #FF1177, 0 0 75px #FF1177;
                    }
                }
            </style>
        </head>
        <body>
            <div class="head">
                <h2 class="head_1">Vysledky testu '.$head_text.' projektu IPP</h2>
                <p>Pro vysledne skore kliknete <a href="#end">zde</a></p>
            </div>
            <hr>
            <h2 class="upper">Successful tests:</h2>
            <ul>';

            $this->html = $this->html . $this->successful;

            $this->html = $this->html . '</ul>

            <hr>
            <h2 class="middle">Failed tests:</h2>

            <ul>';
            $this->html = $this->html . $this->bad;

            $this->html = $this->html . '</ul>
            <hr>
            <div class="end">
                <h2 class="head_1"><a id=end></a>Celkove skore:</h2>
                <a id=dobre class="dobre">SUCCESSFUL : <font class="successful_number">'.$counter_suc.'</font>/'.$counter.' ( <font class="successful_number">'. number_format($counter_suc/$counter*100, 2) .'%</font> )</a>
                <p id=dobre class="dobre">BAD : <font class="bad">'.$counter_bad.'</font>/'.$counter.'</p>
            </div>
        </body>
        </html>';

        echo $this->html;
    }

    #generator html kodu uspesnych testu
    public function Generate_successful($count, $path) {
        $this->successful = $this->successful . '<li><font class="test">'.$count.' TEST : </font>' . $path . '<font class="successful"> SUCCESSFUL </font></li>';
    }

    #generator html kodu neuspesnych testu
    public function Generate_bad($count, $path, $returned, $expected) {
        $this->bad = $this->bad . '<li><font class="test">'.$count.' TEST : </font>' . $path . '<div class="left"><font class="bad"> FAILED </font> | returned code: <font class="bad"> '.$returned.' </font> | expected code: <font class="successful_number"> '.$expected.' </font></div></li>';
    }


}

$result = new HTML(); #instance html generatoru

$Param = new Parameters(); #instance kontroly parametru
$Param->CheckParamas($argc, $argv); #kontrola parametru

$Directory = new RecursiveDirectoryIterator($Param->directoryPath);
if ($Param->recursive)
    $Iterator = new RecursiveIteratorIterator($Directory);
else
    $Iterator = new IteratorIterator($Directory);

$Regex = new RegexIterator($Iterator, '/^.+\.src$/i', RecursiveRegexIterator::GET_MATCH);

#docasne soubory
$tmp1 = new TemporaryFile();
$tmp2 = new TemporaryFile();

#pocitadlo vsech testu
$test_counter = 0;
#pocitadlo vsech uspesnych testu
$successful_counter = 0;
#pocitadlo vsech neuspesnych testu
$bad_counter = 0;

#kontrola souboru .src .in .out .rc
foreach ($Regex as $key) {
    $test_counter++;
    $File_Path_and_Name =  substr_replace($key[0], '', -4);
    if (!file_exists($File_Path_and_Name.".rc")) {
        file_put_contents($File_Path_and_Name.".rc", "0");
    }
    if (!file_exists($File_Path_and_Name.".in")) {
        file_put_contents($File_Path_and_Name.".in", "");
    }
    if (!file_exists($File_Path_and_Name.".out")) {
        file_put_contents($File_Path_and_Name.".out", "");
    }

    #parse only
    if ($Param->parseOnly) {
        $tmp1->create();
        unset($ParseOutput);
        #provedeni parse.php
        exec('php7.4 ' . $Param->parseScript . ' ' . "<" . $File_Path_and_Name.".src" . ">" . $tmp1->get_path(), $ParseOutput, $ParseReturnCode);
        if ( $ParseReturnCode == 0 ) {
            #porovnani vysledku s nastrojem A7Soft JExamXML
            exec('java -jar ' . $Param->jexamPath . " " . $tmp1->get_path() . ' ' . $File_Path_and_Name.".out", $output, $diffReturnCode);
            if ($diffReturnCode == 0) {
                $successful_counter++;
                $result->Generate_successful($successful_counter, $File_Path_and_Name.".src");
            }
            else {
                $bad_counter++;
                $result->Generate_bad($bad_counter, $File_Path_and_Name.".src", $diffReturnCode, file_get_contents($File_Path_and_Name.".rc"));
            }
        }
        else {
            if ( $ParseReturnCode == file_get_contents($File_Path_and_Name.".rc") ){
                $successful_counter++;
                $result->Generate_successful($successful_counter, $File_Path_and_Name.".src");
            }
            else {
                $bad_counter++;
                $result->Generate_bad($bad_counter,$File_Path_and_Name.".src", $ParseReturnCode, file_get_contents($File_Path_and_Name.".rc"));
            }
        }
        $tmp1->end();

    }
    #interpret only
    elseif ($Param->intOnly) {
        $tmp1->create();
        unset($InterpretOutput);
        #provedeni interpret.py
        exec("python3.8 " . $Param->interpretScript . " --source=" . $File_Path_and_Name.".src" . " --input=" . $File_Path_and_Name.".in" . ">" . $tmp1->get_path(), $InterpretOutput, $InterpretReturnCode);
        if ( $InterpretReturnCode == 0 ) {
            #porovnani vysledku s nastrojem diff
            exec('diff ' . $tmp1->get_path() . ' ' . $File_Path_and_Name.".out", $output, $diffReturnCode);
            if ($diffReturnCode == 0) {
                $successful_counter++;
                $result->Generate_successful($successful_counter, $File_Path_and_Name.".src");
            }
            else {
                $bad_counter++;
                $result->Generate_bad($bad_counter, $File_Path_and_Name.".src", $diffReturnCode, file_get_contents($File_Path_and_Name.".rc"));
            }
        }
        else {
            if ( $InterpretReturnCode == file_get_contents($File_Path_and_Name.".rc") ){
                $successful_counter++;
                $result->Generate_successful($successful_counter, $File_Path_and_Name.".src");
            }
            else {
                $bad_counter++;
                $result->Generate_bad($bad_counter, $File_Path_and_Name.".src", $InterpretReturnCode, file_get_contents($File_Path_and_Name.".rc"));
            }
        }
        $tmp1->end();
    }
    #oboji
    else {
        unset($ParseOutput);
        $tmp1->create();
        $tmp2->create();
        #provedeni parse.php
        exec('php7.4 ' . $Param->parseScript . ' ' . "<" . $File_Path_and_Name.".src" . ">" . $tmp1->get_path(), $ParseOutput, $ParseReturnCode);
        if ( $ParseReturnCode == 0 ) {
            unset($InterpretOutput);
            #provedeni interpret.py
            exec("python3.8 " . $Param->interpretScript . " --source=" . $tmp1->get_path() . " --input=" . $File_Path_and_Name.".in". ">" . $tmp2->get_path(), $InterpretOutput, $InterpretReturnCode);
            if ($InterpretReturnCode == 0) {
                #porovnani vysledku s nastrojem diff
                exec('diff ' . $tmp2->get_path() . ' ' . $File_Path_and_Name.".out", $output, $diffReturnCode);
                if ($diffReturnCode == 0) {
                    $successful_counter++;
                    $result->Generate_successful($successful_counter, $File_Path_and_Name.".src");
                }
                else {
                    $bad_counter++;
                    $result->Generate_bad($bad_counter, $File_Path_and_Name.".src", $diffReturnCode, file_get_contents($File_Path_and_Name.".rc"));
                }
            }
            else {
                if ( $InterpretReturnCode == file_get_contents($File_Path_and_Name.".rc") ){
                    $successful_counter++;
                    $result->Generate_successful($successful_counter, $File_Path_and_Name.".src");
                }
                else {
                    $bad_counter++;
                    $result->Generate_bad($bad_counter, $File_Path_and_Name.".src", $InterpretReturnCode, file_get_contents($File_Path_and_Name.".rc"));
                }
            }
        }
        else {
            if ( $ParseReturnCode == file_get_contents($File_Path_and_Name.".rc") ){
                $successful_counter++;
                $result->Generate_successful($successful_counter, $File_Path_and_Name.".src");
            }
            else {
                $bad_counter++;
                $result->Generate_bad($bad_counter, $File_Path_and_Name.".src", $ParseReturnCode, file_get_contents($File_Path_and_Name.".rc"));
            }
        }
        $tmp1->end();
        $tmp2->end();
    }

}

#generovani konecnych vysledku testu
$result->Generate_html($Param->parseOnly, $Param->intOnly, $test_counter, $bad_counter, $successful_counter);
?>
