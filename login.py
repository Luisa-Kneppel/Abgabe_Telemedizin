# hier werden alle Funktionen, die den Login und die Registrierung betreffen, geschrieben und erst nachher im main.py implementiert.

import streamlit as st
from read_data import load_user_data, add_patient, add_user
from streamlit_authenticator.utilities.hasher import Hasher
from datetime import date 

def login():
    '''Steuert die Anzeige der Login- und Registrierungsansicht.'''

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
    '''Erzeugt die Login-Ansicht. Je nach gewählter Rolle wird
    der Patienten- oder der Ärzte-Login angezeigt.'''

    st.title("Patientenverwaltung")
    if st.session_state.rolle == "arzt":
        st.subheader("Login - Arzt")
    elif st.session_state.rolle == "patient":
        st.subheader("Login - Patienten")
    
    # Ohne den Session State würde die Seite direkt neu laden 
    # und die Nachricht würde sofort verschwinden
    if st.session_state.get("registrierung_erfolgreich"):
        st.toast("Registrierung erfolgreich!")
        del st.session_state["registrierung_erfolgreich"]

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    if st.button("Login"):

        users = load_user_data()

        for user in users:
            # Zuerst wird geprüft, ob der Benutzer zur gewählten Rolle gehört.
            if (
                user["username"] == username
                and user["rolle"] == st.session_state.rolle
            ):
            # Im nächsten Schritt wird das gehashte Passwort überprüft
                if Hasher.check_pw(password, user["password"]):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.rerun()

        st.error("Benutzername oder Passwort falsch.")      # Für den Fall, dass Benutzernamen oder Passwort nicht mit den erwarteten Werten übereinstimmt

    if st.session_state.rolle == "patient":
        # Damit das Registrieren nur im Patientendashboard erscheint. Im Ärztedashboard soll es nicht angezeigt werden.

        st.divider()
        neuer_benutzer, zurück, platzhalter = st.columns([2,2,8])
        with neuer_benutzer:
            if st.button("Neu registrieren"):
                st.session_state.ansicht = "registrieren"
                st.rerun()
        with zurück:
            if st.button("Zurück zur Startseite"):
                st.session_state.rolle = None
                st.session_state.ansicht = "login"
                st.rerun()

    if st.session_state.rolle == "arzt":
        st.divider()
        if st.button("Zurück zur Startseite"):
            st.session_state.rolle = None
            st.session_state.ansicht = "login"
            st.rerun()

def registrieren():
    '''Ermöglicht neuen Patient:innen die eigenständige Registrierung.
    Nach erfolgreicher Registrierung werden die Patientendaten gespeichert
    und zur Login-Ansicht zurückgekehrt.'''

    st.title("Patientenverwaltung")
    st.subheader("Registrierung")

    st.write ("### Persönliche Daten")

    vorname = st.text_input("Vorname")
    nachname = st.text_input("Nachname")

    geburtsdatum = st.date_input(
    "Geburtsdatum",
    value= None,
    min_value=date(1900, 1, 1),
    max_value=date.today())

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

    Registrieren, zurück, platzhalter = st.columns([2,2,10])

    with zurück:
        if st.button("Zurück"):
            st.session_state.ansicht = "login"
            st.rerun()
    with Registrieren:
        if st.button("Registrieren"):
            # Vor dem Speichern werden alle Eingaben geprüft.
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
            # Es wird geprüft, ob ein Profilbild hochgeladen wurde (Pflichtfeld).
            if foto is None:
                st.error("Bitte laden Sie ein Profilbild hoch.")
                return
            # Die beiden eingegebenen Passwörter werden verglichen. 
            # Bei Nichtübereinstimmung wird eine Fehlermeldung ausgegeben.
            if password != password2:
                st.error("Die Passwörter stimmen nicht überein.")
                return
            
            # Es wird geprüft, ob der Benutzername bereits vergeben ist.
            users = load_user_data()

            for user in users:
                if user["username"] == username:
                    st.error("Benutzername ist bereits vergeben.")
                    return
            
            # Hier wird das Passwort gehasht:
            hashed_password = Hasher.hash(password)
            # Das Datum in einen String umwandeln:
            geburtsdatum = geburtsdatum.strftime("%Y-%m-%d")
            # Neuen Patienten und den dazugehörigen Benutzer speichern.
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



