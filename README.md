# moses_noten
Python script for an automatic entry of students homework grades for math tutors at the TU Berlin. <br/>

Step by Step guide to use the script:<br/>

Step 1: if you never used Python -> (VERY RECOMMENDED!) watch this video to install spyder (O:00 -> 2:22 min) https://youtu.be/dZfuAx5cW3w  

Step 2: two csv files are NECESSARY before running the code:
    2.1: sing in into your MOSES account -> Teilleistungen -> Teilleistungverwaltung > [Teilleistungen Ergebnisse der Veranstaltung bearbeiten] -> Hausaufgaben ->            select a Homework that has not been graded > Alle studierende aus meinen Tutorien > (scroll down) > Gespeicherte Ergebnisse als CSV Datei -> name the file          eintragungsliste.csv
    2.2: sing in into your ISIS account -> Go to the page of the math subject (Modul) you are tutoring -> On the left column, click on Teilnehmer/innen -> (scroll            down) -> Click on 'Alle {number} Nutzer/innen Auswählen' -> Next to 'Für ausgewählte Nutzer/innen …' select: 'Komma separierte Werte (.csv)' -> name the            file Teilnehmerliste.csv
    2.3: put the files in the same directory as the python files (add_remove_moses.py, configuration_moses.py, grades_moses.py) and PLEASE MAKE SURE that the files          are correctly named eintragungsliste.csv (the file downloaded from moses) and Teilnehmerliste.csv (the file downloaded from ISIS) 
    
Step 3: assign students to groups: 
    open configuration_moses.py with your preferred IDE (spyder for example, as in the linked video) -> run the code (the green arrow top left in spyder) -> please     read CAREFULLY all the messages in the console (bottom right in spyder), you will be guided through the configuration 

Step 4: final step is inserting grades:
    4.1: for homework without an online part -> directy go to step 4.3
    4.2: if there exists an online part of the homework: sing in into your ISIS account -> Go to the page of the math subject (Modul) you are tutoring -> go the              online homework -> Tabellendaten herunterladen als Komma separierte Werte (.csv) -> name the file as follows HAweeknumber.csv (VERY IMPORTANT!) -> example:          HA7.csv for week 7, HA10.csv for week 10 -> put the file in the same directory as the other files   
    4.3: open grades_moses.py with your preferred IDE (spyder for example, as in the linked video) -> run the code (the green arrow top left in spyder) -> please            read CAREFULLY all the messages in the console (bottom right in spyder), you will be guided through the grading.  
 
 
 If you wish to add, remove a student from a group or modify the email address -> run add_remove.py and read the messages in the console. 
