from __future__ import annotations

import streamlit as st

from src.config import load_catalog

# ────────────────────── CONFIG ──────────────────────
st.set_page_config(
    page_title="ML Project",
    page_icon="🤖",
    layout="centered",
)

# ───────────── Sidebar – profile ──────────────
PROFILE: dict[str, str] = {
    "name": "Angelo F.V.",
    "description": "Data Scientist & ML Engineer 🛠️",
    "location": "Paris, France",
    "avatar": "https://i.postimg.cc/6pDXBGFy/DSC0064-1.jpg",
}
LINKS: dict[str, str] = {
    "LinkedIn": "https://linkedin.com/in/angelo-fv/",
    "GitHub": "https://github.com/angelofv",
    "Email": "mailto:angelo.fv@outlook.fr",
}

with st.sidebar:
    if PROFILE["avatar"]:
        st.image(PROFILE["avatar"], width=130)
    st.title(PROFILE["name"])
    st.caption(f"{PROFILE['description']}  \n📍 {PROFILE['location']}")
    inline = " · ".join(f"[{l}]({u})" for l, u in LINKS.items() if u)
    if inline:
        st.markdown(inline)

st.markdown("---")

# ─────────── Load model from catalog ───────────
catalog = load_catalog()
model = catalog.load("model")

# ───────────── Model explorer ──────────────
FEATURES: list[str] = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
]
st.header("Model Explorer")
with st.form("prediction_form"):
    st.write("Enter feature values:")
    values = [st.number_input(f, value=0.0, format="%.3f") for f in FEATURES]
    if st.form_submit_button("Predict"):
        try:
            with st.spinner("Predicting…"):
                pred = model.predict([values])[0]
            st.success(f"Prediction: {pred}")
        except Exception as exc:
            st.error(f"Prediction failed: {exc}")
