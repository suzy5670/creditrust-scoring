import streamlit as st

st.title("Recommandations")
st.caption("Un outil d'aide à la décision, pas un pilote automatique")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("#### Politique d'octroi")
        st.markdown(
            """
- **Garder l'historique de crédit comme critère central** de la politique d'octroi — son poids écrase largement tous les autres facteurs (71,7 points d'écart, confirmé par l'EDA et les trois modèles).

- **Investiguer l'écart géographique** entre zones rurales et semi-urbaines (15,3 points) — pour vérifier s'il reflète un vrai risque économique ou un biais d'accès au crédit à corriger.

- **Utiliser le niveau d'éducation avec prudence** (effet réel mais modéré, 9,6 points) — pour ne pas en faire un critère discriminant.
            """
        )

with col2:
    with st.container(border=True):
        st.markdown("#### Déploiement technique et limites")
        st.markdown(
            """
- **Déployer le modèle retenu** (Random Forest, Rappel de 65,8 %) comme un outil d'aide à la décision, pas un remplacement du conseiller — il laisse encore passer environ 1 dossier à risque sur 3.

- **Limite structurelle** : l'échantillon actuel (614 dossiers) reste réduit pour garantir robustesse statistique et équité entre profils dans un déploiement à grande échelle — la collecte de données supplémentaires est prioritaire.
            """
        )