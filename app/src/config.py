NUMERIC_FEATURES = [
    "age", "bmi", "systolic_pressure", "diastolic_pressure",
    "glucose", "hba1c", "cholesterol", "hdl_cholesterol",
    "ldl_cholesterol", "triglycerides",
]

ALL_FEATURES = [
    "age", "sex", "bmi", "systolic_pressure", "diastolic_pressure",
    "glucose", "hba1c", "cholesterol", "hdl_cholesterol",
    "ldl_cholesterol", "triglycerides", "smoking",
    "physical_activity", "family_history_diabetes", "family_history_hypertension",
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
}

MODEL_PATH = "model/models.pkl"