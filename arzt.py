import json
import pandas as pd
import plotly.express as px 
import streamlit as st
import plotly.graph_objects as go
from read_data import load_person_data, get_person_list, update_medizinische_daten, add_mitteilung, load_mitteilungen
from patienten import get_person_object_by_full_name

TEMP_GRENZWERT=38.0 #zentraler Grenzwert für die Temperaturmessungen

def show_patientenansicht_arzt():
    ''' hier werden die Patientendaten geladen und die Patienten ausgewählt, deren Daten angezeigt werden sollen zudem 
    ist die Funktion für die Bearbeitung der medizinischen Daten umgesetzt'''

    if "medizin_bearbeiten" not in st.session_state:
        st.session_state["medizin_bearbeiten"] = False
    if "mitteilung_schreiben" not in st.session_state:
        st.session_state.mitteilung_schreiben = False

    patienten_data = load_person_data()
    person_names = get_person_list(patienten_data)

    st.subheader("Patientendaten")
    selected_person = st.selectbox("Patient:in auswählen", person_names)

    patient = get_person_object_by_full_name(selected_person)

    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            st.image(patient.foto, width=150)
            st.divider()

            if st.button("Kontaktieren"):
                st.session_state.mitteilung_schreiben = True
                st.rerun()

        with col2:
            st.subheader(patient.get_full_name())

            st.write("**Alter:** " + str(patient.calc_age()) + " Jahre")
            st.write("**Telefon:** " + patient.telefon)
            st.write("**Adresse:** " + patient.get_adresse_as_string())

        with col3:
            st.write("**Diagnosen:**")

            for diagnose in patient.diagnosen:
                st.write(diagnose)

            st.write("**Medikamente:**")

            if len(patient.medikamente) == 0:
                st.info("Keine Medikamente eingetragen.")
            else:
                medikamente_tabelle = []

                for medikament in patient.medikamente:
                    medikamente_tabelle.append({
                        "Name": medikament["name"],
                        "Dosis": medikament["dosis"],
                        "Einnahme": medikament["einnahme"]
                    })

                st.dataframe(
                    medikamente_tabelle,
                    hide_index=True,
                    width="stretch"
                )

            if not st.session_state["medizin_bearbeiten"]: #Button zum bearbeiten der medizinischen Daten
                if st.button("Medizinische Daten bearbeiten"):
                    st.session_state["medizin_bearbeiten"] = True
                    st.rerun()
    
    if st.session_state.mitteilung_schreiben:
        with st.container(border=True):
            st.subheader("Mitteilung schreiben")
            titel = st.text_input("Titel")
            text = st.text_area("Nachricht")
            senden, abbrechen = st.columns(2)
            with senden:
                if st.button("Senden"):
                    add_mitteilung(patient.id,
                                   titel,
                                   text)
                    st.success("Mitteilung wurde gesendet.")
                    st.session_state.mitteilung_schreiben = False
                    st.rerun()
        with abbrechen:
            if st.button("Abbrechen"):
                st.session_state.mitteilung_schreiben = False
                st.rerun()

    if st.session_state["medizin_bearbeiten"]:
        with st.container(border=True):
            st.subheader("Medizinische Daten bearbeiten")

            diagnosen_text = st.text_area(
                "Diagnosen",
                value=", ".join(patient.diagnosen),
                help="Mehrere Diagnosen bitte mit Komma trennen."
            )

            medikamente_tabelle = []

            for medikament in patient.medikamente:
                medikamente_tabelle.append({
                    "Name": medikament["name"],
                    "Dosis": medikament["dosis"],
                    "Einnahme": medikament["einnahme"]
                })

            if len(medikamente_tabelle) == 0: #leere Tabelle/ df erstellen, wenn keine Medikamente vorhanden sind
                df_medikamente = pd.DataFrame(columns=["Name", "Dosis", "Einnahme"])
            else:
                df_medikamente = pd.DataFrame(medikamente_tabelle)

            medikamente_bearbeitet = st.data_editor(
                df_medikamente,
                num_rows="dynamic",
                hide_index=True,
                width="stretch"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Medizinische Daten speichern"):
                    neue_diagnosen = []

                    for diagnose in diagnosen_text.split(","):
                        diagnose = diagnose.strip()

                        if diagnose != "":
                            neue_diagnosen.append(diagnose)

                    neue_medikamente = []

                    for medikament in medikamente_bearbeitet.to_dict("records"):
                        name = str(medikament["Name"]).strip()
                        dosis = str(medikament["Dosis"]).strip()
                        einnahme = str(medikament["Einnahme"]).strip()

                        if name != "":
                            neue_medikamente.append({
                                "name": name,
                                "dosis": dosis,
                                "einnahme": einnahme
                            })

                    update_medizinische_daten(
                        patient.id,
                        neue_diagnosen,
                        neue_medikamente
                    )

                    st.success("Medizinische Daten wurden gespeichert.")
                    st.session_state["medizin_bearbeiten"] = False
                    st.rerun()

            with col2:
                if st.button("Abbrechen"):
                    st.session_state["medizin_bearbeiten"] = False
                    st.rerun()

    st.divider() #horizontale Trennlinie 

    show_temp_auswertung(patient.id)
#Daten laden
def load_temp_messdaten ():
    ''' wir lesen die Daten aus der json Datei ein (diese hat Zugriff auf die csv)'''
    with open("data/messungen_datenbank.json", "r", encoding="utf-8") as file:
        temp_messdaten = json.load(file)

    return temp_messdaten

def get_temp_messdaten_by_id(patienten_id):
    ''' hier suchen wir alle Temp Messdaten, die zu einer bestimmten ID gehören'''
    temp_messdaten = load_temp_messdaten()

    temp_liste = []

    for messung in temp_messdaten:
        if messung["patient_id"] == patienten_id and messung["typ"] == "koerpertemperatur":
            temp_liste.append(messung)

    return temp_liste 

def load_temp_csv(dateipfad):
    ''' lädt die einzelnen csv dateien, teilt ordner ab nur noch Pfad'''
    full_path = "data/" + dateipfad
    df_temp = pd.read_csv(full_path) #hier df mit den Daten anlegen

    return df_temp

#Start der Berechnungen
def temp_summary(temp_liste):
    ''' wir brauchen für den Trend die wichitgsten Daten der einzelnen Tage
    diese Daten erstellen wir hier aus der temp_liste um es später zu plotten'''

    summary_liste = []

    for messung in temp_liste:
        df_temp = load_temp_csv(messung["dateipfad"])

        durchschnitt = df_temp["temperatur"].mean()
        minimum = df_temp["temperatur"].min()
        maximum = df_temp["temperatur"].max()

        summary_liste.append({
            "Datum": messung["datum"],
            "Durchschnitt" :round(durchschnitt, 2),
            "Minimum": minimum,
            "Maximum": maximum
        })
    df_summary = pd.DataFrame(summary_liste)

    return df_summary

def get_temp_alarme_ein_tag(df_temp, temp_grenzwert=TEMP_GRENZWERT):
    '''alle Werte, die an einem Tag den Grenzwert überschreiten, 
    speichern wir in einem neuen Data Frame Alarme'''

    df_alarme = df_temp[df_temp["temperatur"] >= temp_grenzwert]

    return df_alarme

def get_temp_alarme_patient(patienten_id, temp_grenzwert=TEMP_GRENZWERT):
    '''Auflistung aller Alamre für die Patient:in, die den Grenzwert überschreiten
    mit zuordnung zur ID'''

    temp_liste = get_temp_messdaten_by_id(patienten_id)

    alarm_liste = []

    for messung in temp_liste:
        df_temp = load_temp_csv(messung["dateipfad"])

        df_alarme = get_temp_alarme_ein_tag(df_temp, temp_grenzwert)

        for alarm in df_alarme.to_dict("records"): 
            #records = jede Zeile des Data Frames wird zu einem Dictionary
            alarm_liste.append({
                "Patient-ID": patienten_id,
                "Datum": messung["datum"],
                "Uhrzeit": alarm["uhrzeit"],
                "Temperatur": alarm["temperatur"],
                "Grenzwert": temp_grenzwert
            })

    df_alarme_patient = pd.DataFrame(alarm_liste)

    return df_alarme_patient

def get_temp_alarme_alle_patienten(temp_grenzwert=TEMP_GRENZWERT):
    ''' hier werden alle Alarme aller Patienten zusammengefasst, die den Grenzwert überschreiten  
        nicht mehr nur die einzelnen Patienten, Grundlage für Alarm Dashboard'''
    patienten_data = load_person_data()

    alle_alarme_liste = []

    for patient in patienten_data:
        patienten_id = patient["id"]

        df_alarme_patient = get_temp_alarme_patient(patienten_id, temp_grenzwert)

        for alarm in df_alarme_patient.to_dict("records"):
            alle_alarme_liste.append({
                "Patient-ID": alarm["Patient-ID"],
                "Name": patient["nachname"] + ", " + patient["vorname"],
                "Telefon": patient["telefon"],
                "Datum": alarm["Datum"],
                "Uhrzeit": alarm["Uhrzeit"],
                "Temperatur": alarm["Temperatur"],
                "Grenzwert": alarm["Grenzwert"]
            })

    df_alarme_alle = pd.DataFrame(alle_alarme_liste)

    return df_alarme_alle

def get_temp_alarm_summary_alle_patienten(temp_grenzwert=TEMP_GRENZWERT):
    ''' auf Basis der vorherigen Funktion, aber kompaktere Alarmübersicht, 
        sodass es pro Patient und Tag nur eine Tabellenzeile gibt '''

    df_alarme = get_temp_alarme_alle_patienten(temp_grenzwert)

    if len(df_alarme) == 0:
        return pd.DataFrame()

    summary_liste = []

    gruppen = df_alarme.groupby(["Patient-ID", "Name", "Telefon", "Datum"]) # alle Alarmzeile 

    for gruppen_name, gruppe in gruppen:
        patienten_id = gruppen_name[0]
        name = gruppen_name[1]
        telefon = gruppen_name[2]
        datum = gruppen_name[3]

        anzahl_alarme = len(gruppe)
        max_temperatur = gruppe["Temperatur"].max()
        erste_auffaelligkeit = gruppe["Uhrzeit"].min()
        #letzte_auffaelligkeit = gruppe["Uhrzeit"].max()
        max_temperatur = gruppe["Temperatur"].max()
        schweregrad = get_temp_schweregrad(max_temperatur)

        summary_liste.append({          # neue zusammengefasste Zeile 
            "Patient-ID": patienten_id,
            "Name": name,
            "Telefon": telefon,
            "Datum": datum,
            "Anzahl Alarme": anzahl_alarme,
            "Max. Temperatur": round(max_temperatur, 2),
            "Schweregrad": schweregrad,
            "Erste Auffälligkeit": erste_auffaelligkeit,
            #"Letzte Auffälligkeit": letzte_auffaelligkeit
        })

    df_summary = pd.DataFrame(summary_liste)

    return df_summary

def get_temp_schweregrad(max_temperatur):
    '''Schweregrad des Alarms wird bestimmt'''
    if max_temperatur >= 39.0:
        return "hoch"

    elif max_temperatur >= 38.5:
        return "deutlich erhöht"

    else:
        return "leicht erhöht"

#Plots bzw. Streamlit Ausgabe
def plot_temp_summary(df_summary, temp_grenzwert=TEMP_GRENZWERT):
    ''' hier wird der Trend über die 5 Tage geplottet, mit Durchschnitt, Minimum und Maximum'''
    fig = px.line(
        df_summary,
        x="Datum",
        y=["Durchschnitt", "Minimum", "Maximum"],
        title="Temperaturverlauf",
        markers=True,
        color_discrete_map={
        "Durchschnitt": "blue",
        "Minimum": "green",
        "Maximum": "orange"
        }
    )

    fig.add_hline(
        y=temp_grenzwert,
        line_color="rgba(255, 0, 0, 0.35)",
        line_width=1,
        annotation_text="Grenzwert " + str(temp_grenzwert) + " °C",
        annotation_position="top left"
    )

    df_alarme = df_summary[df_summary["Durchschnitt"] >= temp_grenzwert]

    fig.add_trace(
        go.Scatter(
            x=df_alarme["Datum"],
            y=df_alarme["Durchschnitt"],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Alarm Durchschnitt"
        )
    )
    
    fig.update_layout(
        xaxis_title="Datum",
        yaxis_title="Temperatur in °C"
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_temp_ein_tag(df_temp, datum, temp_grenzwert=TEMP_GRENZWERT): 
    ''' einen Tag plotten mit 1 Wert/h'''
    fig = px.line(
        df_temp,
        x="uhrzeit",
        y="temperatur",
        title="Temperaturverlauf am " + datum,
        markers=True
    )

    df_alarme = get_temp_alarme_ein_tag(df_temp, temp_grenzwert=temp_grenzwert)

    fig.add_trace(
        go.Scatter(
            x=df_alarme["uhrzeit"],
            y=df_alarme["temperatur"],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Alarm"
        )
    )

    fig.add_hline(
        y=temp_grenzwert,
        line_color="rgba(255, 0, 0, 0.35)",
        line_width=1,
        annotation_text="Grenzwert " + str(temp_grenzwert) + " °C",
        annotation_position="top left"
    )

    fig.update_layout(
        xaxis_title="Uhrzeit",
        yaxis_title="Temperatur in °C"
    )

    st.plotly_chart(fig, use_container_width=True)

def show_temp_alarm_info_ein_tag(df_temp, temp_grenzwert=TEMP_GRENZWERT):
    '''textliche Ausgabe, wie viele Alarme an einem Tag aufgetreten sind 
   und welche Uhrzeiten betroffen waren'''

    df_alarme = get_temp_alarme_ein_tag(df_temp, temp_grenzwert)

    if len(df_alarme) == 0:
        st.success("Keine Temperaturalarme an diesem Tag.")
    else:
        st.warning(
            str(len(df_alarme))
            + " Temperaturalarme an diesem Tag über "
            + str(temp_grenzwert)
            + " °C."
        )

        #st.dataframe(df_alarme) # wenn das drin ist wird noch der df mit allen Alarmen und Zeitpunkten angezeigt
        #sieht nicht schön aus und ist nicht sehr hilfreich

def show_temp_tag_auswahl(temp_liste):
    ''' Auswahlbox um einen der letzten 5 Tage anzuschauen '''

    datum_liste = []

    for messung in temp_liste:
        datum_liste.append(messung["datum"])

    selected_datum = st.selectbox(
        "Messtag auswählen",
        datum_liste
    )

    selected_messung = None

    for messung in temp_liste: 
        #dem ausgewähltem Datum wieder den richtigen Dateipfad zuordnen
        if messung["datum"] == selected_datum:
            selected_messung = messung

    df_temp = load_temp_csv(selected_messung["dateipfad"])

    plot_temp_ein_tag(df_temp, selected_datum)

    show_temp_alarm_info_ein_tag(df_temp)

def show_temp_auswertung(patienten_id):
    # alles zusammenfassen zu den Grafiken um in anzeige() nicht so viel reinschreiben zu müssen
    temp_liste = get_temp_messdaten_by_id(patienten_id)

    if len(temp_liste) == 0:
        st.warning("Für diese Patient:in liegen keine Temperaturmessungen vor.")
        return

    df_summary = temp_summary(temp_liste)

    with st.container(border=True):
        st.subheader("Temperaturtrend über 5 Tage")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Ø Temperatur",
                str(round(df_summary["Durchschnitt"].mean(), 1)) + " °C"
            )

        with col2:
            st.metric(
                "Max. Temperatur",
                str(round(df_summary["Maximum"].max(), 1)) + " °C"
            )

        with col3:
            alarmtage = len(df_summary[df_summary["Durchschnitt"] >= TEMP_GRENZWERT])
            st.metric(
                "Alarmtage",
                str(alarmtage)
            )

        plot_temp_summary(df_summary, temp_grenzwert=TEMP_GRENZWERT)

    with st.container(border=True):
        st.subheader("Tagesansicht")
        show_temp_tag_auswahl(temp_liste)

def show_temp_alarmuebersicht():
    '''Zeigt eine Übersicht aller Temperaturalarme aller Patienten mit der summary als Basis
        Pro Patient und Tag wird eine Zeile angezeigt'''
    
    st.subheader("Alarmübersicht")

    df_alarm_summary = get_temp_alarm_summary_alle_patienten()

    if len(df_alarm_summary) == 0:
        st.success("Aktuell liegen keine Temperaturalarme vor.")
        return

    schweregrad_sortierung = {
        "hoch": 3,
        "deutlich erhöht": 2,
        "leicht erhöht": 1
    }

    df_alarm_summary["Schweregrad-Sortierung"] = df_alarm_summary["Schweregrad"].map(schweregrad_sortierung)

    df_alarm_summary = df_alarm_summary.sort_values(
        by=["Datum", "Schweregrad-Sortierung", "Max. Temperatur"],
        ascending=[False, False, False]
    )

    df_alarm_summary = df_alarm_summary.drop(columns=["Schweregrad-Sortierung"])

    with st.container(border=True):
        st.write("### Zusammenfassung")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Auffällige Tage",
                len(df_alarm_summary)
            )

    with col2:
        anzahl_patienten_mit_alarm = df_alarm_summary["Patient-ID"].nunique() 
        #nunique bedeutet, dass die IDs gezählt werden,aber nur die die sich von vorherigen unterscheiden
        st.metric(
            "Patient:innen mit Alarm",
            anzahl_patienten_mit_alarm
    )

        with col3:
            anzahl_hoch = len(df_alarm_summary[df_alarm_summary["Schweregrad"] == "hoch"])
            st.metric("Hohe Alarme", anzahl_hoch)

    with st.container(border=True):
        st.write("### Alarmtabelle")

        schweregrad_filter = st.selectbox(
            "Schweregrad filtern",
            ["Alle", "hoch", "deutlich erhöht", "leicht erhöht"]
        )

        if schweregrad_filter != "Alle":
            df_alarm_summary = df_alarm_summary[
                df_alarm_summary["Schweregrad"] == schweregrad_filter
            ]

        st.dataframe(
            df_alarm_summary,
            use_container_width=True,
            hide_index=True
        )

