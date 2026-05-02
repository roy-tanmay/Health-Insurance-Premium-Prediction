import streamlit as st
from prediction import predicting_premium

# Initial Structure
st.set_page_config(page_title="Health Premium Predictor", page_icon="🏥", layout="centered")
st.title("🏥 Health Insurance Premium Predictor ")
st.markdown("### Your Health Is Our Priority")
st.write("Live each day like you have a significantly better health insurance plan.")

# Main Structure
name = st.text_input("Enter your name").title()
if name:
    st.success(f"Hello, {name} Please fill in the details below to estimate your annual health insurance premium ")
st.divider()

st.write("Please provide the necessary details below.")

# Configuring columns
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age",min_value= 1, max_value=100, value=25)
    number_of_dependants = st.number_input("Number of Dependents", min_value= 0, max_value=20, value=0)
    income_lakhs = st.number_input("Annual Income (In Lakhs ₹)",min_value= 0.0, max_value=200.0,step=0.5, value=0.0)
    genetical_risk = st.number_input("Genetical Risk(0-5)",min_value= 0, max_value=5, value=0)
    if age < 25:
        st.caption(
            "0 = No risk,  1–2 = Low,  3 = Moderate,  4–5 = High. Based on family history of hereditary conditions."
        )

with col2:
    gender = st.selectbox("Gender", ['Male','Female'],index=None, placeholder="Select option")
    marital_status =st.selectbox("Marital Status",['Unmarried', 'Married'],index=None, placeholder="Select option")
    employment_status =st.selectbox("Employment Status", ['Salaried', 'Self-Employed', 'Freelancer'],index=None,  placeholder="Select option")
    bmi_category = st.selectbox("BMI Category", ['Normal','Obesity', 'Overweight', 'Underweight'],index=None ,  placeholder="Select option")


with col3:
    region = st.selectbox("Region",["Northwest", "Southeast", "Northeast", "Southwest"],index=None, placeholder="Select option")
    smoking_status = st.selectbox("Smoking Status", ["No Smoking", "Regular", "Occasional"],index=None, placeholder="Select option")
    medical_history = st.selectbox("Medical History", [
                                "No Disease", "Diabetes", "High blood pressure",
                                "Diabetes & High blood pressure", "Thyroid", "Heart disease",
                                "High blood pressure & Heart disease", "Diabetes & Thyroid",
                                "Diabetes & Heart disease"],index=None, placeholder="Select option")
    insurance_plan = st.selectbox("Insurance Plan", ["Bronze", "Silver", "Gold"],index=None, placeholder="Select option")

st.divider()

# Prediction Button
if st.button("Predict Premium", width="stretch", type="primary"):
    user_data = {
        "age": age,
        "number_of_dependants": number_of_dependants,
        "income_lakhs": income_lakhs,
        "genetical_risk": genetical_risk,
        "medical_history": medical_history,
        "gender": gender,
        "marital_status": marital_status,
        "bmi_category": bmi_category,
        "smoking_status": smoking_status,
        "employment_status": employment_status,
        "region": region,
        "insurance_plan": insurance_plan
    }

    with st.spinner("predicting ..."):
        result = predicting_premium(user_data)
    st.success(f"💰 Estimated Annual Premium: ₹{result:,.0f}")

    with st.sidebar:
        st.write(' ## Your Submitted Details 📃\n_____________________ ')

        for k, v in user_data.items():
            if k == "normalized_risk_score":
                continue
            st.write(f"**{k.replace('_', ' ').title()}:** `{v}`")