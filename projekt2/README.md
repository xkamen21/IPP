## Implementační dokumentace k 2. úloze do IPP 2019/2020
##### **Jméno a příjmení:** Daniel Kamenický
##### **Login:** xkamen21
---
### 1. Skript `interpret.py`
Interpret XML reprezentace kódu. Skript má za úkol načíst XML reprezentaci kódu a interpretovat předaný kód na standardní výstup. Skript je navrhunt objektově a rozdělen do několika modulů.
Jak už bylo zmíněno, celý skript je rozdělen do modulů a to přesně do devíti. Modul, nesoucí název **`interpret.py`**, je mozkem celého programu. Z daného modulu je celý program řízen, tudíž daný modul slouží i pro spuštění. Například:
```ssh
python3.8 interpret.py --source=source_file.src --input=input_file.in
```
Dále program pracuje s těmito moduly: **`arg_instruction.py`**, **`aguments.py`**, **`error.py`**, **`frames.py`**, **`instruction.py`**, **`list_of_instructions.py`**, **`stack.py`**, **`xml_parser`**.

#### Přehled modulů a jejich vysvětlení:
##### INTERPERT
Modul bere instrukce z hlavního listu (Main_List) v nekonečném cyklu **while**. Proměnná **iterator** je v každém jednom cyklu inkrementována a slouží jako klíč hlavního listu. Z while cyklu se dostanemev případě chybové hlášky, nebo když skript dojede na konec zdrojového kódu. While cyklus se skládá z mnoha dotazů **if**, které rozpoznají a vykonají příslušnou instrukci. Výsledek je interpretován na standardní výstup.

---
##### ARG_INSTRUCTION
Modul má na starost seřazení argumentů dané instrukce.

---
##### ARGUMENTS
Modul zařizuje správné zkontrolování a předání argumentů skriptu.

---
##### ERROR
Modul zaručuje vypsání chybové hlášky na standardní chybový výstup a vrácení správného chybového kódu.

---
##### FRAMES
Modul má na starost práci s rámci. Dále do nich zapisuje hodnoty a názvy proměnných. Také pracuje s daty v proměnných uložených v rámcích, například při instrukci **SETCHAR**, nebo při vypsání dat či zjištění datového typu uchovaného v proměnné.

---
##### INSTRUCTION
Modul má na starosti seřazení celé posloupnosti instrukcí podle parametru **order**.

---
##### LIST OF INSTRUCTIONS
Modul pracuje s hlavním listem, ve kterém jsou uloženy výsledné instrukce převedené z XML reprezentace. Instrukce v listu má jako klíč celé číslo a všechny klíče jsou reprezentovány jako posloupnost celých čísel od 1 a slouží také jako číslování řádků kódu pro případné skoky. Hodnotou listu jsou pak dané instrukce uložené v řetězci. Dále modul obsahuje list návěští, ve kterém jsou uloženy všechny návěští, které kód obsahuje. Klíčem je zde zvolené jméno návěští a hodnota je pozice kódu, kde se dané návěští vyskytuje. Modul při instrukci **JUMP** vezme jméno návěští a z listu vrátí pozici v kódu. Modul také pracuje s instrukcemi **CALL** a **RETURN** a zásobníkem volání (call_stack).

---
##### STACK
Modul reprezentuje datový zásobník. Umožňuje vkládát a odebírat hodnoty ze zásobníku pomocí instrukcí **POPS** a **PUSHS**.

---
##### XML PARSER
Skript načítá XML reprezentaci zdrojového kódu. V průběhu načítání kódu provádí syntaktickou a lexikální analýzu. Vysledné vygenerované instrukce ukládá do hlavního listu instrukcí (Main_List).  

---
#### Parametry interpretu:
Interpret má 3 parametry které můžeme zadat. Jedním z nich je parametr __( --help )__ , který vypíše pomocné informace, které uživatel potřebuje k spuštění skriptu. Parametr help se nesmí kombinovat s jinými parametry, jinak nastane chyba. Zbylé dva parametry slouží pro vložení speciálních souborů a to zdrojového souboru __( --source= )__ a vstupního souboru __( --input= )__.
### 2. Skript `test.php`
Skript **test.php** slouží pro testování skriptů **parse.php** a **interpret.py**. Skript v celku pracuje pouze s 4 typy souborů a potřebnými skripty. Soubor s příponou **.src** slouží jako zdrojový soubor. Soubor s příponou **.out** obsahuje výsledný interpret, který by daný skript měl vrátit. S timto souborem je výstup porovnáván pomocí nástroje **diff**. V případě **parse.php** porovnáváme XML reprezentaci, zde musíme použít nástroj **A7Soft JExamXML**. Soubor s příponou **.rc** obsahuje návratový kód který by měl vrátit daný skript. Posledním soubor obsahuje příponu **.in** a jedná se o vstupní soubor.
Skript také pracuje s mnoha parametry. Parametr **( --int-only )** slouží jen pro porovnání interpretu. Parametr **( --parse-only )** slouží jen pro porovnání parseru. Parametr **( --help )** vypíše potřebné informace k spuštění a nesmí být kombinován s žádným jiným parametrem. Parametr **( --directory= )** slouží pro vložení cesty k dané složce, která obsahuje potřebné soubory k testování. V případě absence parametru je nastavena cesta **./**. Parametr **( --recursive )** slouží pro průchod všemi adresáří, které se nachází v adresáři předaném pomocí --directory=. Parametr **( --int-script= )** slouží pro předání cesty k skriptu **interpret.py**. Při absenci je nastavena cesta **./interpret.py**. Parametr **( --parse-script= )** slouží pro předání cesty k skriptu **parse.php**. Při absenci je nastavena cesta **./parse.php**. Poslední parametr **( --jexamxml= )** pro cestu k JAR balíčku obsahujicí nástroj **A7Soft JExamXML**.