def anzeige_arzt():
    '''die Funktion ist wichtig, da sie die Schnittstelle zur main.py darstellt'''
    
    tab_patienten,tab_alarme, tab_mitteilungen = st.tabs(["Patient:innen", "Alarmübersicht", "Mitteilungen"])
    
    with tab_patienten:
        show_patientenansicht_arzt()

    with tab_alarme:
        show_temp_alarmuebersicht()

    with tab_mitteilungen:
        anzeige_mitteilungen_arzt()

def anzeige_mitteilungen_arzt():
    '''Zeigt alle versendeten Mitteilungen.'''
    mitteilungen = load_mitteilungen()
    st.subheader("Mitteilungen")

    if "ausgewaehlte_mitteilung_arzt" not in st.session_state:
        st.session_state.ausgewaehlte_mitteilung_arzt = None

    # Übersicht:
    if st.session_state.ausgewaehlte_mitteilung_arzt is None:

        if len(mitteilungen) == 0:
            st.info("Es wurden noch keine Mitteilungen versendet.")
            return

        for nummer, mitteilung in enumerate(reversed(mitteilungen)):    # Auch hier wieder enumerate damit jeder Mitteilung eine Nummer zugewiesen wird, und reversed, dass die Neuste ganz am Anfang steht
            with st.container(border=True):

                nachricht, pfeil = st.columns([6, 1])

                with nachricht:
                    st.write("**" + mitteilung["titel"] + "**")
                    st.write(mitteilung["patient"])
                    st.caption(mitteilung["datum"])

                with pfeil:
                    if st.button(">", key=f"arzt_{nummer}"):
                        st.session_state.ausgewaehlte_mitteilung_arzt = mitteilung
                        st.rerun()
    # Detailansicht:
    else:
        mitteilung = st.session_state.ausgewaehlte_mitteilung_arzt
        st.subheader(mitteilung["titel"])
        st.write("Patient:in:" + mitteilung["patient"])
        st.caption(mitteilung["datum"])
        st.divider()
        st.write(mitteilung["text"])
        if st.button("Zurück"):
            st.session_state.ausgewaehlte_mitteilung_arzt = None
            st.rerun()