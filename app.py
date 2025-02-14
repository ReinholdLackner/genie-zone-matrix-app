import streamlit as st
import pandas as pd
import altair as alt
import random

def clamp(val, min_val=0, max_val=10):
    """Sorgt dafür, dass val innerhalb [min_val, max_val] bleibt."""
    return max(min_val, min(val, max_val))

def get_zone(competence, joy):
    """
    Ordnet (Kompetenz, Freude) einer der vier Zonen zu.
    """
    if competence <= 5 and joy <= 5:
        return "🔴 Automatisierungs-Zone"
    elif competence > 5 and joy <= 5:
        return "🟡 Gefahren-Zone"
    elif competence <= 5 and joy > 5:
        return "🟢 KI-Unterstützungs-Zone"
    else:
        return "🔵 Genie-Zone"

def main():
    st.title("Coach Aufgabenliste mit Bewertung – Zonenlabels außerhalb")

    # Aufgabenliste (Beispiel)
    if "tasks" not in st.session_state:
        st.session_state.tasks = [
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

    # Kompetenz und Freude initialisieren
    if "competence" not in st.session_state:
        st.session_state.competence = {}
    if "joy" not in st.session_state:
        st.session_state.joy = {}

    # Standardwerte
    for t in st.session_state.tasks:
        if t not in st.session_state.competence:
            st.session_state.competence[t] = 5
        if t not in st.session_state.joy:
            st.session_state.joy[t] = 5

    # Neue Aufgabe hinzufügen
    st.subheader("Neue Aufgabe hinzufügen")
    new_task = st.text_input("Aufgabe eingeben")
    if st.button("Hinzufügen"):
        if new_task.strip() and new_task not in st.session_state.tasks:
            st.session_state.tasks.append(new_task)
            st.session_state.competence[new_task] = 5
            st.session_state.joy[new_task] = 5
            st.success(f"Aufgabe '{new_task}' hinzugefügt!")

    # Sliders für jede Aufgabe
    st.subheader("Bewerte Kompetenz & Freude (1-10)")
    for task in st.session_state.tasks:
        with st.expander(f"Aufgabe: {task}", expanded=False):
            st.session_state.competence[task] = st.slider(
                f"Kompetenz: '{task}'",
                min_value=1, max_value=10,
                value=st.session_state.competence[task],
                key=f"comp_{task}"
            )
            st.session_state.joy[task] = st.slider(
                f"Freude: '{task}'",
                min_value=1, max_value=10,
                value=st.session_state.joy[task],
                key=f"joy_{task}"
            )

    # Tabelle anzeigen
    st.subheader("Auswertung: Welche Aufgabe liegt in welcher Zone?")
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

    # Diagramm
    st.subheader("4-Quadranten-Matrix: Kompetenz vs. Freude")

    # Zufalls-Jitter gegen Überlappungen
    df["Kompetenz_jitter"] = [
        clamp(x + random.uniform(-0.2, 0.2), 0, 10) for x in df["Kompetenz"]
    ]
    df["Freude_jitter"] = [
        clamp(y + random.uniform(-0.2, 0.2), 0, 10) for y in df["Freude"]
    ]

    # Domain auf [-3,13] erweitert, damit Labels bei x=-2/12, y=2/8 sichtbar sind
    base = alt.Chart(df).encode(
        x=alt.X("Kompetenz_jitter:Q", 
                scale=alt.Scale(domain=[-3,13]), 
                title="Kompetenz"),
        y=alt.Y("Freude_jitter:Q", 
                scale=alt.Scale(domain=[-3,13]), 
                title="Freude"),
        tooltip=["Aufgabe", "Kompetenz", "Freude", "Zone"]
    )

    # Punkte
    points = base.mark_circle(size=100).encode(
        color="Zone"
    )

    # Labels der einzelnen Aufgaben
    labels = base.mark_text(
        align='left',
        baseline='middle',
        dx=7
    ).encode(text="Aufgabe")

    # Linien bei x=5 und y=5
    vline = alt.Chart(pd.DataFrame({'x': [5]})).mark_rule(color='gray').encode(x='x')
    hline = alt.Chart(pd.DataFrame({'y': [5]})).mark_rule(color='gray').encode(y='y')

    # Zonenlabels deutlich außerhalb bei x=-2 bzw. 12
    quadrant_labels_df = pd.DataFrame([
        {"x": -2, "y": 2,  "label": "🔴 Automatisierungs-Zone"},
        {"x": 12, "y": 2,  "label": "🟡 Gefahren-Zone"},
        {"x": -2, "y": 8,  "label": "🟢 KI-Unterstützungs-Zone"},
        {"x": 12, "y": 8,  "label": "🔵 Genie-Zone"}
    ])
    quadrant_labels = alt.Chart(quadrant_labels_df).mark_text(
        fontSize=10,
        fontWeight='bold',
        color='#333'
    ).encode(
        x='x:Q',
        y='y:Q',
        text='label:N'
    )

    chart = alt.layer(
        points,
        labels,
        vline,
        hline,
        quadrant_labels
    ).properties(
        width=900,
        height=700
    ).interactive()

    # Kein Grid, kein Rahmen
    chart = chart.configure_axis(grid=False).configure_view(stroke=None)
    st.altair_chart(chart, use_container_width=False)

    st.markdown("""
    **Quadranten-Übersicht**  
    - 🔴 **Automatisierungs-Zone** (niedrige Freude, niedrige Kompetenz) → Automatisieren oder delegieren!  
    - 🟡 **Gefahren-Zone** (hohe Kompetenz, niedrige Freude) → Delegieren oder neu bewerten!  
    - 🟢 **KI-Unterstützungs-Zone** (niedrige Kompetenz, hohe Freude) → Mit KI optimieren!  
    - 🔵 **Genie-Zone** (hohe Kompetenz, hohe Freude) → Hier solltest du den Großteil deiner Zeit verbringen!
    """)

if __name__ == "__main__":
    main()
