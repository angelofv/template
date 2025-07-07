import pandas as pd
from prefect import get_run_logger, task
from sklearn.datasets import load_iris


@task
def load_raw_data() -> pd.DataFrame:
    logger = get_run_logger()
    logger.info("Extract raw data")

    # TODO : Replace by your own data loading logic
    df = load_iris(as_frame=True).frame
    return df


@task
def preprocess(
    df_raw: pd.DataFrame,
    dropna_columns: list[str],
) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info("Preprocessing data")
    
    # TODO : Replace by your own preprocessing logic
    df_processed = df_raw.dropna(subset=dropna_columns)
    return df_processed
