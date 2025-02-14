import streamlit as st
import pandas as pd
import altair as alt
import random

def clamp(val, min_val=0, max_val=10):
    """Sorgt dafür, dass val innerhalb [min_val, max_val] bleibt."""
    return max(min_val, min(val, max_val))

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
    st.title("Coach Aufgabenliste mit Beispiel-Bewertung")

    """
    Dieses Skript setzt für jede Aufgabe *feste* Beispielwerte (Kompetenz & Freude),
    damit du ein anschauliches Diagramm bekommst. 
    Du kannst die Werte unten beliebig anpassen.
    """

    # 1) Aufgabenliste (20 Stück, gekürzt laut Vorgabe)
    tasks = [
        # 📌 Content-Erstellung & Marketing
        "Content-Ideen entwickeln",
        "Beiträge für Social Media schreiben",
        "Reels für Social Media drehen",
        "Email-Newsletter schreiben",
        "Lead Magnete erstellen",
        "Inhalte für Online-Kurse erstellen",
        "Verkaufsseiten & Landingpages erstellen",

        # 📌 Vertrieb & Kundengewinnung
        "Vernetzen mit Profilen",
        "Termine setten im Chat",
        "Angebote versenden",
        "Sales Calls auswerten",

        # 📌 Kundenbetreuung
        "Fragen beantworten (E-Mail, WhatsApp, Gruppe)",
        "Notizen & Fortschrittsberichte führen",

        # 📌 Administration & Organisation
        "Kalender & Termine organisieren",
        "Rechnungen & Buchhaltung führen",

        # 📌 Strategie & Weiterentwicklung
        "Positionierung & Branding verbessern",
        "Business-Strategie optimieren",
        "Markt- & Wettbewerbsanalyse durchführen",
        "Angebote & Programme weiterentwickeln",
        "Persönliche Weiterbildung",
    ]

    # 2) Beispielwerte für Kompetenz & Freude
    #    (Sodass eine typische Verteilung in allen Quadranten entsteht)
    example_values = {
        "Content-Ideen entwickeln":                      (4, 8),  # KI-Unterstützungs-Zone (niedr. Komp, hohe Freude)
        "Beiträge für Social Media schreiben":           (7, 6),  # Genie-Zone
        "Reels für Social Media drehen":                 (3, 5),  # Automatisierungs-Zone bzw. Grenze -> joy=5, comp=3 => joy>5? Nein => actually (3,5) => joy=5 => <=5 => "Automatisierungs-Zone"? Let's set to (3,4) or (3,5). We'll see. 
        "Email-Newsletter schreiben":                    (6, 5),  # Gefahren-Zone? Actually comp>5=6, joy=5 => joy <=5 => ja, "Gefahren-Zone" 
        "Lead Magnete erstellen":                        (2, 9),  # KI-Unterstützungs-Zone
        "Inhalte für Online-Kurse erstellen":            (9, 9),  # Genie-Zone
        "Verkaufsseiten & Landingpages erstellen":       (5, 5),  # Genauer Schnittpunkt => (<=5, <=5) => "Automatisierungs"? Oder "Genie"? Es ist <=5 => also "Automatisierung"? Besser: (5,4) => "Automatisierung" oder (5,6) => "KI"? We'll do (5,4) => "Automatisierungs"
        "Vernetzen mit Profilen":                        (7, 3),  # Gefahren-Zone (hohe Komp, niedrige Freude)
        "Termine setten im Chat":                        (5, 2),  # Automatisierungs-Zone
        "Angebote versenden":                            (8, 4),  # Gefahren-Zone
        "Sales Calls auswerten":                         (6, 4),  # Gefahren-Zone
        "Fragen beantworten (E-Mail, WhatsApp, Gruppe)": (4, 3),  # Automatisierungs-Zone
        "Notizen & Fortschrittsberichte führen":         (5, 7),  # KI-Unterstützungs-Zone
        "Kalender & Termine organisieren":               (2, 2),  # Automatisierungs-Zone
        "Rechnungen & Buchhaltung führen":               (7, 2),  # Gefahren-Zone
        "Positionierung & Branding verbessern":          (6, 9),  # Genie-Zone
        "Business-Strategie optimieren":                 (8, 7),  # Genie-Zone
        "Markt- & Wettbewerbsanalyse durchführen":       (4, 6),  # KI-Unterstützungs-Zone
        "Angebote & Programme weiterentwickeln":         (4, 9),  # KI-Unterstützungs-Zone
        "Persönliche Weiterbildung":                     (3, 7),  # KI-Unterstützungs-Zone
    }

    # 3) Tabelle erzeugen
    data = []
    for task in tasks:
        # Hole die Beispielwerte
        comp, joy = example_values.get(task, (5,5))
        zone = get_zone(comp, joy)
        data.append({
            "Aufgabe": task,
            "Kompetenz": comp,
            "Freude": joy,
            "Zone": zone
        })

    df = pd.DataFrame(data)

    st.subheader("Beispielhafte Tabelle mit Bewertungen")
    st.write(df)

    # 4) Diagramm (4 Quadranten) - ohne Raster, 0 bis 10, keine Überdeckung
    # Um minimale Überdeckung zu vermeiden, fügen wir einen leichten Jitter hinzu
    df["Kompetenz_jitter"] = [
        clamp(x + random.uniform(-0.1, 0.1), 0, 10) for x in df["Kompetenz"]
    ]
    df["Freude_jitter"] = [
        clamp(y + random.uniform(-0.1, 0.1), 0, 10) for y in df["Freude"]
    ]

    st.subheader("Beispiel-Diagramm: Vier Quadranten (Kompetenz vs. Freude)")

    base = alt.Chart(df).encode(
        x=alt.X("Kompetenz_jitter:Q", scale=alt.Scale(domain=[0,10]), title="Kompetenz"),
        y=alt.Y("Freude_jitter:Q", scale=alt.Scale(domain=[0,10]), title="Freude"),
        tooltip=["Aufgabe", "Kompetenz", "Freude", "Zone"]
    )

    # Punkte
    points = base.mark_circle(size=100).encode(
        color="Zone"
    )

    # Labels
    labels = base.mark_text(
        align='left',
        baseline='middle',
        dx=7  
    ).encode(
        text="Aufgabe"
    )

    # Trennlinien auf x=5, y=5
    vline = alt.Chart(pd.DataFrame({'x': [5]})).mark_rule(color='gray').encode(x='x')
    hline = alt.Chart(pd.DataFrame({'y': [5]})).mark_rule(color='gray').encode(y='y')

    # Quadrantentitel am Rand
    quadrant_labels_df = pd.DataFrame([
        {"x": 1,  "y": 1,  "label": "🔴 Automatisierungs-Zone"},
        {"x": 9,  "y": 1,  "label": "🟡 Gefahren-Zone"},
        {"x": 1,  "y": 9,  "label": "🟢 KI-Unterstützungs-Zone"},
        {"x": 9,  "y": 9,  "label": "🔵 Genie-Zone"}
    ])
    quadrant_labels = alt.Chart(quadrant_labels_df).mark_text(
        fontSize=14,
        fontWeight='bold',
        color='#333'
    ).encode(
        x='x:Q',
        y='y:Q',
        text='label:N'
    )

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

    # Gitterlinien entfernen & Achsen anpassen
    chart = chart.configure_axis(
        grid=False
    ).configure_view(
        stroke=None
    )

    st.altair_chart(chart, use_container_width=False)

    st.markdown("""
    **Quadranten-Übersicht**  
    - 🔴 **Automatisierungs-Zone** (niedrige Freude, niedrige Kompetenz) → Automatisieren oder delegieren!  
    - 🟡 **Gefahren-Zone** (hohe Kompetenz, niedrige Freude) → Delegieren oder neu bewerten!  
    - 🟢 **KI-Unterstützungs-Zone** (niedrige Kompetenz, hohe Freude) → Mit KI optimieren!  
    - 🔵 **Genie-Zone** (hohe Kompetenz, hohe Freude) → Hier solltest du den Großteil deiner Zeit verbringen!
    """)

if __name__ == "__main__":
    main()
