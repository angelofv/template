import mlflow
from prefect import flow, get_run_logger

from src.config import load_config
from src.modeling import train_model
from src.plotting import plot_metrics
from src.preprocessing import load_raw_data, preprocess


@flow(name="ML Pipeline")
def run():
    logger = get_run_logger()
    cfg = load_config()
    # Setup MLflow
    mlflow.set_tracking_uri(cfg.tracking.uri)
    mlflow.set_experiment(cfg.tracking.experiment_name)

    with mlflow.start_run():
        logger.info("Configuration chargée")

        # 1. Pré-traitement
        df_raw = load_raw_data(cfg)
        df_clean = preprocess(df_raw, cfg)

        # 2. Modélisation
        model = train_model(df_clean, cfg)

        # 3. Reporting
        report_path = plot_metrics(model, df_clean, cfg)
        logger.info(f"Rapport généré : {report_path}")


if __name__ == "__main__":
    run()
