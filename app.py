import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Titel der App
st.title("Genie-Zone-Matrix für Online-Coaches")

# Session State initialisieren
if "page" not in st.session_state:
    st.session_state.page = 1
if "selected_tasks" not in st.session_state:
    st.session_state.selected_tasks = []
if "custom_tasks" not in st.session_state:
    st.session_state.custom_tasks = []
if "ratings" not in st.session_state:
    st.session_state.ratings = []

# Standardaufgabenliste
default_tasks = [
    "1:1 Coaching-Sessions", "Gruppen-Coachings", "Content-Ideen entwickeln", "Social Media Beiträge schreiben",
    "Videos drehen", "Webinare moderieren", "Sales Calls führen", "Follow-ups mit Leads", "Kunden-Onboarding",
    "Community-Management", "Newsletter schreiben", "Lead Magnets erstellen", "Marktforschung", "Buchhaltung"
]

# Seitensteuerung
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

# **Seite 1: Auswahl der Tätigkeiten**
if st.session_state.page == 1:
    st.write("### Wähle deine Tätigkeiten aus")
    selected_tasks = st.multiselect(
        "Tätigkeiten auswählen:", 
        options=default_tasks + st.session_state.custom_tasks, 
        default=st.session_state.selected_tasks
    )
    
    new_task = st.text_input("Eigene Tätigkeit hinzufügen und Enter drücken:")
    if new_task and new_task not in st.session_state.custom_tasks and new_task not in default_tasks:
        st.session_state.custom_tasks.append(new_task)
        st.session_state.selected_tasks.append(new_task)
        st.experimental_rerun()
    
    if st.button("Weiter →"):
        st.session_state.selected_tasks = selected_tasks
        next_page()

# **Seite 2: Bewertung der Tätigkeiten**
elif st.session_state.page == 2:
    st.write("### Bewerte deine Tätigkeiten nach Freude und Kompetenz")
    ratings = []
    for task in st.session_state.selected_tasks:
        st.write(f"**{task}**")
        enjoyment = st.slider(f"Freude an {task}", 1, 10, 5, key=f"enjoy_{task}")
        proficiency = st.slider(f"Kompetenz in {task}", 1, 10, 5, key=f"prof_{task}")
        ratings.append([task, enjoyment, proficiency])
        st.markdown("---")  # Trennlinie zwischen den Aufgaben
    
    if st.button("← Zurück"):
        prev_page()
    if st.button("Weiter →"):
        st.session_state.ratings = ratings
        next_page()

# **Seite 3: Ergebnisse anzeigen**
elif st.session_state.page == 3:
    st.write("### Deine Genie-Zone-Matrix")
    if not st.session_state.ratings:
        st.warning("Es sind keine Daten verfügbar. Bitte gehe zurück und wähle Aufgaben aus.")
    else:
        df = pd.DataFrame(st.session_state.ratings, columns=["Aufgabe", "Freude", "Kompetenz"])
        
        def categorize_task(enjoyment, proficiency):
            if enjoyment <= 4 and proficiency <= 4:
                return "Automatisierungs-Zone"
            elif 5 <= enjoyment <= 7 and 5 <= proficiency <= 7:
                return "KI-Unterstützungs-Zone"
            elif enjoyment >= 8 and proficiency >= 8:
                return "Genie-Zone"
            else:
                return "Gefahren-Zone"
        
        df["Kategorie"] = df.apply(lambda row: categorize_task(row["Freude"], row["Kompetenz"]), axis=1)
        st.dataframe(df)
        
        fig, ax = plt.subplots(figsize=(6,6), dpi=100)
        colors = {
            "Automatisierungs-Zone": "#FF6961", 
            "KI-Unterstützungs-Zone": "#77DD77", 
            "Gefahren-Zone": "#FDFD96", 
            "Genie-Zone": "#779ECB"
        }
        
        ax.axhline(5, color='black', linestyle='-', linewidth=2)
        ax.axvline(5, color='black', linestyle='-', linewidth=2)
        
        ax.text(8, 9, "Genie-Zone", fontsize=12, fontweight='bold', color='#779ECB')
        ax.text(1, 9, "Gefahren-Zone", fontsize=12, fontweight='bold', color='#FDFD96')
        ax.text(8, 1, "KI-Unterstützungs-Zone", fontsize=12, fontweight='bold', color='#77DD77')
        ax.text(1, 1, "Automatisierungs-Zone", fontsize=12, fontweight='bold', color='#FF6961')
        
        for _, row in df.iterrows():
            ax.scatter(row["Kompetenz"], row["Freude"], s=100, color=colors[row["Kategorie"]], edgecolors="black")
            ax.text(row["Kompetenz"], row["Freude"], row["Aufgabe"], fontsize=8, ha='right')
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title("Genie-Zone-Matrix", fontsize=14, fontweight='bold')
        ax.grid(False)
        st.pyplot(fig)
    
    if st.button("← Zurück"):
        prev_page()
