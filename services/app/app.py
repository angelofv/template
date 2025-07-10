import os

import requests
import streamlit as st

st.title("ML Model Explorer")
api_url = os.getenv("API_URL", "http://localhost:8000") + "/predict"

# Noms des features du modèle Iris
feature_names = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
]

with st.form("prediction_form"):
    st.write("Entrez les valeurs des features :")
    input_data = {}
    for name in feature_names:
        input_data[name] = st.number_input(name, value=0.0, format="%.3f")
    submitted = st.form_submit_button("Predict")
    if submitted:
        # Préparer la liste de listes pour l'API
        features = [list(input_data.values())]
        response = requests.post(api_url, json={"features": features})
        preds = response.json().get("predictions", [])
        st.write("### Prédiction", preds[0])
