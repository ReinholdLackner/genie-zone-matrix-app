import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titel der App
st.title("Genie-Zone-Matrix für Online-Coaches")
st.write("Bewerte deine Aufgaben nach Freude und Kompetenz, um deine Genie-Zone zu entdecken!")

# Standardaufgabenliste
default_tasks = [
    "1:1 Coaching-Sessions", "Gruppen-Coachings", "Content-Ideen entwickeln", "Social Media Beiträge schreiben",
    "Videos drehen", "Webinare moderieren", "Sales Calls führen", "Follow-ups mit Leads", "Kunden-Onboarding",
    "Community-Management", "Newsletter schreiben", "Lead Magnets erstellen", "Marktforschung", "Buchhaltung"
]

# Nutzer kann eigene Aufgaben hinzufügen
tasks = st.multiselect("Wähle deine Aufgaben oder füge eigene hinzu:", default_tasks, default=default_tasks)
new_task = st.text_input("Falls du eine eigene Aufgabe hinzufügen möchtest, trage sie hier ein:")
if new_task:
    tasks.append(new_task)

# Bewertungen für Freude und Kompetenz erfassen
data = []
for task in tasks:
    enjoyment = st.slider(f"Freude an {task}", 1, 10, 5)
    proficiency = st.slider(f"Kompetenz in {task}", 1, 10, 5)
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
fig, ax = plt.subplots(figsize=(6,6))
colors = {"Automatisierungs-Zone": "#FF6961", "KI-Unterstützungs-Zone": "#77DD77", "Gefahren-Zone": "#FDFD96", "Genie-Zone": "#779ECB"}

for _, row in df.iterrows():
    ax.scatter(row["Kompetenz"], row["Freude"], s=200, color=colors[row["Kategorie"]], label=row["Kategorie"], edgecolors="black")
    ax.text(row["Kompetenz"], row["Freude"], row["Aufgabe"], fontsize=8, ha='right')

ax.set_xticks(range(1, 11))
ax.set_yticks(range(1, 11))
ax.set_xlabel("Kompetenz")
ax.set_ylabel("Freude")
ax.set_title("Genie-Zone-Matrix")
ax.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)
