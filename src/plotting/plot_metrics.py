from kedro.io import KedroDataCatalog
import matplotlib.pyplot as plt
import mlflow
from omegaconf import DictConfig
import pandas as pd
from prefect import get_run_logger, task


@task
def plot_metrics(
    model, df_clean: pd.DataFrame, cfg: DictConfig, catalog: KedroDataCatalog
) -> plt.Figure:
    logger = get_run_logger()
    logger.info("Plotting...")

    # TODO : Replace by your own plotting logic
    # 1) Calcul de la même accuracy
    params = cfg.get("model", {})
    target = params.get("target_column", "target")

    X = df_clean.drop(columns=[target])
    y = df_clean[target]
    preds = model.predict(X)
    acc = (preds == y).mean()

    # 2) Plot minimal
    fig, ax = plt.subplots()
    ax.bar(["accuracy"], [acc])
    ax.set_ylim(0, 1)
    ax.set_ylabel("score")
    fig.tight_layout()

    # 3) Log + sauvegarde
    mlflow.log_figure(fig, "plots/accuracy.png")
    catalog.save("accuracy_plot", fig)
    return fig
