import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import joblib

st.title("Analyse du risque de crédit")

@st.cache_data
def charger(fichier):
    return pd.read_csv(fichier)

kpis = charger("kpis.csv").iloc[0]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. Ampleur du risque",
    "2. Historique de crédit",
    "3. Zone géographique",
    "4. Diplôme",
    "5. Choix du modèle",
    "Simulateur",
])

# ============ Slide 1 ============
with tab1:
    st.subheader("Quelle est l'ampleur du risque de refus chez CrediTrust aujourd'hui ?")
    st.caption("KPI 1 + 2 — Taux de refus global, nombre de dossiers")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Taux de refus global", f"{kpis['taux_refus_global']} %")
    with col2:
        st.metric("Dossiers analysés", f"{int(kpis['nb_dossiers'])}")

    fig, ax = plt.subplots(figsize=(6,3.5))
    rep = charger("graph_repartition.csv")
    valeurs = rep["nombre"].tolist()
    labels = rep["statut"].tolist()
    couleurs = ["#1E3A5F", "#D97706"]
    barres = ax.bar(labels, valeurs, color=couleurs, width=0.5)
    pourcentages = [round(100 - kpis["taux_refus_global"], 1), kpis["taux_refus_global"]]
    for barre, valeur, pct, couleur in zip(barres, valeurs, pourcentages, couleurs):
        ax.text(barre.get_x() + barre.get_width()/2, barre.get_height() + 10,
                 f"{valeur}\n({pct}%)", ha="center", va="bottom",
                 fontsize=12, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=couleur))
    ax.set_ylabel("Nombre de dossiers")
    ax.set_ylim(0, max(valeurs) * 1.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig)

# ============ Slide 2 ============
with tab2:
    st.subheader("L'historique de crédit doit-il rester le critère prioritaire dans la décision d'octroi ?")
    st.caption("KPI 3 + 4 — Taux de refus par Credit_History")

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Refus (mauvais historique)", f"{kpis['taux_refus_credit_mauvais']} %")
    with col4:
        st.metric("Refus (bon historique)", f"{kpis['taux_refus_credit_bon']} %")

    credit = charger("graph_credit.csv")
    fig, axes = plt.subplots(1, 2, figsize=(6,3))
    couleurs_credit = {0.0: "#D97706", 1.0: "#1E3A5F"}
    noms_credit = {0.0: "Mauvais historique", 1.0: "Bon historique"}
    for ax, (_, row) in zip(axes, credit.iterrows()):
        taux = row["taux_refus"]
        ax.pie([taux, 100-taux], colors=[couleurs_credit[row["Credit_History"]], "#EAEAEA"], startangle=90, wedgeprops=dict(width=0.35))
        ax.text(0, 0, f"{taux}%", ha="center", va="center", fontsize=14, fontweight="bold")
        ax.set_title(noms_credit[row["Credit_History"]], fontsize=9)
    st.pyplot(fig)

# ============ Slide 3 ============
with tab3:
    st.subheader("Existe-t-il une inégalité géographique dans l'octroi de crédit ?")
    st.caption("KPI 5 — Taux de refus par Property_Area")

    zone = charger("graph_zone.csv").set_index("Property_Area")["taux_refus"].sort_values()
    taux_refus_global = kpis["taux_refus_global"]

    fig, ax = plt.subplots(figsize=(11,6))
    couleurs_zones = ["#1F4E79" if v == zone.min() else "#E8A33D" if v == zone.max() else "#8CA6C9" for v in zone]
    barres = ax.barh(zone.index, zone.values, color=couleurs_zones, height=0.5)
    for barre, valeur in zip(barres, zone.values):
        ax.text(valeur + 1, barre.get_y() + barre.get_height()/2, f"{valeur}%", va="center", fontsize=16, fontweight="bold")
    ax.axvline(taux_refus_global, color="black", linestyle="--", linewidth=1.2)
    ax.text(taux_refus_global, len(zone) - 0.15, f" Moyenne : {taux_refus_global}%", fontsize=12, style="italic", va="bottom")
    ax.set_title(f"{zone.idxmax()} : la zone la plus exposée au refus de prêt", fontsize=18, fontweight="bold", pad=35)
    ax.set_xlabel("Taux de refus (%)", fontsize=13)
    ax.tick_params(axis="both", labelsize=13)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    definitions = {
        "Rural": "zone rurale — campagne, petites localités",
        "Semiurban": "zone semi-urbaine — villes moyennes, périphérie",
        "Urban": "zone urbaine — grandes villes"
    }
    patches = [mpatches.Patch(color=couleur, label=f"{z} : {definitions[z]}") for z, couleur in zip(zone.index, couleurs_zones)]
    ax.legend(handles=patches, loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=11)
    plt.tight_layout()
    st.pyplot(fig)

