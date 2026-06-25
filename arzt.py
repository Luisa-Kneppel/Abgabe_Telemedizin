from read_data import load_person_data, get_person_list
from patienten import get_person_object_by_full_name
import streamlit as st




def anzeige():

    patienten_data = load_person_data()
    person_names = get_person_list(patienten_data)

    selected_person = st.selectbox("Patient:in auswählen", person_names)

    patient = get_person_object_by_full_name(selected_person)
    
    col1, col2 = st.columns(2)
    with col1:

        st.image(patient.foto) #, width=120)

    with col2:
        st.write("Name: " + patient.get_full_name())
        st.write("Alter: " + str(patient.calc_age()))
        st.write("Telefon: " + patient.telefon)
        st.write("Adresse: " + patient.get_adresse_as_string())
        st.write("Diagnosen: " + patient.get_diagnosen_as_string())
        st.write("Medikamente: " + patient.get_medikamente_as_string())

