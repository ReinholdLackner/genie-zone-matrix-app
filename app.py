import streamlit as st
import pandas as pd
import altair as alt
import random

def clamp(val, min_val=0, max_val=10):
    """Sorgt dafür, dass val innerhalb [min_val, max_val] bleibt."""
    return max(min_val, min(val, max_val))

def get_zone(competence, joy):
    """
    Bestimmt anhand von Kompetenz (x) und Freude (y) die passende Zone:
    🔴 (niedrige Kompetenz, niedrige Freude)
    🟡 (hohe Kompetenz, niedrige Freude)
    🟢 (niedrige Kompetenz, hohe Freude)
    🔵 (hohe Kompetenz, hohe Freude)
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
    st.title("Coach Aufgabenliste mit Bewertung")

    # 1) Session State vorbereiten (Tasks, Kompetenz-/Freude-Werte)
    if "tasks" not in st.session_state:
        # Nur 20 Aufgaben
        st.session_state.tasks = [
            # 📌 Content-Erstellung & Marketing
            "Content-Ideen entwickeln",
            "Beiträge für Social Media schreiben",
            "Reels für Social Media drehen",
            "Email-Newsletter schreiben",
            "Lead Magnete (z.B. E-Books, Checklisten, Webinare) erstellen",
            "Inhalte für Online-Kurse oder Memberships erstellen",
            "Verkaufsseiten & Landingpages erstellen",

            # 📌 Vertrieb & Kundengewinnung
            "Vernetzen mit Profilen",
            "Termine setten im Chat",
            "Angebote versenden",
            "Sales Calls auswerten",

            # 📌 Kundenbetreuung
            "Fragen beantworten Email, Whatsapp, Gruppe",
            "Notizen & Fortschrittsberichte für Kunden führen",

            # 📌 Administration & Organisation
            "Kalender & Termine organisieren",
            "Rechnungen schreiben & Buchhaltung führen",

            # 📌 Strategie & Weiterentwicklung
            "Eigene Positionierung & Branding verbessern",
            "Business-Strategie entwickeln & optimieren",
            "Markt- & Wettbewerbsanalyse durchführen",
            "Angebote & Programme weiterentwickeln",
            "Persönliche Weiterbildung (Kurse, Bücher, Mentoring)",
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

    # 3) Für jede Aufgabe Schieber (Kompetenz & Freude)
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

    # 4) Auswertung in einer Tabelle
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

    # 5) Diagramm: 4 Quadranten
    st.subheader("Visualisierung deiner Aufgaben in der 4-Quadranten-Matrix (Kompetenz vs. Freude)")

    # Um Überlagerungen zu vermeiden, fügen wir einen kleinen Zufalls-Jitter hinzu
    df["Kompetenz_jitter"] = [
        clamp(x + random.uniform(-0.2, 0.2), 0, 10) for x in df["Kompetenz"]
    ]
    df["Freude_jitter"] = [
        clamp(y + random.uniform(-0.2, 0.2), 0, 10) for y in df["Freude"]
    ]

    base = alt.Chart(df).encode(
        x=alt.X("Kompetenz_jitter:Q", scale=alt.Scale(domain=[0,10]), title="Kompetenz"),
        y=alt.Y("Freude_jitter:Q", scale=alt.Scale(domain=[0,10]), title="Freude"),
        tooltip=["Aufgabe", "Kompetenz", "Freude", "Zone"]
    )

    # Punkte
    points = base.mark_circle(size=100).encode(
        color="Zone"
    )

    # Textlabels (klein neben den Punkten)
    labels = base.mark_text(
        align='left',
        baseline='middle',
        dx=7  # etwas nach rechts verschieben
    ).encode(
        text="Aufgabe"
    )

    # Vertikale und horizontale Linien (Trennlinien für Quadranten)
    vline = alt.Chart(pd.DataFrame({'x': [5]})).mark_rule(color='gray').encode(x='x')
    hline = alt.Chart(pd.DataFrame({'y': [5]})).mark_rule(color='gray').encode(y='y')

    # Quadrantentitel am Rand platzieren
    quadrant_labels_df = pd.DataFrame([
        {"x": 1,  "y": 1,  "label": "🔴 Automatisierungs-Zone"},
        {"x": 9,  "y": 1,  "label": "🟡 Gefahren-Zone"},
        {"x": 1,  "y": 9,  "label": "🟢 KI-Unterstützungs-Zone"},
        {"x": 9,  "y": 9,  "label": "🔵 Genie-Zone"}
    ])
    quadrant_labels = alt.Chart(quadrant_labels_df).mark_text(
        fontSize=14,
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
        width=700,
        height=600
    ).interactive()

    # Gitterlinien entfernen & Achsen anpassen
    chart = chart.configure_axis(
        grid=False  # keine Rasterlinien
    ).configure_view(
        stroke=None  # kein Rahmen um das Diagramm
    )

    st.altair_chart(chart, use_container_width=False)

    st.markdown(
        """
        **Quadranten-Übersicht**  
        - 🔴 **Automatisierungs-Zone** (niedrige Freude, niedrige Kompetenz) → Automatisieren oder delegieren!  
        - 🟡 **Gefahren-Zone** (hohe Kompetenz, niedrige Freude) → Delegieren oder neu bewerten!  
        - 🟢 **KI-Unterstützungs-Zone** (niedrige Kompetenz, hohe Freude) → Mit KI optimieren!  
        - 🔵 **Genie-Zone** (hohe Kompetenz, hohe Freude) → Hier solltest du den Großteil deiner Zeit verbringen!
        """
    )

if __name__ == "__main__":
    main()
