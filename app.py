import streamlit as st
import pandas as pd

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

    # Session State für Aufgaben und Bewertungen initialisieren
    if "tasks" not in st.session_state:
        st.session_state.tasks = [
            # Beispiel-Aufgaben
            "Content-Ideen entwickeln",
            "Beiträge für Social Media schreiben",
            "Reels für Social Media drehen",
            "Podcasts oder Audioformate aufnehmen",
            "Blogartikel schreiben",
            "Email-Newsletter schreiben",
            "Webinare oder Live-Events planen & moderieren",
            "Content für YouTube oder andere Plattformen produzieren",
            "Lead Magnets erstellen",
            "Verkaufsseiten & Landingpages erstellen",
            # usw. weitere wie gewünscht ...
        ]

    # Dictionaries zur Speicherung von Kompetenz- und Freude-Werten
    if "competence" not in st.session_state:
        st.session_state.competence = {}
    if "joy" not in st.session_state:
        st.session_state.joy = {}

    # Sicherstellen, dass alle bestehenden Aufgaben mindestens einen Defaultwert haben
    for t in st.session_state.tasks:
        if t not in st.session_state.competence:
            st.session_state.competence[t] = 5
        if t not in st.session_state.joy:
            st.session_state.joy[t] = 5

    # 1) Neue Aufgabe hinzufügen (direkt inkl. Defaultwerte für Schieber)
    new_task = st.text_input("Neue Aufgabe eingeben (Hinweis: Button muss evtl. 2x gedrückt werden):")
    if st.button("Hinzufügen"):
        if new_task.strip() and new_task not in st.session_state.tasks:
            st.session_state.tasks.append(new_task)
            st.session_state.competence[new_task] = 5
            st.session_state.joy[new_task] = 5
            st.success(f"Aufgabe '{new_task}' hinzugefügt!")

    # 2) Für jede Aufgabe zwei Schieber anzeigen (Kompetenz & Freude)
    st.subheader("Bewertung jeder Aufgabe")
    for task in st.session_state.tasks:
        with st.expander(f"Aufgabe: {task}", expanded=False):
            st.session_state.competence[task] = st.slider(
                f"Kompetenz bei '{task}' (1-10)",
                min_value=1, max_value=10,
                value=st.session_state.competence[task],
                key=f"comp_{task}"
            )
            st.session_state.joy[task] = st.slider(
                f"Freude an '{task}' (1-10)",
                min_value=1, max_value=10,
                value=st.session_state.joy[task],
                key=f"joy_{task}"
            )

    # 3) Auswertung in einer Tabelle
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

    st.markdown(
        """
        **Zonen-Erläuterung**  
        - 🔴 **Automatisierungs-Zone** (niedrige Freude, niedrige Kompetenz) → Automatisieren oder delegieren!  
        - 🟡 **Gefahren-Zone** (hohe Kompetenz, niedrige Freude) → Delegieren oder neu bewerten!  
        - 🟢 **KI-Unterstützungs-Zone** (niedrige Kompetenz, hohe Freude) → Mit KI optimieren!  
        - 🔵 **Genie-Zone** (hohe Freude, hohe Kompetenz) → Hier solltest du den Großteil deiner Zeit verbringen!
        """
    )

if __name__ == "__main__":
    main()
