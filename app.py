import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titel der App
st.title("Genie-Zone-Matrix für Online-Coaches")
st.write("Wähle hier Tätigkeiten aus, die du durchführst, und ergänze darunter eigene Tätigkeiten.")

# Standardaufgabenliste
default_tasks = [
    "1:1 Coaching-Sessions", "Gruppen-Coachings", "Content-Ideen entwickeln", "Social Media Beiträge schreiben",
    "Videos drehen", "Webinare moderieren", "Sales Calls führen", "Follow-ups mit Leads", "Kunden-Onboarding",
    "Community-Management", "Newsletter schreiben", "Lead Magnets erstellen", "Marktforschung", "Buchhaltung"
]

# Nutzer kann Aufgaben auswählen
tasks = st.multiselect("Wähle deine Tätigkeiten aus:", default_tasks, default=default_tasks)

# Nutzer kann eigene Aufgaben hinzufügen
st.write("Ergänze eigene Tätigkeiten:")
new_task = st.text_input("Neue Tätigkeit hinzufügen")
if new_task:
    tasks.append(new_task)

# Bewertungen für Freude und Kompetenz erfassen
data = []
for task in tasks:
    st.subheader(task)
    enjoyment = st.slider(f"Freude an {task}", 1, 10, 5)
    proficiency = st.slider(f"Kompetenz in {task}", 1, 10, 5)
    st.markdown("---")  # Trennlinie zwischen den Aufgaben
    data.append([task, enjoyment, proficiency])

# DataFrame erstellen
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

# Ergebnisse als Tabelle anzeigen
st.write("### Deine Genie-Zone-Matrix")
st.dataframe(df)

# Visualisierung der Matrix
fig, ax = plt.subplots(figsize=(8,8))
colors = {"Automatisierungs-Zone": "#FF6961", "KI-Unterstützungs-Zone": "#77DD77", "Gefahren-Zone": "#FDFD96", "Genie-Zone": "#779ECB"}

# Achsen als Kreuz zeichnen
ax.axhline(5, color='black', linestyle='--', linewidth=1)
ax.axvline(5, color='black', linestyle='--', linewidth=1)

# Quadranten benennen
ax.text(8, 9, "Genie-Zone", fontsize=12, fontweight='bold', color='#779ECB')
ax.text(1, 9, "Gefahren-Zone", fontsize=12, fontweight='bold', color='#FDFD96')
ax.text(8, 1, "KI-Unterstützungs-Zone", fontsize=12, fontweight='bold', color='#77DD77')
ax.text(1, 1, "Automatisierungs-Zone", fontsize=12, fontweight='bold', color='#FF6961')

# Punkte in der Matrix darstellen
for _, row in df.iterrows():
    ax.scatter(row["Kompetenz"], row["Freude"], s=200, color=colors[row["Kategorie"]], edgecolors="black")
    ax.text(row["Kompetenz"], row["Freude"], row["Aufgabe"], fontsize=8, ha='right')

ax.set_xticks(range(1, 11))
ax.set_yticks(range(1, 11))
ax.set_xlabel("Kompetenz")
ax.set_ylabel("Freude")
ax.set_title("Genie-Zone-Matrix")
ax.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)
