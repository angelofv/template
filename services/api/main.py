import os
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from src.utils import load_model_from_file

# Détecte dynamiquement le chemin vers le modèle si on est en local ou en container
BASE_DIR = Path(__file__).resolve().parent      # racine du projet dans l’image
DEFAULT_MODEL_PATH = BASE_DIR / "data" / "03_models" / "model.pkl"
MODEL_PATH = Path(os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH)))

app = FastAPI(title="ML FastAPI Service")

try:
    model = load_model_from_file(str(MODEL_PATH))
except FileNotFoundError as e:
    # Fallback minimal pour dev local sans Docker
    from sklearn.dummy import DummyClassifier

    dummy = DummyClassifier()
    # Fit simple pour interface scikit
    dummy.fit([[0, 0, 0, 0]], [0])
    model = dummy
    app.state._model_load_error = str(e)


class PredictRequest(BaseModel):
    features: list[list[float]]  # Liste d'observations, chacune une liste de floats


@app.get("/health")
def health():
    status = {"status": "ok"}
    # Ajoute info si fallback activé
    if hasattr(app.state, "_model_load_error"):
        status["warning"] = "Model load error: " + app.state._model_load_error
    return status


@app.post("/predict")
def predict(request: PredictRequest):
    preds = model.predict(request.features)
    return {"predictions": preds.tolist()}
