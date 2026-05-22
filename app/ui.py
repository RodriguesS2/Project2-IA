import streamlit as st

CSS = """
<style>
    /* header */
    .app-header {
        background: #14375e; 
        color: #ffffff;
        padding: 20px 28px; 
        border-radius: 6px;
        margin-bottom: 1.6rem;
    }
    
    .app-header h1 { 
        color: #ffffff !important; 
        margin: 0; 
    }

    .app-header p {
        color: #d6e0ec !important;
    }

    /* form sec*/
    .section-header {
        font-size: 1.05rem; 
        color: #14375e;
        border-bottom: 1px solid #b9bfc7; 
        padding-bottom: 3px;
        margin-top: 1.2rem; 
        margin-bottom: 0.6rem;
    }

    /* lateral panel */
    .panel {
        border: 1px solid #cdd3da; 
        border-radius: 6px;
        background: #ffffff; 
        padding: 14px 16px;
    }

    .panel-title {
        font-weight: 700; 
        color: #14375e; 
        font-size: 1.05rem;
        border-bottom: 2px solid #14375e; 
        padding-bottom: 6px; 
        margin-bottom: 12px;
    }


    table.ref { 
        width: 100%; 
        border-collapse: collapse; 
        margin-bottom: 14px; 
        color: #1c1c1c; 
    }

    table.ref th, table.ref td { 
        padding: 6px; 
        border: 1px solid #d4d9e0; 
        text-align: center; 
    }

    table.ref th { 
        background: #14375e; 
        color: #ffffff; 
    }

    table.ref td.m {
        text-align: left; 
        font-weight: 600;
    }

    table.ref td.ok   {
        background: #e6f4ea; 
        color: #1b5e20; 
    }

    table.ref td.warn {
        background: #fff6e0; 
        color: #8a5a00;
    }

    table.ref td.bad  {
        background: #fdecea; 
        color: #a31515;
    }

    .band {
        font-size: 0.85rem; 
        margin: 4px 0; 
        color: #1c1c1c;
    }

    /* results */
    .risk-card {
        border: 1px solid #c9c9c9; 
        padding: 16px 18px; 
        margin-bottom: 1rem; 
        border-radius: 6px; 
    }

    .risk-vlow { background: #e6f4ea;}
    .risk-low { background: #f0f7e6;}
    .risk-medium { background: #fff6e0;}
    .risk-high { background: #fdf0e0;}
    .risk-vhigh { background: #fdecea;}
    
    .risk-label {
        font-size: 1rem; 
        font-weight: 700; 
        color: #14375e; 
        margin-bottom: 6px;
    }

    .risk-score {
        font-size: 2.5rem; 
        font-weight: 700; 
        line-height: 1; 
        color: #1c1c1c;
    }
    
    .risk-badge {
        display: inline-block; 
        margin-top: 10px; 
        padding: 4px 12px; 
        border-radius: 4px; 
        font-size: 0.8rem; 
        font-weight: 700; 
        text-transform: uppercase;
    }

    .badge-vlow {
        background: #2e7d32; 
        color: #fff;
    }

    .badge-low {
        background: #7cb342; 
        color: #fff;
    }

    .badge-medium {
        background: #f0a500; 
        color: #1c1c1c;
    }

    .badge-high {
        background: #e07b00; 
        color: #fff;
    }

    .badge-vhigh {
        background: #c0392b; 
        color: #fff;
    }
    
    button[data-testid="stNumberInputStepUp"]:hover,
    button[data-testid="stNumberInputStepDown"]:hover,
    button[data-testid="stNumberInputStepUp"]:focus,
    button[data-testid="stNumberInputStepDown"]:focus,
    button[data-testid="stNumberInputStepUp"]:active,
    button[data-testid="stNumberInputStepDown"]:active {
        color: #31333F !important;
        background-color: transparent !important;
        border-color: rgba(49, 51, 63, 0.2) !important;
    }
</style>
"""

