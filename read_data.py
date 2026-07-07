import json
from datetime import datetime #damit wir das aktuelle Datum für die CSV Datei bekommen
from pathlib import Path #damit wir neue Ordner gut erstellen können


def load_person_data(person_data_path="data/patienten_daten.json"):
    '''Lädt die Patientendaten aus der JSON-Datei.'''
    with open(person_data_path, "r", encoding="utf-8") as file:
        person_data = json.load(file)

    return person_data

def load_user_data(user_data_path="data/user.json"):
    '''Lädt die Benutzerdaten aus der JSON-Datei.'''
    with open(user_data_path, "r", encoding="utf-8") as file:
        user_data = json.load(file)

    return user_data

def get_person_list(person_data):
    '''Gibt eine Liste aller Patientennamen im Format 'Nachname, Vorname' zurück.'''
    list_of_names = []

    for eintrag in person_data:
        list_of_names.append(eintrag["nachname"] + ", " + eintrag["vorname"])

    return list_of_names

def find_person_data_by_name(suchstring):
    '''Übergibt einen Namen im Format "Nachname, Vorname" und gibt die passende Person als Dictionary zurück.'''
    person_data = load_person_data()

    if suchstring == "None":
        return {}

    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    for eintrag in person_data:
        if eintrag["nachname"] == nachname and eintrag["vorname"] == vorname:
            return eintrag

    return {}

def update_patienten_daten(patient_id, geburtsdatum, vorname, nachname, foto, telefon, adresse, diagnosen, medikamente):
    '''Aktualisiert die Patientendaten anhand der Patienten-ID.'''
    patienten = load_person_data()

    for patient in patienten:
        # Anhand der übergebenen Patienten-ID wird der richtige Patient ausgewählt.
        if patient["id"] == patient_id:
            patient["geburtsdatum"] = geburtsdatum
            patient["vorname"] = vorname
            patient["nachname"] = nachname

            if foto is not None: 
                bildpfad = f"data/pictures/patient_{patient_id}.png"
                with open(bildpfad, "wb") as file:      # wb = write binary, also das Bild besteht aus binärdaten
                    file.write(foto.getbuffer())    # Das hochgeladene Bild wird aus dem Arbeitsspeicher gelesen.

                patient["foto"] = bildpfad

            patient["telefon"] = telefon
            patient["adresse"] = adresse
            patient["diagnosen"] = diagnosen
            patient["medikamente"] = medikamente

            break

    # Die aktualisierten Daten werden in der JSON-Datei gespeichert:
    with open("data/patienten_daten.json", "w", encoding="utf-8")as file: 
        json.dump(patienten, file, indent=4, ensure_ascii=False)        # ensure_ascii sorgt dafür, dass Umlaute dargestellt werden, durch indent = 4 wird das JSON übersichtlich dargestellt (nicht alles in einer Zeile)

def update_medizinische_daten(patient_id, diagnosen, medikamente):
    """ Aktualisiert Diagnosen und Medikamente """

    patienten = load_person_data()

    for patient in patienten:
        if patient["id"] == patient_id:
            patient["diagnosen"] = diagnosen
            patient["medikamente"] = medikamente
            break

    with open("data/patienten_daten.json", "w", encoding="utf-8") as file:
        json.dump(patienten, file, indent=4, ensure_ascii=False)

