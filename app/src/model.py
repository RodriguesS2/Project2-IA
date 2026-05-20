import os
import joblib
import streamlit as st
import numpy 
import pandas

from .config import NUMERIC_FEATURES, ALL_FEATURES, MODEL_PATH

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


def scale_and_predict(bundle, df_features):
    df_scaled = df_features.copy()
    df_scaled[NUMERIC_FEATURES] = bundle["scaler"].transform(df_features[NUMERIC_FEATURES])

    prob_diab = bundle["diabetes"].predict_proba(df_scaled)[0][1]
    prob_hyp = bundle["hypertension"].predict_proba(df_scaled)[0][1]
    return prob_diab, prob_hyp, df_scaled


def get_importances(bundle, target: str):
    """Return a {feature: weight} dict for the chart.

    - Logistic Regression: absolute coefficients.
    - Random Forest / Decision Tree: built-in importances.
    - SVM / KNN: no usable per-feature weight at predict time, so None.
    """
    model = bundle[target]

    if hasattr(model, "coef_"):                  # Logistic Regression
        vals = numpy.abs(model.coef_[0])
    elif hasattr(model, "feature_importances_"):  # tree-based models
        vals = model.feature_importances_
    else:
        return None

    # Normalise so the bars add up to 100%.
    total = vals.sum()
    if total > 0:
        vals = vals / total
    return dict(zip(ALL_FEATURES, vals))