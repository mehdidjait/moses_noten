# moses_noten
## Python CLI for an automatic entry of students homework grades for math tutors at the TU Berlin. (PLEASE CAREFULLY READ THE GUIDE)<br/>
###### If you have any feedback, wish to see a feature implemented or any question, PLEASE send me an email to mehdidjait@gmail.com I would be more than happy to respond! <br/><br/> Step by Step guide to use the script:

## Step 1:
<br/>
If you never used Python -> (VERY RECOMMENDED!) watch this video to install spyder -> https://youtu.be/dZfuAx5cW3w  
<br/>
<br/>
<br/>

## Step 2: Two csv files are NECESSARY before running the code:
<br/>
1. sign in into your MOSES account:
<br/>
Teilleistungen -> Teilleistungverwaltung -> Teilleistungen Ergebnisse der Veranstaltung bearbeiten -> Hausaufgaben -> select a Homework that has not been graded -> Alle studierende aus meinen Tutorien -> (scroll down) -> Gespeicherte Ergebnisse als CSV Datei -> name the file eintragungsliste.csv
<br/>
<br/>
2. sign in into your ISIS account:
<br/>
Go to the page of the math subject (Modul) you are tutoring -> On the left column, click on Teilnehmer/innen -> (scrolldown) -> Click on 'Alle {number} Nutzer/innen Auswählen' -> Next to 'Für ausgewählte Nutzer/innen …' select: 'Komma separierte Werte (.csv)' -> name the file Teilnehmerliste.csv 
<br/>
<br/>
3. put the files in the same directory as the python files (add_remove_moses.py, configuration_moses.py, grades_moses.py)

***PLEASE MAKE SURE that the files are correctly named eintragungsliste.csv (the file downloaded from moses) and Teilnehmerliste.csv (the file downloaded from ISIS)*** 
<br/>
<br/>
<br/>

## Step 3: Assign students to groups:
<br/>
open configuration_moses.py with your preferred IDE (spyder for example, as in the linked video) -> run the code (the green arrow top left in spyder) -> 

***please read CAREFULLY all the messages in the console (bottom right in spyder), you will be guided through the configuration***
<br/>
<br/>
<br/>

## Step 4: Final step is inserting grades: 
<br/>
1. for homework without an online part -> directy go to step 4.3
<br/>
<br/>
2. if there exists an online part of the homework: sing in into your ISIS account -> Go to the page of the math subject (Modul) you are tutoring -> go to the 
online homework -> Tabellendaten herunterladen als Komma separierte Werte (.csv) -> name the file as follows **HAweeknumber.csv (VERY IMPORTANT!)** -> example: 
HA7.csv for week 7, HA10.csv for week 10 -> put the file in the same directory as the other files   
<br/>
<br/>
3. open grades_moses.py with your preferred IDE (spyder for example, as in the linked video) -> run the code (the green arrow top left in spyder) -> * **please read CAREFULLY all the messages in the console (bottom right in spyder), you will be guided through the grading.**  
**check this link to see how to access the console of your browser: https://balsamiq.com/support/faqs/browserconsole/#apple-safari**

<br/>
<br/>
<br/>
If you wish to add, remove a student from a group or modify the email address -> run add_remove_moses.py and read the messages in the console.
