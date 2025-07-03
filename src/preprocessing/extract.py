from omegaconf import DictConfig
import pandas as pd
from prefect import get_run_logger, task
from sklearn.datasets import load_iris


@task
def load_raw_data(cfg: DictConfig) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info("Extraction...")

    # TODO : Replace by your own data loading logic
    df = load_iris(as_frame=True).frame
    return df


@task
def preprocess(df_raw: pd.DataFrame, cfg: DictConfig) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info("Preprocessing...")

    # TODO : Replace by your own preprocessing logic
    df_processed = df_raw.copy()
    return df_processed
