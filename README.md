# Diabetes and Hypertension risk prediction model

This project is a POC of a diabetes and hypertension risk detection machine learning model, developed and trained on artificial data.

We've also developed a simple web app to interact with the model, by inputting hypothetical patient information.

## Initial setup

```
// To create virtual environment (recommended)
python -m venv .venv  
```

```
// To activate the venv (on macOS / Linux):
source .venv/bin/activate
```

```
// To install the necessary dependencies:
pip install -r requirements.txt
```

## To train/export models / see model scores and metrics

Run each cell of the model_building notebook in order. The model will be exported to app/model, which will then be used by the web app.

## To run the web app

```
// Change the path to the app directory
cd app

// Run the app locally
streamlit run app.py
```