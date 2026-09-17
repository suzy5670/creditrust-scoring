import streamlit as st

st.title("Présentation du projet")

st.subheader("Contexte métier")
st.write(
    "CrediTrust est un établissement de crédit qui souhaite s'appuyer sur un modèle "
    "prédictif pour évaluer le risque associé à une demande de prêt. L'objectif est de "
    "prédire si un dossier sera accordé ou refusé, à partir des caractéristiques du "
    "demandeur (revenus, historique de crédit, situation familiale, etc.)."
)
st.write(
    "Toutes les erreurs de prédiction n'ont pas le même coût : accorder un prêt à un "
    "profil réellement à risque représente une perte financière potentielle bien plus "
    "grave pour la banque qu'un refus par excès de prudence. L'évaluation des modèles "
    "priorise donc la réduction des Faux Négatifs, plutôt que la seule accuracy globale."
)

st.subheader("Démarche globale du projet")
st.markdown(
    """
    1. **Analyse exploratoire (EDA)** du fichier `loan_data.csv` (981 lignes, 614 dossiers labellisés) pour faire émerger les facteurs de risque bancaire
    2. **Prétraitement complet** des données (valeurs manquantes, encodage, scaling) sans fuite de données
    3. **Entraînement de 3 modèles** de classification binaire (Régression Logistique, Arbre de Décision, Random Forest)
    4. **Sélection du modèle optimal** (Random Forest) sur la base du Rappel, et analyse d'interprétabilité
    5. **Dashboard Streamlit** : KPIs, graphiques interactifs, et simulateur connecté au modèle
    """
)

st.subheader("Ce que nous avons trouvé")
st.write(
    "L'historique de crédit (`Credit_History`) est de très loin le facteur de risque "
    "dominant (écart de 71,7 points entre bon et mauvais historique), confirmé à la fois "
    "par l'analyse exploratoire et par les trois modèles entraînés. Le revenu et le "
    "montant du prêt, pris isolément, n'ont en revanche presque aucun pouvoir explicatif."
)