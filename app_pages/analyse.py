import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.title("Analyse du risque de crédit")

@st.cache_data
def charger(fichier):
    return pd.read_csv(fichier)

kpis = charger("kpis.csv").iloc[0]

tab1, tab2, tab3, tab4 = st.tabs([
    "Ampleur du risque",
    "Historique de crédit",
    "Zone géographique",
    "Diplôme",
])

with tab1:
    st.subheader("Quelle est l'ampleur du risque de refus chez CrediTrust aujourd'hui ?")
    st.caption("Taux de refus global, nombre de dossiers")

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
        ax.text(barre.get_x() + barre.get_width()/2, barre.get_height() + 10, f"{valeur}\n({pct}%)", ha="center", va="bottom", fontsize=12, fontweight="bold", bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=couleur))
    ax.set_ylabel("Nombre de dossiers")
    ax.set_ylim(0, max(valeurs) * 1.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig)

with tab2:
    st.subheader("L'historique de crédit doit-il rester le critère prioritaire dans la décision d'octroi ?")
    st.caption("Taux de refus par historique de crédit")

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

with tab3:
    st.subheader("Existe-t-il une inégalité géographique dans l'octroi de crédit ?")
    st.caption("Taux de refus par zone géographique")

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

    definitions = {"Rural": "zone rurale — campagne, petites localités", "Semiurban": "zone semi-urbaine — villes moyennes, périphérie", "Urban": "zone urbaine — grandes villes"}
    patches = [mpatches.Patch(color=couleur, label=f"{z} : {definitions[z]}") for z, couleur in zip(zone.index, couleurs_zones)]
    ax.legend(handles=patches, loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=11)
    plt.tight_layout()
    st.pyplot(fig)

with tab4:
    st.subheader("Le niveau d'éducation influence-t-il la décision, et est-ce un biais à surveiller ?")
    st.caption("Taux de refus par niveau d'éducation")

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