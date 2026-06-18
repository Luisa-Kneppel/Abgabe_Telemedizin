import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

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

st.title("Patientenverwaltung")

st.write("Bitte wählen Sie Ihre Rolle:")

col1, col2 = st.columns(2)

with col1:
    if st.button("Arzt", use_container_width=True):
        st.session_state["rolle"] = "arzt"
        st.switch_page("pages/arzt.py")

with col2:
    if st.button("Patient", use_container_width=True):
        st.session_state["rolle"] = "patient"
        st.switch_page("pages/patient.py")