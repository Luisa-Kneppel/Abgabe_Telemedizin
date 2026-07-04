# hier werden alle Funktionen, die den Login betreffen, geschrieben und erst nachher im main.py implementiert.

import streamlit as st
from read_data import load_user_data, add_patient, add_user
from streamlit_authenticator.utilities.hasher import Hasher
from datetime import date 

def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "ansicht" not in st.session_state:
        st.session_state.ansicht = "login"

    if st.session_state.logged_in:
        return

    if st.session_state.ansicht == "login":
        login_formular()
    elif st.session_state.ansicht == "registrieren":
        registrieren()

def login_formular():
    st.title("Patientenverwaltung")
    if st.session_state.rolle == "arzt":
        st.subheader("Login - Arzt")
    elif st.session_state.rolle == "patient":
        st.subheader("Login - Patienten")
    
    # damit die Mitteilung "Registrierung erfolgreich" angezeigt wird,
    # ohne dem hier würde die Seite direkt neu laden und die Nachricht würde direkt verschwinden
    if st.session_state.get("registrierung_erfolgreich"):
        st.toast("Registrierung erfolgreich!")
        del st.session_state["registrierung_erfolgreich"]

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    if st.button("Login"):

        users = load_user_data()

        for user in users:
            # zuerst prüfen ob Benutzer im richtigen Login ist (Arzt oder Patient)
            if (
                user["username"] == username
                and user["rolle"] == st.session_state.rolle
            ):
            # im nächsten Schritt wird das gehashte Passwort überprüft
                if Hasher.check_pw(password, user["password"]):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.rerun()

        st.error("Benutzername oder Passwort falsch.")      # für den Fall, dass Benutzernamen oder Passwort nicht mit den erwarteten Werten übereinstimmt

    if st.session_state.rolle == "patient":
        # damit das neu registrieren nur im Patientendashboard erscheint. Ohne dem würde es auch im Ärztedashboard angezeigt werden

        st.divider()

        if st.button("Neu registrieren"):
            st.session_state.ansicht = "registrieren"
            st.rerun()
    if st.button("Zurück zur Startseite"):
        st.session_state.rolle = None
        st.session_state.ansicht = "login"
        st.rerun()

def registrieren():
    st.title("Patientenverwaltung")
    st.subheader("Registrierung")

    st.write ("### Persönliche Daten")

    vorname = st.text_input("Vorname")
    nachname = st.text_input("Nachname")

    geburtsdatum = st.date_input(
    "Geburtsdatum",
    value= None,
    min_value=date(1900, 1, 1),
    max_value=date.today()
    )

    telefon = st.text_input("Telefon")
    foto = st.file_uploader("Profilbild", type = ["png"])

    if foto is not None:
        st.image(foto, width = 180)
    
    adresse = {
        "strasse": st.text_input("Straße"),
        "plz": st.text_input("PLZ"),
        "ort": st.text_input("Ort")}

    st.divider()
    st.write("### Zugangsdaten")

    username = st.text_input("Benutzername")

    password = st.text_input(
        "Passwort",
        type="password")

    password2 = st.text_input(
        "Passwort bestätigen",
        type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Registrieren"):
            # damit die Registrierung gespeichert wird, werden hier alle Daten geprüft:
            # die nächste if Bedingung stellt sicher, dass die Daten vollständig sind:
            if (
                vorname == ""
                or nachname == ""
                or geburtsdatum == None
                or telefon == ""
                or adresse["strasse"] == ""
                or adresse["plz"] == ""
                or adresse["ort"] == ""
                or username == ""
                or password == ""
                or password2 == ""):
                st.error("Bitte füllen Sie alle Felder aus.")
                return
            # hier wird geprüft ob ein Profilbild hochgeladen wurde (ist Pflicht)
            if foto is None:
                st.error("Bitte laden Sie ein Profilbild hoch.")
                return
            # die zwei eingegebenden Passwörter werden verglichen. Bei nicht Übereinstimmung wird eine Fehlermeldung ausgegeben
            if password != password2:
                st.error("Die Passwörter stimmen nicht überein.")
                return
            
            # jezt wird geprüft, ob der Benutzer bereits angelegt ist (gesucht wird mitteln Benutzernamen)
            users = load_user_data()

            for user in users:
                if user["username"] == username:
                    st.error("Benutzername ist bereits vergeben.")
                    return
            
            # hier wird das Passwort gehasht:
            hashed_password = Hasher.hash(password)
            # das Datum in einen String umwandeln:
            geburtsdatum = geburtsdatum.strftime("%Y-%m-%d")
            # neuen Benutzer anlegen bzw. speichern:
            patient_id = add_patient(
                    geburtsdatum,
                    vorname,
                    nachname,
                    foto,
                    telefon,
                    adresse)
            add_user(
                username,
                hashed_password,
                patient_id) 
            st.session_state.registrierung_erfolgreich = True
            st.session_state.ansicht = "login"
            st.rerun()

    with col2:
        if st.button("Zurück"):
            st.session_state.ansicht = "login"
            st.rerun()

