import streamlit as st

def render_header():
    st.title("Diabetes and Hypertension Prediction")
    st.info("Estimation of diabetes and hypertension risk from patient demographics, "
        "laboratory results and lifestyle factors.")
    st.divider()

def render_table():
    with st.container(border=True):
        st.subheader("Clinical Reference Ranges")
        
        markdown_table = """
        | Measure | Normal | Borderline | At risk |
        | :--- | :--- | :--- | :--- |
        | **Glucose** (mg/dL) | < 100 | 100–125 | >= 126 |
        | **HbA1c** (%) | < 5.7 | 5.7–6.4 | >= 6.5 |
        | **Blood pressure** (mmHg) | < 120/80 | 120–139/80–89 | >= 140/90 |
        | **BMI** (kg/m²) | 18.5–24.9 | 25–29.9 | >= 30 |
        | **LDL cholesterol** | < 100 | 100–159 | >= 160 |
        | **HDL cholesterol** | >= 60 | 40–59 | < 40 |
        | **Triglycerides** | < 150 | 150–199 | >= 200 |
        """
        st.markdown(markdown_table)
        
        st.divider()
        
        st.subheader("Risk Tiers")
        st.markdown("""
        * **< 30%** — Very Low
        * **30–50%** — Low/Moderate
        * **50–70%** — Moderate/High
        * **70–85%** — High
        * **> 85%** — Very High
        """)

#maps the risk
def risk_tier(prob: float):
    if prob < 0.30: 
        return "Very Low"
    
    elif prob < 0.50: 
        return "Low/Moderate"
    
    elif prob < 0.70: 
        return "Moderate/High"
    
    elif prob < 0.85: 
        return "High"
    
    else: 
        return "Very High"


#renders the model output based on the prob
def render_risk_card(title, prob):
    label = risk_tier(prob)
    percentage = int(round(prob * 100))
    
    if prob < 0.30: 
        bg_color = "#e6f4ea"  
        text_color = "#1b5e20" 
    
    elif prob < 0.50: 
        bg_color = "#f0f7e6" 
        text_color = "#33691e"
    
    elif prob < 0.70: 
        bg_color = "#fff6e0"  
        text_color = "#f57f17"
    
    elif prob < 0.85: 
        bg_color = "#fdf0e0"  
        text_color = "#e65100"
    
    else: 
        bg_color = "#fdecea" 
        text_color = "#a31515" 

    #color the card based on the risk
    html_code = f"""
    <div style="background: {bg_color}; padding: 15px; border-radius: 5px; border: 1px solid #ccc; margin-bottom: 15px;">
        <h4 style="margin: 0;">{title}</h4>
        <h1 style="margin: 5px 0; color: {text_color};">{percentage}%</h1>
        <span style="background: {text_color}; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px;">
            <b>{label.upper()} RISK</b>
        </span>
    </div>
    """
    
    st.markdown(html_code, unsafe_allow_html=True)


#output the advice based on the risk
def render_clinical_advice(prob_diabetes: float, prob_hypertension: float):
    diabetes = prob_diabetes >= 0.5
    hypertension = prob_hypertension >= 0.5
    
    st.write("")
    
    if diabetes and hypertension:
        st.error("Elevated risk for **both diabetes and hypertension**. Clinical follow-up and broad lifestyle review are advised.")
    
    elif diabetes:
        st.warning("Elevated risk for **diabetes**. Consider blood-sugar monitoring, weight management, increased physical activity and reduced sugar intake.")
    
    elif hypertension:
        st.warning("Elevated risk for **hypertension**. Consider blood-pressure monitoring, reduced sodium intake and stress management.")
    
    else:
        st.success("Low estimated risk for both conditions. Maintain healthy habits and routine check-ups.")

    st.caption("**Disclaimer:** The results are not medically validated and must never replace a professional clinical assessment.")