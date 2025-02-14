import streamlit as st
import pandas as pd
import altair as alt

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


def page_tasks():
    st.title("Coach Aufgabenliste")
    st.subheader("Aufgaben auswählen:")

    # Checkboxes für alle Aufgaben
    for i, task in enumerate(st.session_state.tasks):
        st.session_state.selected[i] = st.checkbox(
            task,
            key=f"task_{i}",
            value=st.session_state.selected[i]
        )
    
    # Neue Aufgabe hinzufügen
    st.subheader("Neue Aufgabe hinzufügen")
    new_task = st.text_input("Aufgabe eingeben (Hinweis: Button muss evtl. 2x gedrückt werden)")
    if st.button("Hinzufügen"):
        if new_task.strip() and new_task not in st.session_state.tasks:
            st.session_state.tasks.append(new_task)
            st.session_state.selected.append(False)
            st.success(f"Aufgabe '{new_task}' hinzugefügt!")

    # Ausgewählte Aufgaben
    selected_tasks = [
        t for t, sel in zip(st.session_state.tasks, st.session_state.selected) if sel
    ]
    if selected_tasks:
        st.subheader("Aktuell ausgewählte Aufgaben:")
        for stask in selected_tasks:
            st.write(f"- {stask}")
    else:
        st.info("Noch keine Aufgaben ausgewählt.")
    
    # Weiter zur Bewertungsseite
    if st.button("Weiter"):
        st.session_state.page = "bewertung"


