from __future__ import annotations

import mlflow
import mlflow.exceptions
import mlflow.sklearn
import pandas as pd
from omegaconf import DictConfig
from prefect import get_run_logger, task
from sklearn.ensemble import RandomForestClassifier


@task
def train_model(df_clean: pd.DataFrame, cfg: DictConfig):
    logger = get_run_logger()
    logger.info("Entrainement...")

    # TODO : Replace by your own model training logic
    params = cfg.get("model", {})

    # 1. Hyper-paramètres (avec valeur par défaut)
    n_estimators = params.get("n_estimators", 100)
    mlflow.log_param("n_estimators", n_estimators)

    # 2. Séparation features / cible
    target = params.get("target", "target")
    X = df_clean.drop(columns=[target])
    y = df_clean[target]

    # 3. Entraînement
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X, y)

    # 4. Évaluation + métrique
    mlflow.log_metric("train_accuracy", float(model.score(X, y)))

    # 5. Log du modèle
    mlflow.sklearn.log_model(model, name="model")

    return model