def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def render_header():
    html_code = """<div class="app-header">
        <h1> Diabetes and Hypertension prediction </h1>
        <p> Estimation of diabetes and hypertension risk from patient demographics, laboratory results and lifestyle factors </p>
        </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def render_reference_panel():
    html_code = """<div class="panel">
<div class="panel-title">Clinical Reference Ranges</div>
<table class="ref">
<tr><th> Measure </th><th> Normal </th><th> Borderline </th><th> At risk </th></tr>
<tr><td class="m"> Glucose (mg/dL) </td><td class="ok"> &lt; 100 </td><td class="warn"> 100–125 </td><td class="bad"> &ge; 126 </td></tr>
<tr><td class="m"> HbA1c (%) </td><td class="ok"> &lt; 5.7 </td><td class="warn"> 5.7–6.4 </td><td class="bad"> &ge; 6.5 </td></tr>
<tr><td class="m"> Blood pressure (mmHg) </td><td class="ok"> &lt;120/80 </td><td class="warn"> 120–139/80–89 </td><td class="bad"> &ge;140/90 </td></tr>
<tr><td class="m"> BMI (kg/m&sup2;) </td><td class="ok"> 18.5–24.9 </td><td class="warn"> 25–29.9 </td><td class="bad"> &ge; 30 </td></tr>
<tr><td class="m"> LDL cholesterol </td><td class="ok"> &lt; 100 </td><td class="warn"> 100–159 </td><td class="bad"> &ge; 160 </td></tr>
<tr><td class="m"> HDL cholesterol </td><td class="ok"> &ge; 60 </td><td class="warn"> 40–59 </td><td class="bad"> &lt; 40 </td></tr>
<tr><td class="m"> Triglycerides </td><td class="ok"> &lt; 150 </td><td class="warn"> 150–199 </td><td class="bad"> &ge; 200 </td></tr>
</table>
<div class="panel-title" style="margin-top: 15px;"> Risks </div>
<div class="band"><strong> &lt; 30% </strong> &mdash; Very Low </div>
<div class="band"><strong> 30–50% </strong> &mdash; Low/Moderate </div>
<div class="band"><strong> 50–70% </strong> &mdash; Moderate/High </div>
<div class="band"><strong> 70–85% </strong> &mdash; High </div>
<div class="band"><strong> &gt; 85% </strong> &mdash; Very High </div>
</div>"""
    
    st.markdown(html_code, unsafe_allow_html=True)


def risk_tier(prob: float):
    if prob < 0.30: 
        return "Very Low", "vlow"
    
    elif prob < 0.50: 
        return "Low/Moderate", "low"
    
    elif prob < 0.70: 
        return "Moderate/High", "medium"
    
    elif prob < 0.85: 
        return "High", "high"
    
    else: 
        return "Very High", "vhigh"


def render_risk_card(title, prob):
    label, tier = risk_tier(prob)
    percentage = int(round(prob * 100))
    
    html_code = f"""<div class="risk-card risk-{tier}">
        <div class="risk-label"> {title} </div>
        <div class="risk-score"> {percentage} %</div>
        <span class="risk-badge badge-{tier}"> {label} Risk</span>
        </div>
    """
    
    st.markdown(html_code, unsafe_allow_html=True)


def render_clinical_advice(prob_diabetes: float, prob_hypertension: float):
    diabetes = prob_diabetes >= 0.5
    hypertension = prob_hypertension >= 0.5
    
    st.markdown("<br>", unsafe_allow_html=True)

    #alerts
    if diabetes and hypertension:
        st.error("Elevated risk for **both diabetes and hypertension**. Clinical follow-up and broad lifestyle review are advised.")
    
    elif diabetes:
        st.warning("Elevated risk for **diabetes**. Consider blood-sugar monitoring, weight management, increased physical activity and reduced sugar intake.")
    
    elif hypertension:
        st.warning("Elevated risk for **hypertension**. Consider blood-pressure monitoring, reduced sodium intake and stress management.")
    
    else:
        st.success("Low estimated risk for both conditions. Maintain healthy habits and routine check-ups.")

    st.caption("**Disclaimer:** The results are not medically validated and must never replace a professional clinical assessment.")