# creditrust-scoring
Scoring de crédit pour CrediTrust — analyse exploratoire, modèles de classification (Rappel priorisé) et dashboard Streamlit interactif avec simulateur d'octroi de prêt.

# CrediTrust Scoring

Projet de scoring de crédit pour **CrediTrust**, un établissement de crédit fictif, réalisé dans le cadre de la formation Data. L'objectif est de prédire si une demande de prêt sera accordée ou refusée, à partir du profil du demandeur, et d'aider la banque à prioriser la réduction des **Faux Négatifs** (accorder un prêt à un profil réellement à risque).

## Équipe

Département Risque Financier :
- **Suz** — Data Lead Tech (architecture, pipeline, déploiement)
- **Mouna** — Data Scientist (modélisation, sélection du modèle, simulateur)
- **Joséphine** — Data Analyst (analyse exploratoire, facteurs de risque, recommandations)

## Contexte métier

Un Faux Négatif (accorder un prêt à un profil à risque) coûte bien plus cher à la banque qu'un Faux Positif (refuser un bon client par excès de prudence). L'ensemble du pipeline — prétraitement, choix des modèles, métrique de sélection — priorise donc le **Rappel** sur la classe "refusé", pas l'accuracy globale.

## Données

`loan_data.csv` — 981 lignes, dont 614 dossiers avec statut connu (accordé/refusé), utilisés pour l'analyse et la modélisation. Colonnes : `Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area, Loan_Status`.

## Démarche

1. **Analyse exploratoire (EDA)** — distributions, valeurs manquantes, corrélations, facteurs de risque
2. **Prétraitement** — imputation, encodage, standardisation, sans fuite de données (split avant tout traitement)
3. **Modélisation** — 3 modèles entraînés (Régression Logistique, Arbre de Décision, Random Forest), évalués sur Accuracy, Précision, Rappel, F1 et ROC-AUC
4. **Sélection du modèle** — **Random Forest** retenu (meilleur Rappel : 65,8 %)
5. **Interprétabilité** — `Credit_History` est de très loin le facteur de risque dominant (écart de 71,7 points entre bon et mauvais historique)
6. **Dashboard Streamlit** — analyse interactive + simulateur connecté au modèle

## Résultats clés

| Modèle | Accuracy | Précision | Rappel | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Régression Logistique | 0.862 | 0.957 | 0.579 | 0.721 | 0.852 |
| Arbre de Décision | 0.732 | 0.558 | 0.632 | 0.593 | 0.704 |
| **Random Forest (retenu)** | 0.837 | 0.781 | **0.658** | 0.714 | 0.806 |

## Structure du dépôt
