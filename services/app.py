from __future__ import annotations

import os
from typing import Dict, List

import requests
import streamlit as st

# ────────────────────── CONFIG ──────────────────────
st.set_page_config(
    page_title=os.getenv("APP_NAME", "ML Project"),
    page_icon="🤖",
    layout="centered",
)

# ───────────── Sidebar – profile ──────────────
PROFILE: Dict[str, str] = {
    "name": os.getenv("PROFILE_NAME", "Angelo F.V."),
    "description": os.getenv("PROFILE_DESC", "Data Scientist & ML Engineer 🛠️"),
    "location": os.getenv("PROFILE_LOC", "Paris, France"),
    "avatar": os.getenv("PROFILE_AVATAR", "https://i.postimg.cc/6pDXBGFy/DSC0064-1.jpg"),
}
LINKS: Dict[str, str] = {
    "LinkedIn": os.getenv("LINK_LINKEDIN", "https://linkedin.com/in/angelo-fv/"),
    "GitHub": os.getenv("LINK_GITHUB", "https://github.com/angelofv"),
    "Email": os.getenv("LINK_EMAIL", "mailto:angelo.fv@outlook.fr"),
}

with st.sidebar:
    if PROFILE["avatar"]:
        st.image(PROFILE["avatar"], width=130)
    st.title(PROFILE["name"])
    st.caption(f"{PROFILE['description']}  \n📍 {PROFILE['location']}")
    inline = " · ".join(f"[{l}]({u})" for l, u in LINKS.items() if u)
    if inline:
        st.markdown(inline)

# ───────────── Landing page ──────────────
st.title(os.getenv("PROJECT_TITLE", "My ML Project"))
st.write(os.getenv("PROJECT_DESC", "_A concise project description._"))

docs_url = os.getenv("PROJECT_DOCS_URL", "a")
repo_url = os.getenv("PROJECT_REPO_URL", "b")

if docs_url or repo_url:
    st.subheader("Resources")
    if docs_url:
        st.markdown(f"📄 **Docs** – Full reference & examples [here]({docs_url}).")
    if repo_url:
        st.markdown(f"🐙 **Repo** – Browse the source code on GitHub [here]({repo_url}).")

st.markdown("---")

# ───────────── Model explorer ──────────────
FEATURES: List[str] = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
]
API_URL = os.getenv("API_URL", "http://localhost:8000") + "/predict"

st.header("Model Explorer")
with st.form("prediction_form"):
    st.write("Enter feature values:")
    values = [st.number_input(f, value=0.0, format="%.3f") for f in FEATURES]
    if st.form_submit_button("Predict"):
        try:
            with st.spinner("Calling model…"):
                r = requests.post(API_URL, json={"features": [values]}, timeout=5)
                r.raise_for_status()
                preds = r.json().get("predictions", [])
            st.success(f"Prediction: {preds[0] if preds else '—'}")
        except requests.exceptions.RequestException as exc:
            st.error(f"Request failed: {exc}")
