import streamlit as st

st.title("Recommandations")

st.write(
    "L'historique de crédit doit rester le critère central de la politique d'octroi, "
    "tant son poids écrase largement tous les autres facteurs (71,7 points d'écart, "
    "confirmé par l'EDA et les trois modèles). À l'inverse, l'écart géographique observé "
    "entre zones rurales et semi-urbaines (15,3 points) mérite d'être investigué pour "
    "vérifier s'il reflète un vrai risque économique ou un biais d'accès au crédit à "
    "corriger, et le niveau d'éducation, dont l'effet est réel mais modéré (9,6 points), "
    "doit être utilisé avec prudence pour ne pas devenir un critère discriminant."
)

st.write(
    "Sur le plan technique, le modèle retenu (Random Forest, Rappel de 65,8 %) doit être "
    "déployé comme un outil d'aide à la décision et non comme un remplacement du "
    "conseiller, puisqu'il laisse encore passer environ un dossier à risque sur trois ; "
    "les prochaines étapes pour l'améliorer incluent l'ajustement du seuil de décision, "
    "un rééquilibrage plus poussé des classes (SMOTE), et surtout la collecte de "
    "davantage de données, l'échantillon actuel (614 dossiers) restant limité pour "
    "garantir une robustesse statistique et une équité totale entre profils dans un "
    "déploiement à grande échelle."
)

st.subheader("Limites à communiquer clairement")
st.markdown(
    """
    - Modèle entraîné sur un échantillon limité (614 dossiers) — à réévaluer régulièrement
    - Le modèle repose presque exclusivement sur `Credit_History`, une variable avec 79 valeurs manquantes dans le dataset actuel
    - Aucune garantie d'équité totale entre profils — un audit de biais régulier est recommandé
    """
)