import streamlit as st
#import plotly.express as px
#import numpy as np
#import pandas as pd
from arzt import anzeige_arzt
from patienten import show_patient, show_mitteilungen
from login import login
from read_data import load_user_data, get_mitteilungen

st.set_page_config(
    page_title="Patientenverwaltung",
    layout="wide")

with st.sidebar:
    st.image("data/pictures/Logo.png", width=150)

    if st.session_state.get("logged_in"):
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
    
        if st.session_state.get("rolle") == "patient":
        
            # Zustände anlegen, sollten sie noch nicht existieren
            if "patienten_ansicht" not in st.session_state:
                st.session_state.patienten_ansicht = "uebersicht"
            if "ausgewaehlte_mitteilung" not in st.session_state:
                st.session_state.ausgewaehlte_mitteilung = None 

            # Button hinzufügen
            username = st.session_state["username"]
            users = load_user_data()       
            patient = None

            for user in users:
                if (user["username"] == username):
                    patient = user["patienten_id"]
                    break

            anzahl = len(get_mitteilungen(patient))

            if st.button(f"Mitteilungen({anzahl})"):
                st.session_state.patienten_ansicht = "mitteilungen"
                st.rerun()

    for i in range(8):
        st.write("")

    st.markdown("""
    ### Praxis Frau Dr. Mustermann

    Maximilianstraße 2  
    6020 Innsbruck  

    ☎ 0721 123456  
    ✉ musterpraxis@innsbruck.at  

    **Entwicklung:**  
    Johanna Helfer  
    Luisa Kneppel
    """)

if "rolle" not in st.session_state:
    st.session_state.rolle = None

if st.session_state.rolle is None:

    left, center, right = st.columns([0.4, 6, 0.4])

    with center:
        st.write("")
        st.write("")

        with st.container(border=True):
            st.title("Willkommen in der Patientenverwaltung")

            st.write(
                "Diese Anwendung unterstützt die Verwaltung von Patientendaten und die Auswertung medizinischer Messwerte.")

            st.divider()

            st.subheader("Bitte wählen Sie Ihre Rolle")
            st.write("")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Ärzt:innenbereich**")

                if st.button("Als **Arzt** anmelden", use_container_width=True):
                    st.session_state.rolle = "arzt"
                    st.rerun()

            with col2:
                st.write("**Patient:innenbereich**")
                
                if st.button("Als **Patient:in** anmelden", use_container_width=True):
                    st.session_state.rolle = "patient"
                    st.rerun()

    st.stop()


login()

if not st.session_state.get("logged_in"):
    st.stop()

username = st.session_state["username"]

users = load_user_data()

current_user = None

for user in users:
    if (user["username"] == username
    and user["rolle"] == st.session_state.rolle):
        current_user = user
        break

if current_user["rolle"] == "arzt":
    anzeige_arzt()

elif st.session_state.patienten_ansicht == "uebersicht":
    show_patient(current_user["patienten_id"])

elif st.session_state.patienten_ansicht == "mitteilungen":
    show_mitteilungen(current_user["patienten_id"])