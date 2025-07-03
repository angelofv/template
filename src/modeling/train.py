import mlflow
import mlflow.sklearn
from omegaconf import DictConfig
import pandas as pd
from prefect import get_run_logger, task
from sklearn.ensemble import RandomForestClassifier


@task
def train_model(df_clean: pd.DataFrame, cfg: DictConfig):
    logger = get_run_logger()
    logger.info("Entrainement...")

    # TODO : Replace by your own model training logic
    # 1) hyper-param (ou défaut)
    n = cfg.model.get("n_estimators", 100)
    mlflow.log_param("n_estimators", n)

    # 2) split trivial
    target = cfg.model.get("target_column", "target")
    X = df_clean.drop(columns=[target])
    y = df_clean[target]

    # 3) entraînement
    model = RandomForestClassifier(n_estimators=n)
    model.fit(X, y)

    # 4) métrique basique & log
    acc = model.score(X, y)
    mlflow.log_metric("train_accuracy", float(acc))

    # 5) log du modèle
    mlflow.sklearn.log_model(model, artifact_path="model")
    return model