import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Choix du modèle")

@st.cache_data
def charger(fichier):
    return pd.read_csv(fichier)

st.subheader("Quel modèle retenir pour automatiser une partie du scoring ?")
st.caption("Comparaison des modèles de classification")

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

definitions_txt = "Accuracy : % de dossiers bien classés au total (accordés + refusés)\nPrécision (N) : quand le modèle prédit refusé, part de fois où c'est vraiment le cas\nRappel (N) : part des dossiers réellement à risque que le modèle parvient à détecter\nF1-Score (N) : équilibre entre Précision et Rappel sur la classe refus, en une seule note\nROC-AUC : capacité globale du modèle à distinguer un dossier à risque d'un dossier sain"
fig.text(0.72, 0.02, definitions_txt, ha="center", va="bottom", fontsize=16, color="#333333", bbox=dict(boxstyle="round,pad=0.8", facecolor="#f9f9f7", edgecolor="#c3c2b7", linewidth=0.8), linespacing=1.9)

plt.subplots_adjust(bottom=0.28, wspace=0.35)
st.pyplot(fig)

st.success("**Modèle retenu : Random Forest** — meilleur Rappel (65,8 %).")

st.divider()
st.subheader("Quelles sont les limites du modèle retenu, à assumer honnêtement ?")
st.caption("Matrice de confusion du modèle final (Random Forest)")

conf = charger("confusion.csv").iloc[0]
tn = conf["tn"]
fp = conf["fp"]
fn = conf["fn"]
tp = conf["tp"]
total = tn + fp + fn + tp

couleur_accord_ok = "#1F4E79"
couleur_refus_injuste = "#898781"
couleur_alerte = "#E8A33D"
couleur_refus_ok = "#2a78d6"

fig2, ax3 = plt.subplots(figsize=(9, 7.5))
grille_couleurs = [[couleur_accord_ok, couleur_refus_injuste], [couleur_alerte, couleur_refus_ok]]
texte_00 = "Accord Légitime\n\n" + str(tp) + " clients\n(" + str(round(tp/total*100, 1)) + "%)"
texte_01 = "Refus Injustifié\n(Manque à gagner)\n\n" + str(fn) + " clients\n(" + str(round(fn/total*100, 1)) + "%)"
texte_10 = "Accorde a tort\n(Client a risque)\n\n" + str(fp) + " clients\n(" + str(round(fp/total*100, 1)) + "%)"
texte_11 = "Refus Justifie\n(Risque evite)\n\n" + str(tn) + " clients\n(" + str(round(tn/total*100, 1)) + "%)"
grille_texte = [[texte_00, texte_01], [texte_10, texte_11]]

for i in range(2):
    for j in range(2):
        ax3.add_patch(plt.Rectangle((j, 1 - i), 1, 1, facecolor=grille_couleurs[i][j], edgecolor="white", linewidth=3))
        ax3.text(j + 0.5, 1 - i + 0.5, grille_texte[i][j], ha="center", va="center", fontsize=13, fontweight="bold", color="white")

ax3.set_xlim(0, 2)
ax3.set_ylim(0, 2)
ax3.set_xticks([0.5, 1.5])
ax3.set_xticklabels(["Predit : Accorde", "Predit : Refuse"], fontsize=11)
ax3.set_yticks([0.5, 1.5])
ax3.set_yticklabels(["Realite : MAUVAIS PAYEUR (N)", "Realite : BON PAYEUR (Y)"], fontsize=11)
ax3.tick_params(length=0)
for spine in ax3.spines.values():
    spine.set_visible(False)
st.pyplot(fig2)

message_alerte = str(int(fp)) + " clients a risque sont accordes a tort (" + str(round(fp/total*100, 1)) + "%) - le vrai danger financier pour la banque, sur " + str(int(total)) + " dossiers de test."
st.warning(message_alerte)