# ============ Slide 4 ============
with tab4:
    st.subheader("Le niveau d'éducation influence-t-il la décision, et est-ce un biais à surveiller ?")
    st.caption("KPI 6 — Taux de refus par Education")

    fig, ax = plt.subplots(figsize=(6,3.5))
    edu = charger("graph_education.csv")
    noms_fr = {"Graduate": "Diplômé", "Not Graduate": "Non diplômé"}
    labels_fr = edu["Education"].map(noms_fr)
    barres = ax.bar(labels_fr, edu["TauxRefus%"], color=["#1E3A5F", "#D97706"], width=0.5)
    ax.bar_label(barres, fmt="%.1f%%", fontsize=11, fontweight="bold")
    ax.set_ylabel("Taux de refus (%)")
    ax.set_ylim(0, 60)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)

# ============ Slide 5 ============
with tab5:
    st.subheader("Quel modèle retenir pour automatiser une partie du scoring ?")
    st.caption("Tableau comparatif des 3 modèles")

    resultats = charger("model_results.csv")
    st.dataframe(resultats, hide_index=True)

    modeles = resultats["Modèle"].tolist()
    rappel = resultats["Rappel (N)"].values
    auc = resultats["ROC-AUC"].values
    metrics_cols = ["Accuracy", "Précision (N)", "Rappel (N)", "F1-Score (N)", "ROC-AUC"]

    fig = plt.figure(figsize=(28, 13))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2, polar=True)

    x = np.arange(len(modeles))
    largeur = 0.35
    b1 = ax1.bar(x - largeur/2, rappel, largeur, label="Rappel (N)", color="#D97706")
    b2 = ax1.bar(x + largeur/2, auc, largeur, label="ROC-AUC", color="#1E3A5F")
    ax1.bar_label(b1, fmt="%.2f", padding=4, fontsize=24, fontweight="bold")
    ax1.bar_label(b2, fmt="%.2f", padding=4, fontsize=24, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(modeles, fontsize=22)
    ax1.set_ylim(0, 1)
    ax1.set_ylabel("Score", fontsize=22)
    ax1.tick_params(axis="y", labelsize=19)
    for spine in ["top", "right"]:
        ax1.spines[spine].set_visible(False)
    ax1.grid(axis="y", color="#e1e0d9", linewidth=0.7, zorder=0)
    ax1.set_axisbelow(True)
    ax1.set_title("Rappel et ROC-AUC par modèle", fontsize=24, fontweight="bold", pad=20)
    ax1.legend(loc="upper left", frameon=False, fontsize=19)

    angles = np.linspace(0, 2 * np.pi, len(metrics_cols), endpoint=False).tolist()
    angles += angles[:1]
    couleurs_modeles = {"Régression Logistique": "#8CA6C9", "Arbre de Décision": "#D97706", "Random Forest": "#1E3A5F"}

    for _, row in resultats.iterrows():
        valeurs = row[metrics_cols].tolist()
        valeurs += valeurs[:1]
        ax2.plot(angles, valeurs, linewidth=4, label=row["Modèle"], color=couleurs_modeles[row["Modèle"]])
        ax2.fill(angles, valeurs, alpha=0.12, color=couleurs_modeles[row["Modèle"]])

    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(metrics_cols, fontsize=19)
    ax2.set_ylim(0, 1)
    ax2.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax2.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=13, color="#888")
    ax2.set_title("Vue d'ensemble sur les 5 métriques", fontsize=24, fontweight="bold", pad=35)
    ax2.legend(loc="upper right", bbox_to_anchor=(1.45, 1.15), frameon=False, fontsize=17)

    definitions_txt = (
        "Accuracy : % de dossiers bien classés au total (accordés + refusés)\n"
        "Précision (N) : quand le modèle prédit \"refusé\", part de fois où c'est vraiment le cas\n"
        "Rappel (N) : part des dossiers réellement à risque que le modèle parvient à détecter\n"
        "F1-Score (N) : équilibre entre Précision et Rappel sur la classe refus, en une seule note\n"
        "ROC-AUC : capacité globale du modèle à distinguer un dossier à risque d'un dossier sain"
    )
    fig.text(0.72, 0.02, definitions_txt, ha="center", va="bottom", fontsize=16, color="#333333",
              bbox=dict(boxstyle="round,pad=0.8", facecolor="#f9f9f7", edgecolor="#c3c2b7", linewidth=0.8), linespacing=1.9)

    plt.subplots_adjust(bottom=0.28, wspace=0.35)
    st.pyplot(fig)

    st.success("**Modèle retenu : Random Forest** — meilleur Rappel (65,8 %).")

