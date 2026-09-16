import streamlit as st

st.title("CrediTrust Scoring")
st.subheader("Équipe projet — Département Risque Financier")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### Suz")
        st.caption("Data Lead Tech")
        st.write("Architecture technique, pipeline de données, déploiement de l'application.")

with col2:
    with st.container(border=True):
        st.markdown("### Mouna")
        st.caption("Data Scientist")
        st.write("Modélisation, sélection du modèle final, simulateur de scoring.")

with col3:
    with st.container(border=True):
        st.markdown("### Joséphine")
        st.caption("Data Analyst")
        st.write("Analyse exploratoire, identification des facteurs de risque, recommandations.")