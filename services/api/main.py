import os

from fastapi import FastAPI
from pydantic import BaseModel

from src.utils import load_model_from_file


class PredictRequest(BaseModel):
    features: list[list[float]]  # Liste d'observations, chacune une liste de floats


app = FastAPI(title="ML FastAPI Service")
MODEL_PATH = os.getenv("MODEL_PATH", "/app/data/03_models/model.pkl")
model = load_model_from_file(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictRequest):
    preds = model.predict(request.features)
    return {"predictions": preds.tolist()}