# ============ Slide 6 — Simulateur ============
with tab6:
    st.subheader("Simulateur de scoring")
    st.caption("Renseignez le profil d'un demandeur pour estimer le risque de refus")

    modele = joblib.load("modele_final.joblib")
    scaler = joblib.load("scaler.joblib")
    colonnes_modele = joblib.load("colonnes_modele.joblib")

    with st.form("simulateur"):
        colf1, colf2, colf3 = st.columns(3)
        with colf1:
            gender = st.selectbox("Genre", ["Male", "Female"])
            married = st.selectbox("Marié(e)", ["Yes", "No"])
            dependents = st.selectbox("Personnes à charge", ["0", "1", "2", "3+"])
        with colf2:
            education = st.selectbox("Diplôme", ["Graduate", "Not Graduate"])
            self_employed = st.selectbox("Indépendant", ["No", "Yes"])
            property_area = st.selectbox("Zone géographique", ["Urban", "Semiurban", "Rural"])
        with colf3:
            credit_history = st.selectbox("Historique de crédit", ["Bon", "Mauvais"])
            applicant_income = st.number_input("Revenu du demandeur", min_value=0, value=4000)
            coapplicant_income = st.number_input("Revenu du co-demandeur", min_value=0, value=0)

        loan_amount = st.number_input("Montant du prêt", min_value=0, value=120)
        loan_term = st.number_input("Durée du prêt (mois)", min_value=0, value=360)

        submit = st.form_submit_button("Estimer le risque")

    if submit:
        profil = pd.DataFrame([{
            "ApplicantIncome": applicant_income,
            "CoapplicantIncome": coapplicant_income,
            "LoanAmount": loan_amount,
            "Loan_Amount_Term": loan_term,
            "Credit_History": 1.0 if credit_history == "Bon" else 0.0,
            "Gender_encoded": 1 if gender == "Male" else 0,
            "Married_encoded": 1 if married == "Yes" else 0,
            "Education_encoded": 1 if education == "Not Graduate" else 0,
            "Self_Employed_encoded": 1 if self_employed == "Yes" else 0,
            "Dependents_1": 1 if dependents == "1" else 0,
            "Dependents_2": 1 if dependents == "2" else 0,
            "Dependents_3+": 1 if dependents == "3+" else 0,
            "Property_Area_Semiurban": 1 if property_area == "Semiurban" else 0,
            "Property_Area_Urban": 1 if property_area == "Urban" else 0,
        }])

        profil = profil.reindex(columns=colonnes_modele, fill_value=0)

        cols_num = ["ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term"]
        profil[cols_num] = scaler.transform(profil[cols_num])

        proba_risque = modele.predict_proba(profil)[0][0]
        decision = "REFUSÉ" if proba_risque >= 0.5 else "ACCORDÉ"

        st.divider()
        cola, colb = st.columns(2)
        with cola:
            st.metric("Probabilité de risque", f"{proba_risque*100:.1f} %")
        with colb:
            if decision == "REFUSÉ":
                st.error(f"Décision suggérée : {decision}")
            else:
                st.success(f"Décision suggérée : {decision}")