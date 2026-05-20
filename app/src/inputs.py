import streamlit as st

#physical activity is stored 0..7 in the data
PHYS_OPTIONS = {
    "0 days": 0, "1 day": 1, "2 days": 2,
    "3 days": 3, "4 days": 4, "5 days": 5, "6 days": 6, "7 days": 7,
}


def _to_binary(label):
    return 1 if "(1)" in label else 0


#sidebar to collect info
def collect_inputs():
    with st.sidebar:
        st.markdown("## Patient Information")

        mode = st.radio(
            "Input method",
            ["Sliders", "Type values"],
            horizontal=True,
            help="Sliders are quick; 'Type values' lets you enter exact numbers.",
        )

        st.markdown("### Demographics")
        sex = st.radio("Biological Sex", ["Female (0)", "Male (1)"], horizontal=True)

        #we will use the slide mode
        if mode == "Sliders":
            age = st.slider("Age (years)", 18, 90, 45, 1)

            st.markdown("### Body Metrics")
            bmi = st.slider("BMI (kg/m2)", 15.0, 50.0, 26.0, 0.1)
            systolic = st.slider("Systolic BP (mmHg)", 80, 200, 120, 1)
            diastolic = st.slider("Diastolic BP (mmHg)", 50, 120, 80, 1)

            st.markdown("### Lab Results")
            glucose = st.slider("Fasting Glucose (mg/dL)", 60, 300, 90, 1)
            cholesterol = st.slider("Cholesterol (mg/dL)", 100, 400, 180, 1)
            hba1c = st.slider("HbA1c (%)", 3.0, 15.0, 5.0, 0.1)
            hdl_cholesterol = st.slider("HDL Cholesterol (mg/dL)", 20, 100, 50, 1)
            ldl_cholesterol = st.slider("LDL Cholesterol (mg/dL)", 50, 250, 100, 1)
            triglycerides = st.slider("Triglycerides (mg/dL)", 50, 500, 150, 1)
        
        #input forms mode with typed inputs
        else:
            age = st.number_input("Age (years)", 18, 90, 45, 1)

            st.markdown("### Body Metrics")
            bmi = st.number_input("BMI (kg/m2)", 15.0, 50.0, 26.0, 0.1)
            systolic = st.number_input("Systolic BP (mmHg)", 80, 200, 120, 1)
            diastolic = st.number_input("Diastolic BP (mmHg)", 50, 120, 80, 1)

            st.markdown("### Lab Results")
            glucose = st.number_input("Fasting Glucose (mg/dL)", 60, 300, 90, 1)
            cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 400, 180, 1)
            hba1c = st.number_input("HbA1c (%)", 3.0, 15.0, 5.0, 0.1)
            hdl_cholesterol = st.number_input("HDL Cholesterol (mg/dL)", 20, 100, 50, 1)
            ldl_cholesterol = st.number_input("LDL Cholesterol (mg/dL)", 50, 250, 100, 1)
            triglycerides = st.number_input("Triglycerides (mg/dL)", 50, 500, 150, 1)

        #same for each case (slider/type)
        st.markdown("### Lifestyle")
        smoking = st.radio("Current Smoker", ["No (0)", "Yes (1)"], horizontal=True)
        phys_label = st.selectbox("Physical Activity Level", list(PHYS_OPTIONS.keys()), index=2)

        st.markdown("### Family History")
        fam_diabetes = st.radio("Diabetes in family", ["No (0)", "Yes (1)"], horizontal=True)
        fam_hypertension = st.radio("Hypertension in family", ["No (0)", "Yes (1)"], horizontal=True)

        st.markdown("---")
        predict = st.button("Predict Risk", use_container_width=True)

    #store all the data collected together
    inputs = {
        "age": float(age),
        "sex": _to_binary(sex),
        "bmi": float(bmi),
        "systolic_pressure": float(systolic),
        "diastolic_pressure": float(diastolic),
        "glucose": float(glucose),
        "hba1c": float(hba1c),
        "cholesterol": float(cholesterol),
        "hdl_cholesterol": float(hdl_cholesterol),
        "ldl_cholesterol": float(ldl_cholesterol),
        "triglycerides": float(triglycerides),
        "smoking": _to_binary(smoking),
        "physical_activity": float(PHYS_OPTIONS[phys_label]),
        "family_history_diabetes": _to_binary(fam_diabetes),
        "family_history_hypertension": _to_binary(fam_hypertension),
    }
    
    return inputs, predict
