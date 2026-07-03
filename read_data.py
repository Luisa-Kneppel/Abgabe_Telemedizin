import json


def load_person_data(person_data_path="data/patienten_daten.json"):
    """Lädt die Patientendaten aus der JSON-Datei."""
    with open(person_data_path, "r", encoding="utf-8") as file:
        person_data = json.load(file)

    return person_data

def load_user_data(user_data_path="data/user.json"):
    """Lädt die Benutzerdaten aus der JSON-Datei."""
    with open(user_data_path, "r", encoding="utf-8") as file:
        user_data = json.load(file)

    return user_data

def get_person_list(person_data):
    """Gibt eine Liste aller Patientennamen im Format 'Nachname, Vorname' zurück."""
    list_of_names = []

    for eintrag in person_data:
        list_of_names.append(eintrag["nachname"] + ", " + eintrag["vorname"])

    return list_of_names

def find_person_data_by_name(suchstring):
    """
    Übergabe: 'Nachname, Vorname'
    Rückgabe: passende Person als Dictionary
    """
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
    patienten = load_person_data()

    for patient in patienten:
        # wir übergeben der Funktion eine Patienten_ID, hier wird der richtige Patient dann ausgewählt
        if patient["id"] == patient_id:
            patient["geburtsdatum"] = geburtsdatum
            patient["vorname"] = vorname
            patient["nachname"] = nachname

            if foto is not None: 
                bildpfad = f"data/pictures/patient_{patient_id}.png"
                with open(bildpfad, "wb") as file:      # wb = write binary, also das Bild besteht aus binärdaten
                    file.write(foto.getbuffer())    # das Bild wird aus dem Arbeitsspeicher geholt

                patient["foto"] = bildpfad

            patient["telefon"] = telefon
            patient["adresse"] = adresse
            patient["diagnosen"] = diagnosen
            patient["medikamente"] = medikamente

            break

        # die neuen Daten in die JSON Datei übernehmen:

    with open("data/patienten_daten.json", "w", encoding="utf-8")as file: 
        json.dump(patienten, file, indent=4, ensure_ascii=False)        # durch das ensure_ascii werden die Namen schön dargebstellt (Ü;Ö;Ä), durch intent = 4 wird das JSON übersichtlich dargestellt (nicht alles in einer Zeile)

def add_patient(geburtsdatum, vorname, nachname, foto, telefon, adresse):
    """diese Funktion fügt einen neuen Patienten zur JSON Datei hinzu"""
    patienten = load_person_data()
    neue_id = max(patient["id"] for patient in patienten) + 1   #dadurch bekommt der neu angelegte Patient die folgende ID

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

    with open(
        "data/patienten_daten.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            patienten,
            file,
            indent=4,
            ensure_ascii=False
        )

    return neue_id

def add_user(username, password, patienten_id):
    """fügt den neuen Benutzer zur user.json hinzu"""
    users = load_user_data()
    
    neuer_user = {
        "username": username,
        "password": password,
        "rolle":"patient",
        "patienten_id": patienten_id
    }
    users.append(neuer_user)

    with open(
        "data/user.json",
        "w",
        encoding = "utf-8")as file:
        json.dump(users, 
                  file,
                  indent = 4,
                  ensure_ascii = False)