Zu Beginn haben wir uns einen Patienten Datensatz erstellt mit allen nötigen Informationen, zudem haben wir csv Dateien erstellt mit fiktiven Messwerten. Diese csv Dateien werden in einer json Datei zusammengefasst. 
Nach dem Erstellen der Daten haben wir das erste Nebenmodul read_data.py erstellt, indem wir verschiedene Funktionen zum Einlesen der json Dateien geschrieben haben. 
Im ersten Schritt haben wir die json Datei importiert.
Funktionen:
-	Load_person_data:  lädt die Patientendaten aus der json Datien und gibt die Personen Daten als Liste zurück (person_data)
-	Get_person_list: der Funktion wird, die soeben erstelle Liste übergeben und gibt wiederrum eine Liste mit Personennamen zurück (list_of_names). Dabei werden die Personen mit Nachnamen und Vorname gespeichert.
-	Find_person_data_by_name: der Funktion wird „Nachname“ und „Vorname“ übergeben. Es wird geprüft ob die Eingabewerte mit den Daten übereinstimmen 
-> Die passende Person wird als Dictionary zurückgegeben

Nebenmodul arzt.py:
In diesem Modul wird das Ärzte Dashboard erstellt, sodass es später im main.py nur mehr aufgerufen werden muss.
Zuerst werden die Funktionen load_person_data, get_person_list aus read_data; get_person_object_by_full_name aus patienten.py und streamlit importiert.
Daraufhin haben wir die Funktion anzeige_arzt() erstellt, durch diese Funktion kann nahcher das Ärzte Dashboard aufgerufen werden. 
Im ersten Schritt laden wir die Patientendaten sowie die Liste der Personennamen ein.
Durch ein Dropdown können die verschiedenen Patienten ausgewählt werden, je nach Auswahl werden die jeweiligen Daten angezeigt. Um es übersichtlicher zu gestalten, haben wir uns dazu entschlossen, mit zwei Spalten zu arbeiten, in der einen Spalte wird das Patientenfoto, in der anderen die Patientendaten angezeigt.

Nebenmodul patienten.py:
Zuerst haben wir die nötigen Pakete und Funktionen importiert (Image, streamlit, load_person_data und get_person_list).
Im nächsten Schritt haben wir die Klasse Person erstellt:
-	Konstruktor
-	Methoden: 
o	Get_full_name
o	Get_image
o	Load_by_id
o	Calc_age
o	Get_adresse_as_string
o	Get_diagnosen_as_string
o	Get_medikamente_as_string
Weitere Funktionen:
-	Get_person_data: läd alle Personen aus der JSON Datei und wandelt sie in Person-Objekte um (zurückgegeben wird eine Liste mit Personen-Objekten)
-	Get_person_objekt_by_full_name: der Funktion wir Nachname und Vorname übergeben (also full_name), bei Übereinstimmung wir das passende Person_Objekt zurückgegeben. 
-	Show_patient: hier wird das Patienten Dashboard erstellt, mit dieser Funktion wird im main.py die Ansicht aufgerufen. Zuerst werden die Patientendaten aufgerufen, durch ein Dropdown können die (DAS STIMMT NOCH NICHT)
Auch hier haben wir uns für eine Darstellung mittels zwei Spalten entschieden. 

Main.py
Anfangs werden alle nötigen Pakete und Funktionen importiert. Daraufhin haben wir das Layout des Dashboards festgelegt (damit es auf einem Laptop übersichtlich erscheint haben wir uns für das Layout „wide“ entschieden) 
1.	Startseite: die Startseite besteht aus einer Sidebar, wo die allgemeinen Infomationen und eventuelle Kontaktdaten der Praxis erscheinen, und eines Loginfeldes, mit der Auswahlmöglichkeit zwischen Arzt und Patient. 
2.	Je nach Rolle wird das jeweilige Dashboard aufgerufen (vorerst Anmeldung mit Benutzername und Kennwort).
Damit die Anmeldung nicht in jeder Ansicht angezeigt wird, haben wir eine if Bedingung eingeführt, somit wird das Anmeldefeld nur angezeigt, solange noch keine Rolle ausgewählt wurde. 

