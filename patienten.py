from PIL import Image

from read_data import load_person_data


def get_person_data():
    """
    Lädt alle Personen aus der JSON-Datei
    und wandelt sie in Person-Objekte um.
    """
    person_data = load_person_data()

    person_object_list = []

    for person_dict in person_data:
        person_object = Person(
            person_dict["id"],
            person_dict["geburtsdatum"],
            person_dict["vorname"],
            person_dict["nachname"],
            person_dict["foto"],
            person_dict["telefon"],
            person_dict["adresse"],
            person_dict["medikamente"],
            person_dict["diagnosen"]
        )

        person_object_list.append(person_object)

    return person_object_list


def get_person_object_by_full_name(full_name):
    """
    Übergabe: 'Nachname, Vorname'
    Rückgabe: passendes Person-Objekt
    """
    persons = get_person_data()

    firstname = full_name.split(", ")[1]
    lastname = full_name.split(", ")[0]

    for person in persons:
        if person.vorname == firstname and person.nachname == lastname:
            return person

    return None

class Person:

    def __init__(
        self,
        id: int,
        geburtsdatum: str,
        vorname: str,
        nachname: str,
        foto: str,
        telefon: str,
        adresse: dict,
        medikamente: list,
        diagnosen: list
    ):
        self.id = id
        self.geburtsdatum = geburtsdatum
        self.vorname = vorname
        self.nachname = nachname
        self.foto = foto
        self.telefon = telefon
        self.adresse = adresse
        self.medikamente = medikamente
        self.diagnosen = diagnosen

    def get_full_name(self):
        return self.nachname + ", " + self.vorname

    def get_image(self):
        image = Image.open(self.foto)
        return image

    def load_by_id(self, id):
        persons = get_person_data()

        for person in persons:
            if person.id == id:
                return person

        return None

    def calc_age(self):
        geburtsjahr = int(self.geburtsdatum.split("-")[0])
        age = 2026 - geburtsjahr
        return age

    def get_adresse_as_string(self):
        return (
            self.adresse["strasse"] + ", "
            + self.adresse["plz"] + " "
            + self.adresse["ort"]
        )

    def get_diagnosen_as_string(self):
        return ", ".join(self.diagnosen)

    def get_medikamente_as_string(self):
        medikamente_liste = []

        for medikament in self.medikamente:
            medikamente_liste.append(
                medikament["name"]
                + " "
                + medikament["dosis"]
                + " "
                + medikament["einnahme"]
            )

        return ", ".join(medikamente_liste)