def page_bewertung():
    st.title("Bewertung deiner ausgewählten Aufgaben")

    # Liste der aktuell ausgewählten Aufgaben
    selected_tasks = [
        t for t, sel in zip(st.session_state.tasks, st.session_state.selected) if sel
    ]

    if not selected_tasks:
        st.warning("Es wurden keine Aufgaben ausgewählt. Bitte gehe zurück und wähle Aufgaben aus.")
        if st.button("Zurück"):
            st.session_state.page = "tasks"
        return

    # Für jede ausgewählte Aufgabe zwei Slider: Kompetenz & Freude
    competence_values = {}
    joy_values = {}
    st.write("Wähle für jede Aufgabe einen Wert von 1-10 aus, um einzuschätzen, wie gut du darin bist (Kompetenz) und wie viel Freude sie dir bereitet.")
    for i, task in enumerate(selected_tasks):
        with st.expander(task):
            competence_key = f"competence_{i}"
            joy_key = f"joy_{i}"
            if competence_key not in st.session_state:
                st.session_state[competence_key] = 5
            if joy_key not in st.session_state:
                st.session_state[joy_key] = 5

            st.session_state[competence_key] = st.slider(
                f"Kompetenz bei '{task}'",
                min_value=1, max_value=10,
                value=st.session_state[competence_key],
                key=competence_key
            )
            st.session_state[joy_key] = st.slider(
                f"Freude an '{task}'",
                min_value=1, max_value=10,
                value=st.session_state[joy_key],
                key=joy_key
            )

            competence_values[task] = st.session_state[competence_key]
            joy_values[task] = st.session_state[joy_key]

    # DataFrame erstellen für die Auswertung
    data = []
    for task in selected_tasks:
        comp = competence_values[task]
        joy = joy_values[task]
        zone = get_zone(comp, joy)
        data.append({
            "Aufgabe": task,
            "Kompetenz": comp,
            "Freude": joy,
            "Zone": zone
        })

    df = pd.DataFrame(data)

    st.subheader("Matrix-Tabelle")
    st.write(df)

    st.subheader("Visualisierte Matrix (Kompetenz vs. Freude)")

    # Altair-Chart
    chart = (
        alt.Chart(df)
        .mark_circle(size=100)
        .encode(
            x=alt.X("Kompetenz", scale=alt.Scale(domain=[1,10])),
            y=alt.Y("Freude", scale=alt.Scale(domain=[1,10])),
            color="Zone",
            tooltip=["Aufgabe", "Kompetenz", "Freude", "Zone"]
        )
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown(
        """
        **Quadranten-Übersicht**  
        - 🔴 **Automatisierungs-Zone** (niedrige Freude, niedrige Kompetenz) → Automatisieren oder delegieren!  
        - 🟡 **Gefahren-Zone** (hohe Kompetenz, niedrige Freude) → Delegieren oder neu bewerten!  
        - 🟢 **KI-Unterstützungs-Zone** (niedrige Kompetenz, hohe Freude) → Mit KI optimieren!  
        - 🔵 **Genie-Zone** (hohe Freude, hohe Kompetenz) → Hier solltest du den Großteil deiner Zeit verbringen!
        """
    )

    if st.button("Zurück"):
        st.session_state.page = "tasks"


def main():
    # Session State initialisieren
    if "page" not in st.session_state:
        st.session_state.page = "tasks"

    if "tasks" not in st.session_state:
        st.session_state.tasks = [
            # 📌 Content-Erstellung & Marketing
            "Content-Ideen entwickeln",
            "Beiträge für Social Media schreiben",
            "Reels für Social Media drehen",
            "Podcasts oder Audioformate aufnehmen",
            "Blogartikel schreiben",
            "Email-Newsletter schreiben",
            "Webinare oder Live-Events planen & moderieren",
            "Content für YouTube oder andere Plattformen produzieren",
            "Lead Magnets (z.B. E-Books, Checklisten, Webinare) erstellen",
            "Inhalte für Online-Kurse oder Memberships erstellen",
            "Content repurposen (z.B. Blogartikel in Social-Media-Posts umwandeln)",
            "Verkaufsseiten & Landingpages erstellen",
            "Automatisierte Funnels & E-Mail-Marketing aufsetzen",

            # 📌 Vertrieb & Kundengewinnung
            "Vernetzen mit Profilen",
            "Termine setten im Chat",
            "Qualifizierungstelefonate führen",
            "Sales Calls führen",
            "Angebote versenden",
            "Sales Calls auswerten",
            "Follow-up mit Interessenten & Leads",
            "Angebote & Preise kalkulieren",
            "Testimonials & Fallstudien sammeln",

            # 📌 Kundenbetreuung
            "Fragen beantworten (E-Mail, WhatsApp, Gruppe)",
            "Community-Management in Gruppen (z.B. Facebook, Telegram, Discord)",
            "Onboarding neuer Kunden (Einführung, Erwartungen klären)",
            "Offboarding-Prozess & Kundenbindung verbessern",
            "Betreuung & Nachbereitung von Coaching-Teilnehmern",
            "Notizen & Fortschrittsberichte für Kunden führen",

            # 📌 Administration & Organisation
            "Kalender & Termine organisieren",
            "Meetings & Coaching-Sessions planen",
            "Rechnungen schreiben & Buchhaltung führen",
            "Tools & Software verwalten (z.B. Zoom, Notion, Kajabi)",
            "Kundendaten pflegen & verwalten",
            "Datenschutz & rechtliche Vorgaben beachten",
            "E-Mails & Anfragen beantworten",
            "Dokumentationen & Arbeitsabläufe strukturieren",

            # 📌 Strategie & Weiterentwicklung
            "Eigene Positionierung & Branding verbessern",
            "Business-Strategie entwickeln & optimieren",
            "Markt- & Wettbewerbsanalyse durchführen",
            "Angebote & Programme weiterentwickeln",
            "Persönliche Weiterbildung (Kurse, Bücher, Mentoring)",
            "Preisstrategie & Angebotsstruktur überdenken",
            "Feedback auswerten & das Coaching-Angebot optimieren"
        ]

    if "selected" not in st.session_state:
        st.session_state.selected = [False] * len(st.session_state.tasks)

    # Navigation zwischen den Seiten
    if st.session_state.page == "tasks":
        page_tasks()
    elif st.session_state.page == "bewertung":
        page_bewertung()


if __name__ == "__main__":
    main()
