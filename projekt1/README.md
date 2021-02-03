## Implementační dokumentace k 1. úloze do IPP 2019/2020
##### **Jméno a příjmení:** Daniel Kamenický
##### **Login:** xkamen21

## 1. Analyzátor zdrojového kódu IPPcode20
Analyzátor kódu IPPcode20 provádí analýzu zdrojového kódu IPPcode20 a převadí na XML reprezentaci. Vprůběhu převádění je prováděna syntaktická a lexikální kontrola. Celý program je rozdělen do 3 souborů. Prvním z nich je **parse.php** pomocí kterého se celý proces spouští zadáním do příkazové řádky, například: **php parse.php <stdin_vstup.src**. Další dva soubory jsou umístěny v adresáři **parse_lib**. Jedním ze souborů je **scanner_and_syntaxt.php** ve kterém probíhá lexikální a syntaktická analýza. Vše je prováděno ve funkci **scan_and_check**. Jednotlivý řádek je načítán a převáděn do proměnné **array_line** typu **array**, ve kterém je pak jednotlivě prozkoumáván každý úsek pomocí funkce **foreach()**. Zavoláním funkce **GetNumberOfInstruction** získáme číslo potřebné instukce. Instrukce jsem si rozdělil podle počtu parametrů, které jsem seskupil dohromady pro jednodušší kontrolu. Poslední částí je **Switch** který předává potřebné informace **generátoru**. Tím se dostáváme do poslední části, kterou je **generator.php**. Celý soubor vcelku tvoří velký **While cyklus**, který volá funkci **scan_and_check**. V cyklu je **Switch** který je rozdělen stejně, jak v předchozím souboru, podle počtu parametrů daných instrukcí. Při správném zadání vstupního souboru, pracujeme se STDIN vstupem, program vygeneruje výsledný XML kód. 

## 2. Parametr --help 
Program také dokáže poskytnout základní výpomoc. Kdyby uživatel nevěděl jak daný program spustit, může program spustit s jediným parametrem, kterým je **--help**. Po spuštění program na **stdout** vypíše potřebné věci, které potřebujete vědět ke spuštění programu. Při špatném zadání parametrů program končí s návratovou hodnotou **10**.

