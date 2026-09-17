import streamlit as st
import pandas as pd
import joblib

st.title("Simulateur de scoring")
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