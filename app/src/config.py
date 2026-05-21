# config.py

NUMERIC_FEATURES = [
    'age', 'bmi', 'systolic_pressure', 'diastolic_pressure',
    'glucose', 'hba1c', 'cholesterol', 'hdl_cholesterol',
    'ldl_cholesterol', 'triglycerides',
    # --- As 5 novas variáveis contínuas ---
    'glucose_cholesterol_index', 'mean_arterial_pressure', 
    'chol_hdl_ratio', 'bmi_sedentary_index', 'smoking_bp_interaction'
]

ALL_FEATURES = [
    'age', 'sex', 'bmi', 'systolic_pressure', 'diastolic_pressure',
    'glucose', 'hba1c', 'cholesterol', 'hdl_cholesterol',
    'ldl_cholesterol', 'triglycerides', 'smoking',
    'physical_activity', 'family_history_diabetes', 'family_history_hypertension',
    # --- As 5 novas variáveis contínuas ---
    'glucose_cholesterol_index', 'mean_arterial_pressure', 
    'chol_hdl_ratio', 'bmi_sedentary_index', 'smoking_bp_interaction'
]

FEATURE_LABELS = {
    "age": "Age",
    "sex": "Sex",
    "bmi": "BMI",
    "systolic_pressure": "Systolic Pressure",
    "diastolic_pressure": "Diastolic Pressure",
    "glucose": "Glucose",
    "hba1c": "HbA1c",
    "cholesterol": "Cholesterol",
    "hdl_cholesterol": "HDL Cholesterol",
    "ldl_cholesterol": "LDL Cholesterol",
    "triglycerides": "Triglycerides",
    "smoking": "Smoking",
    "physical_activity": "Physical Activity",
    "family_history_diabetes": "Family Diabetes",
    "family_history_hypertension": "Family Hypertension",
    "glucose_cholesterol_index": "Glucose-Cholesterol Index",
    "mean_arterial_pressure": "Mean Arterial Pressure",
    "chol_hdl_ratio": "Cholesterol/HDL Ratio",
    "bmi_sedentary_index": "BMI-Sedentary Index",
    "smoking_bp_interaction": "Smoking-BP Interaction"
}

MODEL_PATH = "model/models.pkl"