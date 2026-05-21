# features.py
import pandas
from .config import ALL_FEATURES

def create_fluid_medical_features(df_input):
    df = df_input.copy()
    
    # Recriar as fórmulas contínuas do Jupyter Notebook
    df['glucose_cholesterol_index'] = (df['glucose'] * df['cholesterol']) / 1000
    df['mean_arterial_pressure'] = (df['systolic_pressure'] + 2 * df['diastolic_pressure']) / 3
    df['chol_hdl_ratio'] = df['cholesterol'] / (df['hdl_cholesterol'] + 1)
    df['bmi_sedentary_index'] = df['bmi'] * (8 - df['physical_activity'])
    df['smoking_bp_interaction'] = df['systolic_pressure'] * df['smoking']
    
    return df

def engineer_features(inputs):
    # Transforma as inputs do Streamlit num DataFrame
    df = pandas.DataFrame([dict(inputs)])
    
    # Cria as variáveis novas
    df = create_fluid_medical_features(df)
    
    # Devolve o DataFrame com as colunas na ordem exata exigida pelo modelo
    return df[ALL_FEATURES]