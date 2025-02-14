import streamlit as st
import pandas as pd
import altair as alt
import random
import tempfile

from fpdf import FPDF
from altair_saver import save as altair_save

def clamp(val, min_val=0, max_val=10):
    return max(min_val, min(val, max_val))

def get_zone(competence, joy):
    """
    Zoneneinteilung für X=Kompetenz, Y=Freude
      - 🔴 Automatisierungs-Zone: x ≤ 5, y ≤ 5
      - 🟡 Gefahren-Zone: x > 5, y ≤ 5
      - 🟢 KI-Unterstützungs-Zone: x ≤ 5, y > 5
      - 🔵 Genie-Zone: x > 5, y > 5
    """
    if competence <= 5 and joy <= 5:
        return "🔴 Automatisierungs-Zone"
    elif competence > 5 and joy <= 5:
        return "🟡 Gefahren-Zone"
    elif competence <= 5 and joy > 5:
        return "🟢 KI-Unterstützungs-Zone"
    else:
        return "🔵 Genie-Zone"

def create_pdf(df, chart):
    """
    Erzeugt ein PDF, das sowohl die Tabelle als auch das Diagramm enthält.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, txt="Auswertung deiner Aufgaben", ln=1)

    # --- 1) Tabelle als Text
    pdf.set_font("Arial", size=12)
    for idx, row in df.iterrows():
        line = f"{row['Aufgabe']} | Kompetenz={row['Kompetenz']} | Freude={row['Freude']} | Zone={row['Zone']}"
        pdf.multi_cell(0, 10, txt=line)

    pdf.ln(5)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 8, txt="Nachfolgendes Diagramm (Altair) als PNG eingebettet.")

    # --- 2) Diagramm als PNG
    # Wir speichern das Altair-Chart TEMPORÄR als PNG und fügen es ein
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        tmp_filename = tmpfile.name

    # altair_saver exportiert das Chart als PNG (Benötigt Node.js oder Selenium)
    altair_save(chart, tmp_filename, scale_factor=2)  
    # scale_factor=2 => höhere Auflösung

    # Im PDF platzieren (x=10, y=100 als Beispiel)
    # W oder H auf 0 => auto-skalierung
    pdf.image(tmp_filename, x=10, y=None, w=180)

    # PDF als Bytes zurückgeben
    return pdf.output(dest="S").encode("latin-1")

def main():
    st.title("Coach Aufgabenliste mit PDF-Download (inkl. Diagramm)")

    if "tasks" not in st.session_state:
        st.session_state.tasks = [
            "Content-Ideen entwickeln",
            "Posts schreiben",
            "Reels drehen",
            "Emails schreiben",
            "Lead Magnete erstellen",
            "Inhalte für Kurse erstellen",
            "Landingpages erstellen",
            "Vernetzen mit Profilen",
            "Termine setten",
            "Angebote versenden",
            "Sales Calls auswerten",
            "Kundenfragen beantworten",
            "Termine organisieren",
            "Rechnungen schreiben",
            "Positionierung verbessern",
            "Business-Strategie optimieren",
            "Marktanalyse durchführen",
            "Programme weiterentwickeln",
            "Persönliche Weiterbildung",
        ]

    if "competence" not in st.session_state:
        st.session_state.competence = {}
    if "joy" not in st.session_state:
        st.session_state.joy = {}

    # Standardwerte
    for t in st.session_state.tasks:
        if t not in st.session_state.competence:
            st.session_state.competence[t] = 5
        if t not in st.session_state.joy:
            st.session_state.joy[t] = 5

    # Neue Aufgabe
    st.subheader("Neue Aufgabe hinzufügen")
    new_task = st.text_input("Aufgabe eingeben:")
    if st.button("Hinzufügen"):
        if new_task.strip() and new_task not in st.session_state.tasks:
            st.session_state.tasks.append(new_task)
            st.session_state.competence[new_task] = 5
            st.session_state.joy[new_task] = 5
            st.success(f"Aufgabe '{new_task}' hinzugefügt!")

    # Slider
    st.subheader("Bewerte jede Aufgabe (Kompetenz & Freude, 1-10)")
    for task in st.session_state.tasks:
        with st.expander(f"{task}"):
            st.session_state.competence[task] = st.slider(
                f"Kompetenz: '{task}'",
                1, 10, st.session_state.competence[task],
                key=f"comp_{task}"
            )
            st.session_state.joy[task] = st.slider(
                f"Freude: '{task}'",
                1, 10, st.session_state.joy[task],
                key=f"joy_{task}"
            )

    # Tabelle
    data = []
    for task in st.session_state.tasks:
        comp = st.session_state.competence[task]
        joy = st.session_state.joy[task]
        zone = get_zone(comp, joy)
        data.append({"Aufgabe": task, "Kompetenz": comp, "Freude": joy, "Zone": zone})
    df = pd.DataFrame(data)

    st.subheader("Auswertungstabelle")
    st.write(df)

    # Diagramm (X=Kompetenz, Y=Freude)
    st.subheader("Diagramm: Kompetenz (X) vs. Freude (Y)")
    df["Comp_jitter"] = [clamp(x + random.uniform(-0.2, 0.2), 0, 10) for x in df["Kompetenz"]]
    df["Joy_jitter"]  = [clamp(y + random.uniform(-0.2, 0.2), 0, 10) for y in df["Freude"]]

    base = alt.Chart(df).encode(
        x=alt.X("Comp_jitter:Q", scale=alt.Scale(domain=[0,10]), title="Kompetenz"),
        y=alt.Y("Joy_jitter:Q",  scale=alt.Scale(domain=[0,10]), title="Freude"),
        tooltip=["Aufgabe", "Kompetenz", "Freude", "Zone"]
    )
    points = base.mark_circle(size=80).encode(color="Zone")
    labels = base.mark_text(align='center', baseline='top', dy=5).encode(text="Aufgabe")

    vline = alt.Chart(pd.DataFrame({'x': [5]})).mark_rule(color='gray').encode(x='x')
    hline = alt.Chart(pd.DataFrame({'y': [5]})).mark_rule(color='gray').encode(y='y')

    quadrant_labels_df = pd.DataFrame([
        {"x": 2, "y": 2,  "label": "🔴 Automatisierungs-Zone"},
        {"x": 8, "y": 2,  "label": "🟡 Gefahren-Zone"},
        {"x": 2, "y": 8,  "label": "🟢 KI-Unterstützungs-Zone"},
        {"x": 8, "y": 8,  "label": "🔵 Genie-Zone"}
    ])
    quadrant_labels = alt.Chart(quadrant_labels_df).mark_text(
        fontSize=12,
        fontWeight='bold'
    ).encode(
        x='x:Q',
        y='y:Q',
        text='label:N'
    )

    chart = alt.layer(points, labels, vline, hline, quadrant_labels).properties(
        width=700,
        height=500
    ).configure_axis(grid=False).configure_view(stroke=None)

    st.altair_chart(chart, use_container_width=False)

    # PDF Download: Tabelle + Diagramm
    st.subheader("PDF Download (Tabelle & Diagramm)")

    # Erstelle PDF aus (df, chart)
    pdf_data = create_pdf(df, chart)
    st.download_button(
        label="Als PDF herunterladen",
        data=pdf_data,
        file_name="aufgaben_auswertung.pdf",
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()
