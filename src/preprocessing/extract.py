from kedro.io import KedroDataCatalog
from omegaconf import DictConfig
import pandas as pd
from prefect import get_run_logger, task
from sklearn.datasets import load_iris


@task
def load_raw_data(catalog: KedroDataCatalog) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info("Extraction…")

    # TODO : Replace by your own data loading logic
    # 1) Chargement
    df = load_iris(as_frame=True).frame

    # 2) Sauvegarde via Kedro Catalog
    catalog.save("raw_data", df)
    return df


@task
def preprocess(df_raw: pd.DataFrame, cfg: DictConfig, catalog: KedroDataCatalog) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info("Preprocessing...")

    # TODO : Replace by your own preprocessing logic
    # 1) Exemple de nettoyage
    df_processed = df_raw.dropna()

    # 2) Sauvegarde via Kedro Catalog
    catalog.save("processed_data", df_processed)
    return df_processed
