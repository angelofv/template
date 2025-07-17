from fastapi import FastAPI
from pydantic import BaseModel

from src.config import load_catalog

catalog = load_catalog()
app = FastAPI(title="ML FastAPI Service")

try:
    model = catalog.load("model")
except FileNotFoundError as e:
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
