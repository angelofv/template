# services/api.py
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
import mlflow.sklearn
from pydantic import BaseModel


# 1) on définit le lifespan qui charge le modèle une seule fois
@asynccontextmanager
async def lifespan(app: FastAPI):
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    model_name = "IrisClassifier"
    model_version = "latest"
    uri = f"models:/{model_name}/{model_version}"
    app.state.model = mlflow.sklearn.load_model(uri)
    yield


# 2) on passe ce lifespan à FastAPI
app = FastAPI(title="ML FastAPI Service", lifespan=lifespan)


class PredictRequest(BaseModel):
    features: list[list[float]]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictRequest):
    # 3) on récupère le modèle chargé au démarrage
    model = app.state.model
    preds = model.predict(request.features)
    return {"predictions": preds.tolist()}
