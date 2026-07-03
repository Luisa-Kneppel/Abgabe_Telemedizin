# hier werden alle Funktionen, die den Login betreffen, geschrieben und erst nachher im main.py implementiert.

import streamlit as st
from read_data import load_user_data
from streamlit_authenticator.utilities.hasher import Hasher

def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "ansicht" not in st.session_state:
        st.session_state.ansicht = "login"

    if st.session_state.logged_in:
        return

    if st.session_state.ansicht == "login":
        login_formular()
    elif st.session_state == "registrieren":
        registrieren()

    
def login_formular():
    st.title("Patientenverwaltung")
    st.subheader("Login")

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

    st.divider()
    
    if st.button("Neu registrieren"):
        st.session_state.ansicht = "registrieren"
        st.rerun()

def registrieren():
    st.title("Patientenverwaltung")
    st.subheader("Registrierung")
    
    if st.button("Zurück"):
        st.session_state.ansicht = "login"
        st.rerun
