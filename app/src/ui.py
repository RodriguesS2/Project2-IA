import streamlit as st
from .config import FEATURE_LABELS


CSS = """
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
        padding-bottom: 4px; margin-top: 1rem; margin-bottom: 0.8rem;
    }

    .risk-card {
        border-radius: 12px; padding: 28px 24px; text-align: center;
        margin-bottom: 1rem; min-height: 255px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .risk-vlow    { background: #d4edda;  }
    .risk-low     { background: #e8f5e9;  }
    .risk-medium  { background: #fff3cd;  }
    .risk-high    { background: #ffe0b2;  }
    .risk-vhigh   { background: #f8d7da;  }

    .risk-label { font-size: 0.85rem; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600; color: #555; margin-bottom: 4px; }
    .risk-score { font-family: 'DM Serif Display', serif; font-size: 3.2rem; font-weight: 700; line-height: 1; margin-bottom: 6px; color: #1a1a2e; }
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
        padding: 12px 16px; font-size: 0.8rem; color: #7a6000; margin-top: 1rem;
    }

    div[data-testid="stButton"] > button {
        background-color: #1a1a2e; color: white; border: none;
        border-radius: 8px; padding: 0.65rem 2.2rem;
        font-family: 'DM Sans', sans-serif; font-weight: 600;
        font-size: 1rem; letter-spacing: 0.04em; width: 100%; transition: opacity 0.2s;
    }
    div[data-testid="stButton"] > button:hover { opacity: 0.85; }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


#for output
def risk_tier(prob: float):
    if prob < 0.30:
        return "Very Low", "vlow"
    
    elif prob < 0.50:
        return "Low Moderate", "low"
    
    elif prob < 0.70:
        return "Moderate High", "medium"
    
    elif prob < 0.85:
        return "High", "high"
    
    else:
        return "Very High", "vhigh"


#risk output
def render_risk_card(title, prob, model_name):
    label, tier = risk_tier(prob)
    pct = int(round(prob * 100))
    badge = f'<span class="model-badge">{model_name}</span>' if model_name else ""
    
    st.markdown(
        f"""
        <div class="risk-card risk-{tier}">
            <div class="risk-label">{title}{badge}</div>
            <div class="risk-score">{pct}%</div>
            <span class="risk-badge badge-{tier}">{label} Risk</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_clinical_advice(prob_diab: float, prob_hyp: float):
    diab = prob_diab >= 0.5
    hyp = prob_hyp >= 0.5

    st.markdown('<div class="section-header">Clinical Guidance</div>', unsafe_allow_html=True)
    
    if diab and hyp:
        st.error("High risk for **both** diabetes and hypertension. Consider seeing a "
                 "healthcare provider and making broad lifestyle changes.")
    
    elif diab:
        st.warning("High risk for **diabetes**. Monitor blood sugar, keep a healthy weight, "
                   "move more and cut back on sugar.")
    
    elif hyp:
        st.warning("High risk for **hypertension**. Monitor blood pressure, reduce sodium, "
                   "and look at stress management.")
    
    else:
        st.success("Low risk for both conditions. Keep up the healthy habits and regular check-ups.")

    st.markdown(
        """
        <div class="disclaimer">
            <strong>Disclaimer:</strong> This tool is a proof-of-concept trained on
            <em>synthetic data</em>. Results are not medically valid and must never replace
            a professional clinical assessment.
        </div>
        """,
        unsafe_allow_html=True,
    )
