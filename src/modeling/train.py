from __future__ import annotations

import mlflow
import mlflow.sklearn
import pandas as pd
from prefect import get_run_logger, task
from sklearn.ensemble import RandomForestClassifier


@task
def train_model(
    df_clean: pd.DataFrame,
    n_estimators: int,
    target: str,
) -> RandomForestClassifier:
    logger = get_run_logger()
    logger.info("Entraînement du modèle")

    # TODO : Replace by your own model training logic
    # 1) Log hyper-paramètre
    mlflow.log_param("n_estimators", n_estimators)

    # 2) Séparation features / cible
    X = df_clean.drop(columns=[target])
    y = df_clean[target]

    # 3) Entraînement
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X, y)

    # 4) Évaluation
    score = float(model.score(X, y))
    mlflow.log_metric("train_accuracy", score)

    # 5) Log du modèle
    mlflow.sklearn.log_model(model, name="model")
    return model
