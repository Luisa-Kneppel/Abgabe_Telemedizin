import json


def load_person_data(person_data_path="data/patienten_daten.json"):
    """Lädt die Patientendaten aus der JSON-Datei."""
    with open(person_data_path, "r", encoding="utf-8") as file:
        person_data = json.load(file)

    return person_data


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