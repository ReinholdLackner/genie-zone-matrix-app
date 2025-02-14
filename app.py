import streamlit as st

# Titel der App
st.title("Coaching Aufgaben Manager")

# Aufgabenkategorien und Aufgaben
tasks = {
    "📌 Content-Erstellung & Marketing": [
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
        "Automatisierte Funnels & E-Mail-Marketing aufsetzen"
    ],
    "📌 Vertrieb & Kundengewinnung": [
        "Vernetzen mit Profilen",
        "Termine setten im Chat",
        "Qualifizierungstelefonate führen",
        "Sales Calls führen",
        "Angebote versenden",
        "Sales Calls auswerten",
        "Follow-up mit Interessenten & Leads",
        "Angebote & Preise kalkulieren",
        "Testimonials & Fallstudien sammeln"
    ],
    "📌 Kundenbetreuung": [
        "Fragen beantworten Email, Whatsapp, Gruppe",
        "Community-Management in Gruppen (z.B. Facebook, Telegram, Discord)",
        "Onboarding neuer Kunden (Einführung, Erwartungen klären)",
        "Offboarding-Prozess & Kundenbindung verbessern",
        "Betreuung & Nachbereitung von Coaching-Teilnehmern",
        "Notizen & Fortschrittsberichte für Kunden führen"
    ],
    "📌 Administration & Organisation": [
        "Kalender & Termine organisieren",
        "Meetings & Coaching-Sessions planen",
        "Rechnungen schreiben & Buchhaltung führen",
        "Tools & Software verwalten (z.B. Zoom, Notion, Kajabi)",
        "Kundendaten pflegen & verwalten",
        "Datenschutz & rechtliche Vorgaben beachten",
        "E-Mails & Anfragen beantworten",
        "Dokumentationen & Arbeitsabläufe strukturieren"
    ],
    "📌 Strategie & Weiterentwicklung": [
        "Eigene Positionierung & Branding verbessern",
        "Business-Strategie entwickeln & optimieren",
        "Markt- & Wettbewerbsanalyse durchführen",
        "Angebote & Programme weiterentwickeln",
        "Persönliche Weiterbildung (Kurse, Bücher, Mentoring)",
        "Preisstrategie & Angebotsstruktur überdenken",
        "Feedback auswerten & das Coaching-Angebot optimieren"
    ]
}

# Auswahl der Kategorie
category = st.selectbox("Wähle eine Kategorie", list(tasks.keys()))

# Anzeige der Aufgaben in der ausgewählten Kategorie
st.write(f"Aufgaben in {category}:")
selected_tasks = st.multiselect("Wähle deine wöchentlichen Aufgaben", tasks[category])

# Möglichkeit, eigene Aufgaben hinzuzufügen
new_task = st.text_input("Füge eine eigene Aufgabe hinzu")
if st.button("Aufgabe hinzufügen"):
    if new_task:
        tasks[category].append(new_task)
        st.success(f"Aufgabe '{new_task}' hinzugefügt!")

# Anzeige der ausgewählten Aufgaben
st.write("Deine ausgewählten Aufgaben:")
for task in selected_tasks:
    st.write(f"- {task}")

# Möglichkeit, die ausgewählten Aufgaben zu speichern
if st.button("Aufgaben speichern"):
    st.write("Aufgaben wurden gespeichert!")