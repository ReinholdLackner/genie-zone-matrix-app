import streamlit as st

# Titel der App
st.title("Coach-Task-Manager: Überblick über deine wöchentlichen Aufgaben")

st.write("Wähle hier deine wöchentlichen Aufgaben aus den vordefinierten Listen oder füge eigene hinzu.")

# Vordefinierte Aufgaben nach Kategorien
categories = {
    "Content-Erstellung & Marketing": [
        "Content-Ideen entwickeln", "Beiträge für Social Media schreiben", "Reels für Social Media drehen",
        "Podcasts oder Audioformate aufnehmen", "Blogartikel schreiben", "Email-Newsletter schreiben",
        "Webinare oder Live-Events planen & moderieren", "Content für YouTube oder andere Plattformen produzieren",
        "Lead Magnets (z.B. E-Books, Checklisten, Webinare) erstellen",
        "Inhalte für Online-Kurse oder Memberships erstellen", "Content repurposen (z.B. Blogartikel in Social-Media-Posts umwandeln)",
        "Verkaufsseiten & Landingpages erstellen", "Automatisierte Funnels & E-Mail-Marketing aufsetzen"
    ],
    "Vertrieb & Kundengewinnung": [
        "Vernetzen mit Profilen", "Termine setten im Chat", "Qualifizierungstelefonate führen",
        "Sales Calls führen", "Angebote versenden", "Sales Calls auswerten", "Follow-up mit Interessenten & Leads",
        "Angebote & Preise kalkulieren", "Testimonials & Fallstudien sammeln"
    ],
    "Kundenbetreuung": [
        "Fragen beantworten (E-Mail, Whatsapp, Gruppe)", "Community-Management in Gruppen (z.B. Facebook, Telegram, Discord)",
        "Onboarding neuer Kunden (Einführung, Erwartungen klären)", "Offboarding-Prozess & Kundenbindung verbessern",
        "Betreuung & Nachbereitung von Coaching-Teilnehmern", "Notizen & Fortschrittsberichte für Kunden führen"
    ],
    "Administration & Organisation": [
        "Kalender & Termine organisieren", "Meetings & Coaching-Sessions planen", "Rechnungen schreiben & Buchhaltung führen",
        "Tools & Software verwalten (z.B. Zoom, Notion, Kajabi)", "Kundendaten pflegen & verwalten",
        "Datenschutz & rechtliche Vorgaben beachten", "E-Mails & Anfragen beantworten",
        "Dokumentationen & Arbeitsabläufe strukturieren"
    ],
    "Strategie & Weiterentwicklung": [
        "Eigene Positionierung & Branding verbessern", "Business-Strategie entwickeln & optimieren",
        "Markt- & Wettbewerbsanalyse durchführen", "Angebote & Programme weiterentwickeln",
        "Persönliche Weiterbildung (Kurse, Bücher, Mentoring)", "Preisstrategie & Angebotsstruktur überdenken",
        "Feedback auswerten & das Coaching-Angebot optimieren"
    ]
}

# Session State initialisieren
if "selected_tasks" not in st.session_state:
    st.session_state.selected_tasks = []
if "custom_tasks" not in st.session_state:
    st.session_state.custom_tasks = []

# Aufgaben auswählen
st.write("## Wähle deine Aufgaben aus")
for category, tasks in categories.items():
    with st.expander(category):
        selected = st.multiselect(f"{category}", tasks, default=[task for task in tasks if task in st.session_state.selected_tasks])
        for task in selected:
            if task not in st.session_state.selected_tasks:
                st.session_state.selected_tasks.append(task)

# Eigene Aufgaben hinzufügen
st.write("## Eigene Aufgaben hinzufügen")
new_task = st.text_input("Neue Aufgabe hinzufügen und Enter drücken:")
if new_task:
    if new_task not in st.session_state.custom_tasks and new_task not in st.session_state.selected_tasks:
        st.session_state.custom_tasks.append(new_task)
        st.session_state.selected_tasks.append(new_task)
        st.experimental_rerun()

# Anzeige der gewählten Aufgaben
st.write("## Deine ausgewählten Aufgaben")
st.write(st.session_state.selected_tasks)
