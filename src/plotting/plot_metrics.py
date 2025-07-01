from omegaconf import DictConfig
import pandas as pd
from prefect import get_run_logger, task


@task
def plot_metrics(model, df_clean: pd.DataFrame, cfg: DictConfig):
    logger = get_run_logger()
    logger.info("Plotting...")
    # TODO
