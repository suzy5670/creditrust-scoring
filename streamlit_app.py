import streamlit as st

st.set_page_config(page_title="CrediTrust Scoring", layout="wide")

page = st.navigation([
    st.Page("app_pages/accueil.py", title="Accueil", icon=":material/home:"),
    st.Page("app_pages/analyse.py", title="Analyse", icon=":material/bar_chart:"),
    st.Page("app_pages/choix_du_modele.py", title="Choix du modèle", icon=":material/model_training:"),
    st.Page("app_pages/simulateur.py", title="Simulateur", icon=":material/calculate:"),
    st.Page("app_pages/recommandation.py", title="Recommandation", icon=":material/lightbulb:"),
])

page.run()