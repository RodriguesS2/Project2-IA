import os
import joblib
import streamlit as st
import numpy 

MODEL_PATH = os.path.join("model", "models.pkl")

NUMERIC_FEATURES = [
    'age', 'bmi', 'systolic_pressure', 'diastolic_pressure',
    'glucose', 'hba1c', 'cholesterol', 'hdl_cholesterol',
    'ldl_cholesterol', 'triglycerides'
]

#load the trained bundle (.pkl file)
def load_bundle(base_dir: str):
    path = os.path.join(base_dir, MODEL_PATH)
    
    if not os.path.exists(path):
        return None
    try:
        return joblib.load(path)
    
    except Exception as e:
        st.error(f"Failed to load the model: {type(e).__name__}: {e}")
        return None


#scale the user data and give that data to tge model
def scale_and_predict(bundle, df_features):
    df_scaled = df_features.copy()
    df_scaled[NUMERIC_FEATURES] = bundle["scaler"].transform(df_features[NUMERIC_FEATURES])

    prob_diabetes = bundle["diabetes"].predict_proba(df_scaled)[0][1]
    prob_hypertension = bundle["hypertension"].predict_proba(df_scaled)[0][1]
    return prob_diabetes, prob_hypertension, df_scaled

