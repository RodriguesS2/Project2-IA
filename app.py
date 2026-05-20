import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os

#  Page config

st.set_page_config(
    page_title="Health Risk Predictor",
    layout="wide",
    initial_sidebar_state="expanded",
)

#  Custom CSS

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'DM Serif Display', serif; }
    .stApp { background-color: #1a1a2e; }
    .main .block-container { background-color: #1a1a2e; }

    section[data-testid="stSidebar"] { background-color: #1a1a2e; color: white; }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p { color: #e0e0e0 !important; }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #ffffff !important; }

    .section-header {
        font-family: 'DM Serif Display', serif;
        font-size: 1.1rem; color: #1a1a2e;
        border-bottom: 2px solid #1a1a2e;
        padding-bottom: 4px; margin-top: 1.5rem; margin-bottom: 1rem;
    }

    .risk-card { border-radius: 12px; padding: 28px 24px; text-align: center; margin-bottom: 1rem; }
    .risk-vlow    { background: #d4edda; border-left: 6px solid #28a745; }
    .risk-low     { background: #e8f5e9; border-left: 6px solid #66bb6a; }
    .risk-medium  { background: #fff3cd; border-left: 6px solid #ffc107; }
    .risk-high    { background: #ffe0b2; border-left: 6px solid #ff9800; }
    .risk-vhigh   { background: #f8d7da; border-left: 6px solid #dc3545; }

    .risk-label { font-size: 0.85rem; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600; color: #555; margin-bottom: 4px; }
    .risk-score { font-family: 'DM Serif Display', serif; font-size: 3.2rem; font-weight: 700; line-height: 1; margin-bottom: 6px; }
    .risk-badge { display: inline-block; padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }
    .badge-vlow   { background: #28a745; color: white; }
    .badge-low    { background: #66bb6a; color: white; }
    .badge-medium { background: #ffc107; color: #333; }
    .badge-high   { background: #ff9800; color: white; }
    .badge-vhigh  { background: #dc3545; color: white; }

    .feat-row { display: flex; align-items: center; margin-bottom: 10px; gap: 10px; }
    .feat-name { width: 200px; font-size: 0.82rem; color: #444; text-align: right; flex-shrink: 0; }
    .feat-bar-wrap { flex: 1; background: #e8e6e0; border-radius: 4px; height: 10px; overflow: hidden; }
    .feat-bar-fill { height: 100%; border-radius: 4px; }
    .feat-val { font-size: 0.78rem; color: #666; width: 42px; flex-shrink: 0; }

    .model-badge {
        display: inline-block; background: #1a1a2e; color: white;
        padding: 3px 12px; border-radius: 20px; font-size: 0.75rem;
        font-weight: 600; letter-spacing: 0.06em; margin-left: 8px;
    }

    .disclaimer {
        background: #fff8e6; border: 1px solid #ffe08a; border-radius: 8px;
        padding: 12px 16px; font-size: 0.8rem; color: #7a6000; margin-top: 1.5rem;
    }

    div[data-testid="stButton"] > button {
        background-color: #1a1a2e; color: white; border: none;
        border-radius: 8px; padding: 0.65rem 2.2rem;
        font-family: 'DM Sans', sans-serif; font-weight: 600;
        font-size: 1rem; letter-spacing: 0.04em; width: 100%; transition: opacity 0.2s;
    }
    div[data-testid="stButton"] > button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

#  Model loader (cached)

@st.cache_resource
def load_models():
    """
    Expects model/models.pkl saved by the export cell in model_building.ipynb with structure:
    {
      'scaler':              fitted StandardScaler,
      'diabetes':            fitted best diabetes classifier,
      'hypertension':        fitted best hypertension classifier,
      'diabetes_name':       str  (e.g. 'Logistic Regression'),
      'hypertension_name':   str,
      'diabetes_metrics':    dict  (auc, f1, recall, precision),
      'hypertension_metrics':dict,
    }
    """
    model_path = os.path.join(os.path.dirname(__file__), "model", "models.pkl")
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)


#  Feature engineering 

NUMERIC_FEATURES = [
    'age', 'bmi', 'systolic_pressure', 'glucose', 'cholesterol',
    'bmi_smoking', 'age_family_diabetes', 'age_family_hypertension',
    'glucose_cholesterol', 'bmi_physical'
]

ALL_FEATURES = [
    'age', 'bmi', 'systolic_pressure', 'glucose', 'cholesterol',
    'smoking', 'physical_activity', 'family_history_diabetes', 'family_history_hypertension',
    # interaction
    'bmi_smoking', 'age_family_diabetes', 'age_family_hypertension',
    'glucose_cholesterol', 'bmi_physical',
    # binary categorical
    'bmi_obese', 'bp_high', 'glucose_high', 'cholesterol_high', 'age_senior'
]

FEATURE_LABELS = {
    'age':                         'Age',
    'bmi':                         'BMI',
    'systolic_pressure':           'Systolic Pressure',
    'glucose':                     'Glucose',
    'cholesterol':                 'Cholesterol',
    'smoking':                     'Smoking',
    'physical_activity':           'Physical Activity',
    'family_history_diabetes':     'Family Hx  Diabetes',
    'family_history_hypertension': 'Family Hx  Hypertension',
    'bmi_smoking':                 'BMI  Smoking',
    'age_family_diabetes':         'Age  Fam. Diabetes',
    'age_family_hypertension':     'Age  Fam. Hypert.',
    'glucose_cholesterol':         'Glucose  Cholesterol',
    'bmi_physical':                'BMI  Physical Activity',
    'bmi_obese':                   'Obese (BMI ≥ 30)',
    'bp_high':                     'High BP (≥ 130)',
    'glucose_high':                'High Glucose (≥ 100)',
    'cholesterol_high':            'High Cholesterol (≥ 200)',
    'age_senior':                  'Senior (≥ 60)',
}


def engineer_features(inputs: dict) -> pd.DataFrame:
    d = inputs.copy()
    d['bmi_smoking']              = d['bmi'] * d['smoking']
    d['age_family_diabetes']      = d['age'] * d['family_history_diabetes']
    d['age_family_hypertension']  = d['age'] * d['family_history_hypertension']
    d['glucose_cholesterol']      = d['glucose'] * d['cholesterol'] / 1000
    d['bmi_physical']             = d['bmi'] * (2 - d['physical_activity'])
    d['bmi_obese']                = int(d['bmi'] >= 30)
    d['bp_high']                  = int(d['systolic_pressure'] >= 130)
    d['glucose_high']             = int(d['glucose'] >= 100)
    d['cholesterol_high']         = int(d['cholesterol'] >= 200)
    d['age_senior']               = int(d['age'] >= 60)
    return pd.DataFrame([d])[ALL_FEATURES]


def scale_and_predict(bundle, df_features: pd.DataFrame):
    df_scaled = df_features.copy()
    df_scaled[NUMERIC_FEATURES] = bundle['scaler'].transform(df_features[NUMERIC_FEATURES])
    prob_diab = bundle['diabetes'].predict_proba(df_scaled)[0][1]
    prob_hyp  = bundle['hypertension'].predict_proba(df_scaled)[0][1]
    return prob_diab, prob_hyp, df_scaled


#  Risk tier - 4-band scale 

def risk_tier(prob: float):
    if prob < 0.30:
        return "Very Low",         "vlow"
    elif prob < 0.50:
        return "Low Moderate",   "low"
    elif prob < 0.70:
        return "Moderate High",  "medium"
    elif prob < 0.85:
        return "High",             "high"
    else:
        return "Very High",        "vhigh"


#  Feature importance (handles LR / tree / SVM-KNN via permutation)

def get_importances(bundle, df_scaled: pd.DataFrame, target: str) -> dict | None:
    model = bundle[target]
    model_name = bundle.get(f'{target}_name', '')

    if hasattr(model, 'coef_'):                        # Logistic Regression
        vals = np.abs(model.coef_[0])
    elif hasattr(model, 'feature_importances_'):       # RF / DT
        vals = model.feature_importances_
    else:
        return None   # SVM / KNN — permutation needs test set; skip at inference time

    if vals.sum() > 0:
        vals = vals / vals.sum()
    return dict(zip(ALL_FEATURES, vals))


def render_importance_bars(importances: dict, top_n: int = 10):
    sorted_items = sorted(importances.items(), key=lambda x: -x[1])[:top_n]
    rows_html = ""
    for feat, val in sorted_items:
        pct   = round(val * 100, 1)
        label = FEATURE_LABELS.get(feat, feat)
        fill  = int(min(val * 400, 100))   # scale bar width
        color = "#1a1a2e" if pct > 12 else "#5c6bc0" if pct > 6 else "#aab0d4"
        rows_html += f"""
        <div class="feat-row">
            <span class="feat-name">{label}</span>
            <div class="feat-bar-wrap">
                <div class="feat-bar-fill" style="width:{fill}%; background:{color};"></div>
            </div>
            <span class="feat-val">{pct}%</span>
        </div>"""
    st.markdown(rows_html, unsafe_allow_html=True)



#  Risk card

def render_risk_card(title: str, prob: float, model_name: str = ""):
    label, tier = risk_tier(prob)
    pct = int(prob * 100)
    badge_extra = f'<span class="model-badge">{model_name}</span>' if model_name else ""
    st.markdown(f"""
    <div class="risk-card risk-{tier}">
        <div class="risk-label">{title}{badge_extra}</div>
        <div class="risk-score">{pct}%</div>
        <span class="risk-badge badge-{tier}">{label} Risk</span>
    </div>
    """, unsafe_allow_html=True)

#  Sidebar - input form

with st.sidebar:
    st.markdown("## Patient Information")
    st.markdown("Fill in the fields and press **Predict** to assess risk.")

    st.markdown("### Demographics")
    age = st.slider("Age (years)", min_value=18, max_value=90, value=45, step=1)
    # sex is in the dataset but not in the feature set -  shown for completeness
    sex = st.radio("Biological Sex", ["Female (0)", "Male (1)"], horizontal=True)

    st.markdown("### Body Metrics")
    bmi      = st.slider("BMI (kg/m²)",         min_value=15.0, max_value=50.0, value=26.0, step=0.1)
    systolic = st.slider("Systolic BP (mmHg)",  min_value=80,   max_value=200,  value=120,  step=1)

    st.markdown("### Lab Results")
    glucose     = st.slider("Fasting Glucose (mg/dL)", min_value=60,  max_value=300, value=90,  step=1)
    cholesterol = st.slider("Cholesterol (mg/dL)",     min_value=100, max_value=400, value=180, step=1)

    st.markdown("### Lifestyle")
    smoking = st.radio("Current Smoker", ["No (0)", "Yes (1)"], horizontal=True)
    # physical_activity goes from in the dataset (None / Moderate / Intense)
    phys_map = {"None (0)": 0, "Moderate (1)": 1, "Intense (2)": 2, "3":3, "4":4, "5":5, "6":6, "7":7}
    phys_label = st.selectbox("Physical Activity Level", list(phys_map.keys()), index=1)

    st.markdown("### Family History")
    fam_diabetes     = st.radio("Diabetes in family",     ["No (0)", "Yes (1)"], horizontal=True)
    fam_hypertension = st.radio("Hypertension in family", ["No (0)", "Yes (1)"], horizontal=True)

    st.markdown("---")
    predict_btn = st.button("🔍 Predict Risk", use_container_width=True)

#  Collect inputs (convert radio labels to numeric)

user_inputs = {
    'age':                         float(age),
    'bmi':                         float(bmi),
    'systolic_pressure':           float(systolic),
    'glucose':                     float(glucose),
    'cholesterol':                 float(cholesterol),
    'smoking':                     1 if "Yes" in smoking else 0,
    'physical_activity':           float(phys_map[phys_label]),
    'family_history_diabetes':     1 if "Yes" in fam_diabetes else 0,
    'family_history_hypertension': 1 if "Yes" in fam_hypertension else 0,
}

# Main content

st.markdown("# Health Risk Predictor")
st.markdown(
    "A machine-learning POC estimating **diabetes** and **hypertension** risk "
    "from patient demographics, lab results, and lifestyle data."
)

bundle = load_models()

if bundle is None:
    st.warning(
        "⚠️ No trained model found at `model/models.pkl`. "
        "Run the export cell in `Projects/Project2-IA/model_building.ipynb` to create the saved bundle."
    )

# Results 
if predict_btn:
    df_features = engineer_features(user_inputs)

    if bundle is None:
        # Heuristic placeholder (no model file) 
        st.info("📋 Showing heuristic placeholder — model not loaded yet.")
        prob_diab = min(0.95, max(0.05,
            0.015 * max(0, age - 40)
            + 0.04  * max(0, bmi - 25) / 5
            + 0.12  * max(0, glucose - 90) / 50
            + 0.15  * user_inputs['smoking']
            + 0.10  * user_inputs['family_history_diabetes']
            - 0.05  * (user_inputs['physical_activity'] / 2)
        ))
        prob_hyp = min(0.95, max(0.05,
            0.015 * max(0, age - 40)
            + 0.10  * max(0, systolic - 120) / 20
            + 0.06  * max(0, bmi - 25) / 5
            + 0.10  * user_inputs['family_history_hypertension']
            - 0.04  * (user_inputs['physical_activity'] / 2)
        ))
        df_scaled       = df_features  # unscaled, for debug only
        importances_diab = None
        importances_hyp  = None
        diab_model_name  = "Placeholder"
        hyp_model_name   = "Placeholder"
        diab_metrics     = None
        hyp_metrics      = None
    else:
        prob_diab, prob_hyp, df_scaled = scale_and_predict(bundle, df_features)
        importances_diab  = get_importances(bundle, df_scaled, 'diabetes')
        importances_hyp   = get_importances(bundle, df_scaled, 'hypertension')
        diab_model_name   = bundle.get('diabetes_name', '')
        hyp_model_name    = bundle.get('hypertension_name', '')
        diab_metrics      = bundle.get('diabetes_metrics')
        hyp_metrics       = bundle.get('hypertension_metrics')

    # Layout 
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-header">Risk Scores</div>', unsafe_allow_html=True)
        render_risk_card("Diabetes Risk",     prob_diab, diab_model_name)
        render_risk_card("Hypertension Risk", prob_hyp,  hyp_model_name)

        # Model performance metrics (if available from bundle)
        if diab_metrics or hyp_metrics:
            st.markdown('<div class="section-header">Model Performance (Test Set)</div>', unsafe_allow_html=True)
            mc1, mc2 = st.columns(2)
            if diab_metrics:
                with mc1:
                    st.caption("Diabetes Model")
                    st.metric("ROC-AUC",   f"{diab_metrics.get('auc', 0):.3f}")
                    st.metric("F1-Score",  f"{diab_metrics.get('f1', 0):.3f}")
            if hyp_metrics:
                with mc2:
                    st.caption("Hypertension Model")
                    st.metric("ROC-AUC",   f"{hyp_metrics.get('auc', 0):.3f}")
                    st.metric("F1-Score",  f"{hyp_metrics.get('f1', 0):.3f}")

    with col_right:
        st.markdown('<div class="section-header">Feature Importance</div>', unsafe_allow_html=True)
        tab_diab, tab_hyp = st.tabs(["Diabetes", "Hypertension"])

        with tab_diab:
            if importances_diab:
                render_importance_bars(importances_diab)
            elif diab_model_name in ('SVM', 'KNN'):
                st.caption(
                    f"Feature importance via permutation requires the test set "
                    f"and is not available at inference time for **{diab_model_name}**."
                )
            else:
                st.caption("Feature importance unavailable — model not loaded.")

        with tab_hyp:
            if importances_hyp:
                render_importance_bars(importances_hyp)
            elif hyp_model_name in ('SVM', 'KNN'):
                st.caption(
                    f"Feature importance via permutation requires the test set "
                    f"and is not available at inference time for **{hyp_model_name}**."
                )
            else:
                st.caption("Feature importance unavailable — model not loaded.")

    # Clinical advice (mirrors notebook summary logic) 
    diab_pred = int(prob_diab >= 0.5)
    hyp_pred  = int(prob_hyp  >= 0.5)

    st.markdown('<div class="section-header">Clinical Guidance</div>', unsafe_allow_html=True)
    if diab_pred and hyp_pred:
        st.error("High risk for **both** diabetes and hypertension. Consider consulting a healthcare provider and making comprehensive lifestyle changes.")
    elif diab_pred:
        st.warning("High risk for **diabetes**. Monitor blood sugar regularly, maintain healthy weight, increase activity and reduce sugar intake.")
    elif hyp_pred:
        st.warning("High risk for **hypertension**. Monitor blood pressure regularly, reduce sodium, consider stress management techniques.")
    else:
        st.success("Low risk for both conditions. Maintain a healthy lifestyle and continue regular check-ups.")

    st.markdown("""
    <div class="disclaimer">
        <strong>Disclaimer:</strong> This tool is a proof-of-concept trained on <em>synthetic data</em>.
        Results are not medically valid and should never replace professional clinical assessment.
    </div>
    """, unsafe_allow_html=True)

else:
    # Landing state 
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Features Used", "19")
    c2.metric("Conditions Assessed", "2")
    c3.metric("Best Model", "Logistic Regression" if bundle is None else bundle.get('diabetes_name', '—'))
    c4.metric("Model Status", "Not Loaded" if bundle is None else "Loaded")

    st.markdown("""
    ### How it works
    1. **Fill the form** in the sidebar with the patient's demographics, lab values, and lifestyle factors.
    2. **Press Predict** — the app engineers 10 interaction & categorical features on top of the 9 base inputs, then runs both classifiers.
    3. **Review scores** — each condition gets a probability and a 4-band risk tier (Very Low → Very High).
    4. **Feature importance** shows which inputs drove the prediction (for Logistic Regression: |coefficients|; for Random Forest / Decision Tree: Gini importance).

    ### Risk tiers
    | Probability | Tier |
    |---|---|
    | < 30% | Very Low |
    | 30 - 50% | Low - Moderate |
    | 50 - 70% | Moderate - High |
    | 70 - 85% | High |
    | > 85% | Very High |
    """)