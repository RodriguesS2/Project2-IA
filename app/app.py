import os
import pandas as pd
import streamlit as st
import ui
from model import load_bundle, scale_and_predict

NUMERIC_FEATURES = [
    'age', 'bmi', 'systolic_pressure', 'diastolic_pressure',
    'glucose', 'hba1c', 'cholesterol', 'hdl_cholesterol',
    'ldl_cholesterol', 'triglycerides'
]

ALL_FEATURES = [
    'age', 'sex', 'bmi', 'systolic_pressure', 'diastolic_pressure',
    'glucose', 'hba1c', 'cholesterol', 'hdl_cholesterol',
    'ldl_cholesterol', 'triglycerides', 'smoking',
    'physical_activity', 'family_history_diabetes', 'family_history_hypertension'
]

PHYS_OPTIONS = {
    "0 days": 0, "1 day": 1, "2 days": 2, "3 days": 3,
    "4 days": 4, "5 days": 5, "6 days": 6, "7 days": 7,
}

YES_NO = {"No": 0, "Yes": 1}
SEX = {"Female": 0, "Male": 1}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#forms to collect the inputs
def collect_inputs():
    st.subheader("Personal Info")
    sex_label = st.radio("Sex", list(SEX.keys()), horizontal=True)
    age = st.number_input("Age (years) (18–90)", 18, 90, 45, 1)
    st.divider()

    st.subheader("Body/Blood Metrics")
    bmi = st.number_input("BMI (kg/m²) (15–50)", 15.0, 50.0, 26.0, 0.1)
    systolic = st.number_input("Systolic blood pressure (mmHg) (80–200)", 80, 200, 120, 1)
    diastolic = st.number_input("Diastolic blood pressure (mmHg) (50–120)", 50, 120, 80, 1)
    glucose = st.number_input("Glucose (mg/dL) (50–300)", 50, 300, 100, 1)
    hba1c = st.number_input("HbA1c (%) (4.0–15.0)", 4.0, 15.0, 5.5, 0.1)
    cholesterol = st.number_input("Cholesterol (mg/dL) (100–400)", 100, 400, 200, 1)
    hdl_cholesterol = st.number_input("HDL Cholesterol (mg/dL) (20–100)", 20, 100, 50, 1)
    ldl_cholesterol = st.number_input("LDL Cholesterol (mg/dL) (50–250)", 50, 250, 100, 1)
    triglycerides = st.number_input("Triglycerides (mg/dL) (50–400)", 50, 400, 150, 1)
    st.divider()

    st.subheader("Lifestyle")
    smoking_label = st.radio("Current smoker", list(YES_NO.keys()), horizontal=True)
    phys_label = st.selectbox("Physical activity (0–7)", list(PHYS_OPTIONS.keys()), index=2)
    st.divider()

    st.subheader("Family History")
    fam_diabetes_label = st.radio("Diabetes in family", list(YES_NO.keys()), horizontal=True)
    fam_hypertension_label = st.radio("Hypertension in family", list(YES_NO.keys()), horizontal=True)

    st.markdown("")
    predict = st.button("Assess Risk", use_container_width=True)

    #stores the input
    inputs = {
        "age": float(age),
        "sex": SEX[sex_label],
        "bmi": float(bmi),
        "systolic_pressure": float(systolic),
        "diastolic_pressure": float(diastolic),
        "glucose": float(glucose),
        "hba1c": float(hba1c),
        "cholesterol": float(cholesterol),
        "hdl_cholesterol": float(hdl_cholesterol),
        "ldl_cholesterol": float(ldl_cholesterol),
        "triglycerides": float(triglycerides),
        "smoking": YES_NO[smoking_label],
        "physical_activity": PHYS_OPTIONS[phys_label],
        "family_history_diabetes": YES_NO[fam_diabetes_label],
        "family_history_hypertension": YES_NO[fam_hypertension_label]
    }
    
    return inputs, predict


#prepare the user data to give to the model used
def prepare_features(inputs):
    df = pd.DataFrame([dict(inputs)])
    return df[ALL_FEATURES]

st.set_page_config(
    page_title="Diabetes and Hypertension Prediction",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#load the bundle/model used
bundle = load_bundle(BASE_DIR)

ui.render_header()

if bundle is None:
    st.warning(
        "No trained model found at `model/models.pkl`. "
        "Run the export cell in `model_building.ipynb` to create it."
    )

#divide the main page in left and right
left, right = st.columns([1, 1.25], gap="large")

#right, user inputs
with right:
    inputs, predict_clicked = collect_inputs()

#left info and results
with left:
    ui.render_table()

    if predict_clicked and bundle is not None:
        df_features = prepare_features(inputs)
        prob_diabetes, prob_hypertension, _ = scale_and_predict(bundle, df_features)

        st.divider() 
        st.subheader("Assessment Result")
        
        ui.render_risk_card("Diabetes risk", prob_diabetes)
        ui.render_risk_card("Hypertension risk", prob_hypertension)
        ui.render_clinical_advice(prob_diabetes, prob_hypertension)