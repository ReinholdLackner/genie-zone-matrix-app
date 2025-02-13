import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Titel der App
st.title("Genie-Zone-Matrix für Online-Coaches")
st.write("Wähle Tätigkeiten aus, die du durchführst, und bewerte sie nach Freude und Kompetenz.")

# Standardaufgabenliste
default_tasks = [
    "1:1 Coaching-Sessions", "Gruppen-Coachings", "Content-Ideen entwickeln", "Social Media Beiträge schreiben",
    "Videos drehen", "Webinare moderieren", "Sales Calls führen", "Follow-ups mit Leads", "Kunden-Onboarding",
    "Community-Management", "Newsletter schreiben", "Lead Magnets erstellen", "Marktforschung", "Buchhaltung"
]

# Session State initialisieren, um Neustarts zu vermeiden
if "selected_tasks" not in st.session_state:
    st.session_state.selected_tasks = default_tasks.copy()
if "custom_tasks" not in st.session_state:
    st.session_state.custom_tasks = []

# Tätigkeiten auswählen
st.write("Wähle deine Tätigkeiten:")
selected_tasks = st.multiselect(
    "Tätigkeiten auswählen:", 
    options=st.session_state.selected_tasks + st.session_state.custom_tasks, 
    default=st.session_state.selected_tasks
)

# Eigene Tätigkeiten hinzufügen
new_task = st.text_input("Eigene Tätigkeit hinzufügen und Enter drücken:")
if new_task:
    if new_task not in st.session_state.custom_tasks and new_task not in st.session_state.selected_tasks:
        st.session_state.custom_tasks.append(new_task)
        st.rerun()

# Bewertungen für Freude und Kompetenz erfassen
data = []
if selected_tasks:
    for task in selected_tasks:
        with st.expander(task):
            enjoyment = st.slider(f"Freude an {task}", 1, 10, 5, key=f"enjoy_{task}")
            proficiency = st.slider(f"Kompetenz in {task}", 1, 10, 5, key=f"prof_{task}")
            data.append([task, enjoyment, proficiency])
else:
    st.warning("Bitte wähle mindestens eine Tätigkeit aus.")

# DataFrame erstellen, falls Daten vorhanden sind
if data:
    df = pd.DataFrame(data, columns=["Aufgabe", "Freude", "Kompetenz"])

    # Funktion zur Kategorisierung
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

    # Ergebnisse anzeigen
    st.write("### Deine Genie-Zone-Matrix")
    st.dataframe(df)

    # Visualisierung der Matrix
    fig, ax = plt.subplots(figsize=(8,8))
    colors = {
        "Automatisierungs-Zone": "#FF6961", 
        "KI-Unterstützungs-Zone": "#77DD77", 
        "Gefahren-Zone": "#FDFD96", 
        "Genie-Zone": "#779ECB"
    }

    # Achsen als Kreuz zeichnen
    ax.axhline(5, color='black', linestyle='-', linewidth=2)
    ax.axvline(5, color='black', linestyle='-', linewidth=2)

    # Quadranten benennen
    ax.text(8, 9, "Genie-Zone", fontsize=12, fontweight='bold', color='#779ECB')
    ax.text(1, 9, "Gefahren-Zone", fontsize=12, fontweight='bold', color='#FDFD96')
    ax.text(8, 1, "KI-Unterstützungs-Zone", fontsize=12, fontweight='bold', color='#77DD77')
    ax.text(1, 1, "Automatisierungs-Zone", fontsize=12, fontweight='bold', color='#FF6961')

    # Punkte in der Matrix darstellen
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

    # PDF-Download
    def generate_pdf():
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Genie-Zone-Matrix Ergebnisse", ln=True, align='C')
        pdf.ln(10)
        
        for index, row in df.iterrows():
            pdf.cell(200, 10, f"{row['Aufgabe']}: {row['Kategorie']}", ln=True)
        
        pdf.output("Genie-Zone-Matrix.pdf")
        return "Genie-Zone-Matrix.pdf"

    if st.button("PDF herunterladen"):
        pdf_path = generate_pdf()
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(label="Download PDF", data=pdf_file, file_name="Genie-Zone-Matrix.pdf", mime="application/pdf")