def add_patient(geburtsdatum, vorname, nachname, foto, telefon, adresse):
    '''Fügt einen neuen Patienten zur JSON-Datei hinzu'''
    patienten = load_person_data()
    neue_id = max(patient["id"] for patient in patienten) + 1   # Der neu angelegte Patient erhält automatisch die nächste freie ID.

    # Profilbild speichern
    bildpfad = f"data/pictures/patient_{neue_id}.png"
    with open(bildpfad, "wb") as file:
        file.write(foto.getbuffer())    # dadurch wird das Bild dauerhaft und nicht nur im Arbeitsspeicher gespeichert.

    neuer_patient = {
        "id": neue_id,
        "nachname": nachname,
        "vorname": vorname,
        "foto": bildpfad,
        "geburtsdatum": geburtsdatum,
        "telefon": telefon,
        "adresse": adresse,
        "medikamente": [],  # dürfen nur vom Arzt verschrieben werden
        "diagnosen": []     # auch hier Aufgabe vom Arzt
    }
    patienten.append(neuer_patient)    

    with open("data/patienten_daten.json", "w", encoding="utf-8") as file:
        json.dump(patienten, file, indent=4, ensure_ascii=False)

    return neue_id

def add_user(username, password, patienten_id):
    '''Fügt den neuen Benutzer zur user.json hinzu'''
    users = load_user_data()
    
    neuer_user = {
        "username": username,
        "password": password,
        "rolle":"patient",
        "patienten_id": patienten_id
    }
    users.append(neuer_user)

    with open("data/user.json", "w", encoding = "utf-8")as file:
        json.dump(users, file, indent = 4, ensure_ascii = False)
        
def add_datei(patient_id, csv_datei):
    '''Speichert die hochgeladene CSV-Datei und ergänzt die Messungsdatenbank.'''

    # Bisherige Messungen aus der JSON-Datei laden
    with open("data/messungen_datenbank.json", "r", encoding="utf-8") as file:
        messungen = json.load(file)

    datum = datetime.now().strftime("%Y-%m-%d")

    ordner = Path(f"data/temperatur_messdaten/patient_{patient_id}")
    
    ordner.mkdir(parents=True, exist_ok=True) # Ordner wird bei Bedarf automatisch erstellt
    # parents=True sorgt hier dafür, dass auch alle übergeordneten Ordner erstellt werden,falls nicht da
    # exist_ok=True kein Fehler wenn ordner schon da

    dateiname = f"patient_{patient_id}_{datum}.csv" 

    dateipfad_speichern = ordner / dateiname # Dateipfad wird hier erstellt

    with open(dateipfad_speichern, "wb") as file:   # CSV dauerhaft speichern
        file.write(csv_datei.getbuffer())

    messungen.append({  # Neue Messung zur Messungsdatenbank hinzufügen
        "patient_id": patient_id,
        "typ": "koerpertemperatur",
        "datum": datum,

        # Pfad ohne "data/", weil beim Laden später "data/" davor gesetzt wird
        "dateipfad": f"temperatur_messdaten/patient_{patient_id}/{dateiname}"
    })

    # Aktualisierte Messungsdatenbank wieder speichern
    with open("data/messungen_datenbank.json", "w", encoding="utf-8") as file:
        json.dump(messungen, file, indent=4, ensure_ascii=False)
        
def load_mitteilungen():
    '''Lädt alle Mitteilungen.'''
    with open("data/mitteilungen.json", "r", encoding="utf-8") as file:
        return json.load(file)
    
def add_mitteilung(patient_id, titel, text):
    '''Speichert eine neue Mitteilung für eine Patient:in.'''
    mitteilungen = load_mitteilungen()
    mitteilungen.append({
        "patienten_id" : patient_id,
        "datum" : datetime.now().strftime("%Y-%m-%d"),
        "titel" : titel,
        "text" : text,
        "gelesen" : False})
    
    with open("data/mitteilungen.json", "w", encoding="utf-8") as file:
        json.dump(mitteilungen, file, indent=4, ensure_ascii=False)
    
def get_mitteilungen(patienten_id):
    '''Gibt die Mitteilungen einer Patient:in zurück.'''
    mitteilungen = load_mitteilungen()
    patient_mitteilungen = []       # Leere Liste erstellen, darin werden später die Mitteilungen abgelegt.

    for mitteilung in mitteilungen:
        if mitteilung["patienten_id"] == patienten_id:
            patient_mitteilungen.append(mitteilung)
    return patient_mitteilungen