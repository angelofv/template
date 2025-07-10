import os
import pickle

import mlflow


def init_mlflow(
    tracking_uri_env: str = "MLFLOW_TRACKING_URI",
    default_tracking_uri: str = "file:./mlruns",
    experiment_env: str = "MLFLOW_EXPERIMENT",
    default_experiment: str = "Default",
) -> None:
    """
    Initialise MLflow en lisant les variables d'env. et en configurant
    le tracking URI et le nom d'expérience.
    """
    tracking_uri = os.getenv(tracking_uri_env, default_tracking_uri)
    experiment_name = os.getenv(experiment_env, default_experiment)

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)


def load_model_from_file(filepath: str):
    """
    Charge un modèle sklearn enregistré en pickle.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Modèle introuvable à {filepath}")
    with open(filepath, "rb") as f:
        return pickle.load(f)
