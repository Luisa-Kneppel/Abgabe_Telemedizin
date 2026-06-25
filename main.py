import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from read_data import load_person_data, get_person_list
from patienten import get_person_object_by_full_name
from arzt import anzeige


#st.write("# ")
#st.header("Login")

st.set_page_config(
    page_title="Patientenverwaltung",
    layout="wide"
    )

with st.sidebar:
    st.image("data/pictures/Logo.png", width=150)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.markdown("""
    ### Musterpraxis

    Hauptstraße 15
    76131 Karlsruhe

    ☎ 0721 123456
    """)

if "rolle" not in st.session_state:
    st.session_state.rolle = None

# damit die Auswahlmöglichkeiten nicht immer aufscheinen müssen wir eine 
# if Bedingung einführen, damit es nur aufscheint, wenn noch nichts gewählt wurde!

if st.session_state.rolle is None: 

    st.title("Patientenverwaltung")
    st.write("Bitte wählen Sie Ihre Rolle:")
    st.write(" ")   # Abstand

    left_space, col1, col2, right_space = st.columns([1.5, 2, 2, 1.5])  # damit die Seitenaufteilung besser ist, die beiden Äußeren bleiben leer.




    with col1:
        if st.button("Arzt", use_container_width=True):
            st.session_state["rolle"] = "arzt"

    with col2:
        if st.button("Patient", use_container_width=True):
            st.session_state["rolle"] = "patient"
else:
    if st.session_state.rolle == "arzt":
        anzeige()
    
    elif st.session_state.rolle == "patient":
        #show_patient()
        pass
