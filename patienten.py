from PIL import Image
from read_data import load_person_data, get_person_list, update_patienten_daten
import streamlit as st


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


    
def show_patient(patient_id):
    """
    Zeigt die Informationen des Patienten an +  Möglichkeit gewisse Daten abzuändern.
    """
    if "bearbeiten" not in st.session_state:
        """
        hier wird der Bearbeitungsmodus angelegt, dadurch, dass Streamlit von 
        oben nach unten durchläuft, würde sich ansonsten das Formular nicht öffnen!
        """
        st.session_state.bearbeiten = False

    persons = get_person_data()
    patient = None

    for person in persons:
        if person.id == patient_id:
            patient = person
            break

    if patient is None:
        st.error("Patient wurde nicht gefunden.")
        return

    col1, col2 = st.columns(2)
    with col1:
        
        st.image(patient.foto, width = 150) 

    with col2:
        st.subheader("Persönliche Daten")
        st.write("Name: " + patient.get_full_name())
        st.write("Alter: " + str(patient.calc_age()))
        st.write("Telefon: " + patient.telefon)
        st.write("Adresse: " + patient.get_adresse_as_string())

        if not st.session_state.bearbeiten:
            """hier wird der Bearbeitungsbutton eingeführt"""

            if st.button("Persönliche Daten bearbeiten"):
                st.session_state.bearbeiten = True
                st.rerun()

        st.divider()    # damit es übersichtlich bleibt (Trennlinie)

        st.subheader("Medizinische Daten")  
        st.write("Diagnosen: " + patient.get_diagnosen_as_string())
        st.write("Medikamente: " + patient.get_medikamente_as_string())

    # Bearbeitungsformular

    if st.session_state.bearbeiten:
        st.subheader("Perönliche Daten bearbeiten:")
        
        geburtsdatum = st.text_input("Geburtsdatum",
                                     value =patient.geburtsdatum)
        vorname = st.text_input("Vorname",
                                value = patient.vorname)
        nachname = st.text_input("Nachname", 
                                 value = patient.nachname)
        foto = st.file_uploader("Neues Profilbild",
                                type = ["png"])         # weil wir alle Bilder in png hochgeladen haben, auf dieses Format begrenzen
        
        # Vorschau des neuen Bildes:
        if foto is not None:
            st.image(foto, width=180)

        telefon = st.text_input("Telefon",
                                value = patient.telefon)
        adresse = {
            "strasse": st.text_input("Straße", 
                                     value = patient.adresse["strasse"]),
            "plz": st.text_input("PLZ",
                                 value = patient.adresse["plz"]), 
            "ort": st.text_input("Ort",
                                 value = patient.adresse["ort"])}
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Speichern"):
                #st.write("Button wurde gedrückt")
                    
                update_patienten_daten(
                    patient.id,
                    geburtsdatum,
                    vorname,
                    nachname,
                    foto,
                    telefon,
                    adresse,
                    patient.diagnosen,
                    patient.medikamente)        # diagnosen und medikamente wurden hier zwar nicht abgeändert, sind aber trotzdem Parameter der Funktion!
                st.success("Änderungen wurden gespeichert.")
                st.session_state.bearbeiten = False
                #st.rerun()
        
        with col2:
            if st.button("Abbrechen"):
                st.session_state.bearbeiten = False
                st.rerun()



    
