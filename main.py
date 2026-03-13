import streamlit as st
import datetime
from fpdf import FPDF
import pandas as pd

# --- CLASSE PDF PERSONNALISÉE ---
class PMS_Report(FPDF):
    def header(self):
        self.set_fill_color(30, 58, 138) # Bleu foncé professionnel
        self.rect(0, 0, 210, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 20, 'RAPPORT OFFICIEL DE CONFORMITÉ SANITAIRE', 0, 1, 'C')
        self.ln(10)

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, title, 0, 1, 'L', fill=True)
        self.ln(2)

# --- CONFIGURATION DE L'APP ---
st.set_page_config(page_title="Système de Maîtrise Sanitaire Pro", layout="wide")

# Menu Principal
menu = st.sidebar.radio("Navigation", ["Audit & Scoring", "Fiches de Suivi", "Plan d'Actions Correctives", "Textes de Loi"])

# Base de données des contrôles
db_controles = {
    "Personnel": {"point": "Hygiène & Tenues", "poids": 5, "loi": "Règl. 852/2004 Annexe II Cap. VIII"},
    "Températures": {"point": "Froid Positif/Négatif", "poids": 5, "loi": "Arrêté 21/12/09 Art. 10"},
    "Traçabilité": {"point": "Étiquetage & DLC", "poids": 5, "loi": "Règl. 178/2002 Art. 18"},
    "Locaux": {"point": "Nettoyage & Désinfection", "poids": 3, "loi": "Règl. 852/2004 Cap. I"},
    "Nuisibles": {"point": "Protection & Contrats", "poids": 4, "loi": "Règl. 852/2004 Cap. IX"}
}

# --- ONGLET 1 : AUDIT & SCORING ---
if menu == "Audit & Scoring":
    st.header("📋 Audit de Conformité")
    st.write("Évaluez les points critiques. Le score est pondéré selon la gravité.")
    
    resultats = {}
    for cat, info in db_controles.items():
        st.subheader(f"{cat}")
        col1, col2 = st.columns([2, 1])
        with col1:
            choix = st.radio(f"{info['point']} (Réf: {info['loi']})", ["Conforme", "Non-Conforme", "N/A"], key=cat, horizontal=True)
        resultats[cat] = 1 if choix == "Conforme" else 0 if choix == "Non-Conforme" else None

    # Calcul du score
    pts_obtenus = sum(v * db_controles[k]['poids'] for k, v in resultats.items() if v is not None)
    pts_max = sum(db_controles[k]['poids'] for k, v in resultats.items() if v is not None)
    score_final = (pts_obtenus / pts_max * 100) if pts_max > 0 else 0

    st.divider()
    st.metric("SCORE DE CONFORMITÉ GLOBAL", f"{score_final:.1f}%")
    
    if score_final < 100:
        st.warning("⚠️ Des actions correctives doivent être saisies pour les points non-conformes.")

# --- ONGLET 2 : FICHES DE SUIVI ---
elif menu == "Fiches de Suivi":
    st.header("📝 Fiches de Suivi Quotidien")
    with st.expander("🌡️ Relevé des Températures"):
        temp_positive = st.number_input("Chambre Froide Positive (°C)", -2.0, 10.0, 3.5)
        temp_negative = st.number_input("Congélateur (°C)", -30.0, -15.0, -18.0)
        st.info("Conformité : 0 à 4°C pour le positif, -18°C pour le négatif.")

    with st.expander("🧼 Registre de Nettoyage"):
        st.checkbox("Cuisine (Sols et murs)")
        st.checkbox("Plans de travail")
        st.checkbox("Sanitaires")

# --- ONGLET 3 : ACTIONS CORRECTIVES ---
elif menu == "Plan d'Actions Correctives":
    st.header("🚀 Plan d'Actions Correctives (PAC)")
    action_text = st.text_area("Description des mesures prises suite aux non-conformités :", 
                               placeholder="Ex: Remplacement du joint de porte chambre froide, formation du nouveau personnel...")
    
    if st.button("💾 Générer le Rapport PDF Complet"):
        pdf = PMS_Report()
        pdf.add_page()
        pdf.section_title("Synthèse de l'Audit")
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 10, f"Score de conformité : {score_final if 'score_final' in locals() else 'N/A'}%", ln=True)
        pdf.ln(5)
        pdf.section_title("Plan d'Actions Correctives")
        pdf.multi_cell(0, 10, action_text if action_text else "Aucune action nécessaire.")
        
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📩 Télécharger le PDF", pdf_bytes, "Rapport_Sanitaire_Pro.pdf", "application/pdf")

# --- ONGLET 4 : TEXTES DE LOI ---
elif menu == "Textes de Loi":
    st.header("⚖️ Références Réglementaires")
    for cat, info in db_controles.items():
        with st.expander(f"Loi sur : {cat}"):
            st.write(f"**Référence :** {info['loi']}")
            st.write("Ce règlement impose une obligation de résultat sur la sécurité des denrées. Toute déviance peut entraîner une fermeture administrative ou des sanctions pénales.")

import plotly.express as px # Ajoutez 'plotly' à votre requirements.txt

