import streamlit as st
import pandas as pd
import altair as alt

# Hilfsfunktion für die Zoneneinteilung
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
        st.session_state.tasks = [
            # 📌 Content-Erstellung & Marketing
            "Content-Ideen entwickeln",
            "Beiträge für Social Media schreiben",
            "Reels für Social Media drehen",
            "Podcasts oder Audioformate aufnehmen",
            "Email-Newsletter schreiben",
            "Lead Magnets (z.B. E-Books, Checklisten, Webinare) erstellen",
            "Inhalte für Online-Kurse oder Memberships erstellen",
            "Content repurposen (z.B. Blogartikel in Social-Media-Posts umwandeln)",
            "Verkaufsseiten & Landingpages erstellen",

            # 📌 Vertrieb & Kundengewinnung
            "Vernetzen mit Profilen",
            "Termine setten im Chat",
            "Angebote versenden",
            "Sales Calls auswerten",
            "Follow-up mit Interessenten & Leads",

            # 📌 Kundenbetreuung
            "Fragen beantworten (E-Mail, WhatsApp, Gruppe)",
            "Betreuung & Nachbereitung von Coaching-Teilnehmern",
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

    # Kompetenz und Freude für jede Aufgabe zwischenspeichern
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

    # Basischart (Altair)
    base = alt.Chart(df).encode(
        x=alt.X("Kompetenz", scale=alt.Scale(domain=[1,10])),
        y=alt.Y("Freude", scale=alt.Scale(domain=[1,10])),
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
        dx=7  # bisschen nach rechts verschieben
    ).encode(
        text="Aufgabe"
    )

    # Vertikale und horizontale Linien (Trennlinien für Quadranten)
    vline = alt.Chart(pd.DataFrame({'x': [5.5]})).mark_rule(color='gray').encode(x='x')
    hline = alt.Chart(pd.DataFrame({'y': [5.5]})).mark_rule(color='gray').encode(y='y')

    # Quadrantentitel: Koordinaten für die Beschriftungen in den vier Quadranten
    quadrant_labels_df = pd.DataFrame([
        {"x": 2.5, "y": 2.5, "label": "🔴 Automatisierungs-Zone"},
        {"x": 8,   "y": 2.5, "label": "🟡 Gefahren-Zone"},
        {"x": 2.5, "y": 8,   "label": "🟢 KI-Unterstützungs-Zone"},
        {"x": 8,   "y": 8,   "label": "🔵 Genie-Zone"}
    ])
    quadrant_labels = alt.Chart(quadrant_labels_df).mark_text(
        align='center',
        baseline='middle',
        fontSize=14,
        fontWeight='bold',
        color='#333'
    ).encode(
        x='x',
        y='y',
        text='label'
    )

    # Layern: Punkte + Labels + Linien + Quadrantentitel
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

    st.altair_chart(chart, use_container_width=False)

    st.markdown(
        """
        **Quadranten-Übersicht**  
        - 🔴 **Automatisierungs-Zone** (niedrige Freude, niedrige Kompetenz) → Automatisieren oder delegieren!  
        - 🟡 **Gefahren-Zone** (hohe Kompetenz, niedrige Freude) → Delegieren oder neu bewerten!  
        - 🟢 **KI-Unterstützungs-Zone** (niedrige Kompetenz, hohe Freude) → Mit KI optimieren!  
        - 🔵 **Genie-Zone** (hohe Freude, hohe Kompetenz) → Hier solltest du den Großteil deiner Zeit verbringen!
        """
    )

if __name__ == "__main__":
    main()
