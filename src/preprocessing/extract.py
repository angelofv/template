from omegaconf import DictConfig
import pandas as pd
from prefect import get_run_logger, task


@task
def load_raw_data(cfg: DictConfig) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info("Extraction...")
    # TODO

@task
def preprocess(df_raw: pd.DataFrame, cfg: DictConfig)-> pd.DataFrame: 
    logger = get_run_logger()
    logger.info("Preprocessing...")
    # TODO