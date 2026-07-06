import streamlit as st
from PIL import Image
from read_data import load_person_data, update_patienten_daten
from read_data import add_datei
from datetime import datetime

class Person:
    '''Dient zur objektorientierten Darstellung einer Patient:in.
    Daten können einfacher in den weiteren Funktionen und Modulen über das 
    jeweilige Objekt aufgerufen werden.'''
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
        diagnosen: list):
        '''Initialisiert ein Person-Objekt mit allen gespeicherten Patientendaten.'''
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
        '''Gibt den vollständigen Namen im Format "Nachname, Vorname" zurück.'''
        return self.nachname + ", " + self.vorname

    def get_image(self):
        '''Lädt das Profilbild und gibt es zurück'''
        image = Image.open(self.foto)
        return image

    def load_by_id(self, id):
        '''Sucht anhand der Patienten-ID das passende Person-Objekt.'''
        persons = get_person_data()

        for person in persons:
            if person.id == id:
                return person

        return None

    def calc_age(self):
        '''Berechnet das Alter der Patient:in.'''
        geburtsjahr = int(self.geburtsdatum.split("-")[0])
        age = datetime.now().year - geburtsjahr
        return age

    def get_adresse_as_string(self):
        '''Gibt die vollständige Adresse zurück'''
        return (
            self.adresse["strasse"] + ", "
            + self.adresse["plz"] + " "
            + self.adresse["ort"])

    def get_diagnosen_as_string(self):
        '''Fasst alle Diagnosen zu einem String zusammen'''
        return ", ".join(self.diagnosen)

    def get_medikamente_as_string(self):
        '''Fasst Name, Dosierung und Einnahme aller Medikamente 
        zu einem String zusammen.'''
        medikamente_liste = []

        for medikament in self.medikamente:
            medikamente_liste.append(
                medikament["name"]
                + " "
                + medikament["dosis"]
                + " "
                + medikament["einnahme"])

        return ", ".join(medikamente_liste)

def get_person_data():
    '''Lädt alle Personen aus der JSON-Datei
    und wandelt sie in Person-Objekte um.'''
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
    '''Der vollständige Name wird übergeben und das passende Person-Objekt
    wird zurückgegeben'''
    persons = get_person_data()

    firstname = full_name.split(", ")[1]
    lastname = full_name.split(", ")[0]

    for person in persons:
        if person.vorname == firstname and person.nachname == lastname:
            return person

    return None
    
def show_patient(patient_id):
    '''Erstellt das Patientendashboard, zeigt die Informationen der 
    Patient:in an und ermöglicht es gewisse Daten abzuändern.'''
    if "bearbeiten" not in st.session_state:
        # hier wird der Bearbeitungsmodus angelegt, dadurch, dass Streamlit von 
        # oben nach unten durchläuft, würde sich ansonsten das Formular direkt wieder schließen!
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

    st.title("Mein Patientenbereich")

    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            st.image(patient.foto, width=180)

        with col2:
            st.subheader("Willkommen, " + patient.vorname)

            st.write("**Name:** " + patient.get_full_name())
            st.write("**Alter:** " + str(patient.calc_age()) + " Jahre")
            st.write("**Telefon:** " + patient.telefon)
            st.write("**Adresse:** " + patient.get_adresse_as_string())

        with col3:
            st.subheader("Medizinische Übersicht")

            st.write("**Diagnosen:**")
            st.info(patient.get_diagnosen_as_string())

            st.write("**Medikamente:**")
            st.success(patient.get_medikamente_as_string())

    if not st.session_state.bearbeiten:
        if st.button("Persönliche Daten bearbeiten"):   # Bearbeitungsmodus muss auf True gesetzt werden, damit das Bearbeitungsformular angezeigt wird
            st.session_state.bearbeiten = True
            st.rerun()

    # Bearbeitungsformular
    if st.session_state.bearbeiten:
        with st.container(border=True):
            st.subheader("Persönliche Daten bearbeiten")
            st.caption("Hier können Sie Ihre gespeicherten Kontaktdaten und Ihr Profilbild aktualisieren.")

            with st.form("patient_daten_bearbeiten"): #eingabefelder sind zu einem Formular zusammen gefasst
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Kontaktdaten")

                    geburtsdatum = st.text_input(
                        "Geburtsdatum", value=patient.geburtsdatum)

                    vorname = st.text_input(
                        "Vorname", value=patient.vorname)

                    nachname = st.text_input(
                        "Nachname", value=patient.nachname)

                    telefon = st.text_input(
                        "Telefon", value=patient.telefon)

                with col2:
                    st.subheader("Adresse und Profilbild")

                    strasse = st.text_input(
                        "Straße", value=patient.adresse["strasse"])
                
                    plz = st.text_input(
                        "PLZ", value=patient.adresse["plz"])
            
                    ort = st.text_input(
                        "Ort", value=patient.adresse["ort"])
        
                    foto = st.file_uploader(
                        "Neues Profilbild", type=["png"])
                    
                    if foto is not None:
                        st.image(foto, width=160)

                st.divider()

                col_speichern, col_abbrechen = st.columns(2)

                with col_speichern:
                    speichern = st.form_submit_button("Speichern", use_container_width=True)

                with col_abbrechen:
                    abbrechen = st.form_submit_button("Abbrechen", use_container_width=True)

                if speichern:
                    adresse = {
                        "strasse": strasse,
                        "plz": plz,
                        "ort": ort}

                    update_patienten_daten(
                        patient.id,
                        geburtsdatum,
                        vorname,
                        nachname,
                        foto,
                        telefon,
                        adresse,
                        patient.diagnosen, #diagnosen und medikamente wurden hier zwar nicht abgeändert, sind aber trotzdem Parameter der Funktion
                        patient.medikamente)

                    st.success("Änderungen wurden gespeichert.")
                    st.session_state.bearbeiten = False     # Bearbeitungsmodus wird beendet, damit das Formular geschlossen wird.

                if abbrechen:
                    st.session_state.bearbeiten = False
                    st.rerun()

    st.divider()
    st.subheader("Dateien hochladen")

    datei = st.file_uploader(
        "CSV-Datei auswählen",
        type = ["csv"])
    if datei is not None:
        if st.button("Datei hochladen"):
            add_datei(patient.id, datei)
            st.success("Datei erfolgreich hochgeladen.")