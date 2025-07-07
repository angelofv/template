import os

import mlflow
from prefect import flow, get_run_logger

from src.config import load_catalog, load_config
from src.modeling import train_model
from src.plotting import plot_metrics
from src.preprocessing import load_raw_data, preprocess


@flow(name="ML Pipeline")
def run():
    logger = get_run_logger()
    cfg = load_config()
    catalog = load_catalog()

    # Setup MLflow
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")
    experiment_name = os.getenv("MLFLOW_EXPERIMENT", "Default")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        logger.info("Configuration & catalog chargés")

        # 1. Pré-traitement
        df_raw = load_raw_data(catalog)
        df_clean = preprocess(df_raw, cfg, catalog)

        # 2. Modélisation
        model = train_model(df_clean, cfg, catalog)

        # 3. Reporting
        _ = plot_metrics(model, df_clean, cfg, catalog)
        logger.info("Pipeline terminé")


if __name__ == "__main__":
    run()
