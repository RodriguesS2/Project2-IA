import os
import streamlit as st
from src.inputs import collect_inputs
from src.features import engineer_features
from src.model import load_bundle, scale_and_predict, get_importances
from src import ui

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Health Risk Predictor",
    layout="wide",
    initial_sidebar_state="expanded",
)
ui.inject_css()

#load the trained model
bundle = load_bundle(BASE_DIR)

#sidebar form
inputs, predict_clicked = collect_inputs()

st.markdown("# Health Risk Predictor")
st.markdown(
    "A machine-learning proof-of-concept estimating **diabetes** and "
    "**hypertension** risk from demographics, lab results and lifestyle."
)

if bundle is None:
    st.warning(
        "No trained model found at `model/models.pkl`. "
        "Run the export cell in `model_building.ipynb` to create it."
    )

#results and more info (TODO: see if we need to add something)
def show_results():
    df_features = engineer_features(inputs)
    prob_diab, prob_hyp, _ = scale_and_predict(bundle, df_features)

    diab_name = bundle.get("diabetes_name", "")
    hyp_name = bundle.get("hypertension_name", "")
    diab_metrics = bundle.get("diabetes_metrics")
    hyp_metrics = bundle.get("hypertension_metrics")

    st.markdown('<div class="section-header">Risk Scores</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        ui.render_risk_card("Diabetes Risk", prob_diab, diab_name)
    with c2:
        ui.render_risk_card("Hypertension Risk", prob_hyp, hyp_name)

    if diab_metrics or hyp_metrics:
        st.markdown('<div class="section-header">Model Performance (Test Set)</div>',
                    unsafe_allow_html=True)
        m1, m2 = st.columns(2)
            
  
    ui.render_clinical_advice(prob_diab, prob_hyp)


def show_landing():
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("Best Model", bundle.get("diabetes_name", "-") if bundle else "-")
    c2.metric("Model Status", "Loaded" if bundle else "Not Loaded")

    st.markdown(
        """
        ### How it works
        1. **Fill the sidebar form** - choose sliders or type the values directly.
        2. **Press Predict** - the app feeds your 15 inputs into both
           classifiers.
        3. **Read the scores** - each condition gets a probability and a risk band.
        4. **Feature importance** shows which inputs pushed the prediction.

        ### Risk tiers
        | Probability | Tier |
        |---|---|
        | < 30% | Very Low |
        | 30 - 50% | Low - Moderate |
        | 50 - 70% | Moderate - High |
        | 70 - 85% | High |
        | > 85% | Very High |
        """
    )


# Decide what to render. We only predict when a model is loaded.
if predict_clicked and bundle is not None:
    show_results()

elif predict_clicked and bundle is None:
    st.info("Load the model first (see the warning above), then press Predict again.")

else:
    show_landing()