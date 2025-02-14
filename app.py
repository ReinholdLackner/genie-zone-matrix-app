import streamlit as st
import pandas as pd
import io

def get_zone(competence, joy):
    """
    Zoneneinteilung für X=Kompetenz, Y=Freude:
    - 🔴 Automatisierungs-Zone: Kompetenz <= 5, Freude <= 5
    - 🟡 Gefahren-Zone: Kompetenz > 5, Freude <= 5
    - 🟢 KI-Unterstützungs-Zone: Kompetenz <= 5, Freude > 5
    - 🔵 Genie-Zone: Kompetenz > 5, Freude > 5
    """
    if competence <= 5 and joy <= 5:
        return "🔴 Automatisierungs-Zone"
    elif competence > 5 and joy <= 5:
        return "🟡 Gefahren-Zone"
    elif competence <= 5 and joy > 5:
        return "🟢 KI-Unterstützungs-Zone"
    else:
        return "🔵 Genie-Zone"

def to_excel(df: pd.DataFrame) -> bytes:
    """
    Konvertiert einen DataFrame in ein Excel-Byte-Objekt, 
    das per st.download_button heruntergeladen werden kann.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Aufgaben")
    return output.getvalue()

def main():
    st.title("Coach Aufgabenliste ohne Diagramm, mit Excel-Download")

    # 1) Session State vorbereiten (Tasks, Kompetenz, Freude)
    if "tasks" not in st.session_state:
        st.session_state.tasks = [
            # Beispiel-Aufgaben
            "Content-Ideen entwickeln",
            "Posts schreiben",
            "Reels drehen",
            "Emails schreiben",
            "Lead Magnete erstellen",
            "Inhalte für Kurse erstellen",
            "Landingpages erstellen",
            "Vernetzen mit Profilen",
            "Termine setten",
            "Angebote versenden",
            "Sales Calls auswerten",
            "Kundenfragen beantworten",
            "Termine organisieren",
            "Rechnungen schreiben",
            "Positionierung verbessern",
            "Business-Strategie optimieren",
            "Marktanalyse durchführen",
            "Programme weiterentwickeln",
            "Persönliche Weiterbildung",
        ]

    if "competence" not in st.session_state:
        st.session_state.competence = {}
    if "joy" not in st.session_state:
        st.session_state.joy = {}

    # Standardwerte für alle Aufgaben
    for t in st.session_state.tasks:
        if t not in st.session_state.competence:
            st.session_state.competence[t] = 5
        if t not in st.session_state.joy:
            st.session_state.joy[t] = 5

    # 2) Neue Aufgabe hinzufügen
    st.subheader("Neue Aufgabe hinzufügen")
    new_task = st.text_input("Aufgabe eingeben (Hinweis: Button muss evtl. 2x gedrückt werden)")
    if st.button("Hinzufügen"):
        if new_task.strip() and new_task not in st.session_state.tasks:
            st.session_state.tasks.append(new_task)
            st.session_state.competence[new_task] = 5
            st.session_state.joy[new_task] = 5
            st.success(f"Aufgabe '{new_task}' hinzugefügt!")

    # 3) Slider für jede Aufgabe: Kompetenz & Freude
    st.subheader("Bewerte jede Aufgabe nach Kompetenz & Freude (1-10)")
    for task in st.session_state.tasks:
        with st.expander(f"Aufgabe: {task}", expanded=False):
            st.session_state.competence[task] = st.slider(
                f"Kompetenz: Wie gut kannst du '{task}'?",
                min_value=1, max_value=10,
                value=st.session_state.competence[task],
                key=f"comp_{task}"
            )
            st.session_state.joy[task] = st.slider(
                f"Freude: Wie gern machst du '{task}'?",
                min_value=1, max_value=10,
                value=st.session_state.joy[task],
                key=f"joy_{task}"
            )

    # 4) Tabelle mit Zonenberechnung
    st.subheader("Auswertungstabelle (mit Zone)")
    data = []
    for task in st.session_state.tasks:
        comp = st.session_state.competence[task]
        joy = st.session_state.joy[task]
        zone = get_zone(comp, joy)
        data.append({
            "Aufgabe": task,
            "Kompetenz": comp,
            "Freude": joy,
            "Zone": zone
        })

    df = pd.DataFrame(data)
    st.write(df)

    # 5) Download als Excel
    st.subheader("Download als Excel-Datei")
    excel_data = to_excel(df)
    st.download_button(
        label="Als Excel herunterladen",
        data=excel_data,
        file_name="aufgaben_auswertung.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    main()
