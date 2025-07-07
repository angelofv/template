import matplotlib.pyplot as plt
import mlflow
from omegaconf import DictConfig
import pandas as pd
from prefect import get_run_logger, task


@task
def plot_metrics(model, df_clean: pd.DataFrame, cfg: DictConfig):
    logger = get_run_logger()
    logger.info("Plotting...")

    # TODO : Replace by your own plotting logic
    # 1) calcul de la même accuracy
    params = cfg.get("model", {})
    target = params.get("target_column", "target")

    X = df_clean.drop(columns=[target])
    y = df_clean[target]
    preds = model.predict(X)
    acc = (preds == y).mean()

    # 2) plot minimal
    fig, ax = plt.subplots()
    ax.bar(["accuracy"], [acc])
    ax.set_ylim(0, 1)
    ax.set_ylabel("score")
    fig.tight_layout()

    # 3) sauvegarde et log
    out = "accuracy.png"
    fig.savefig(out)
    plt.close(fig)
    mlflow.log_artifact(out, artifact_path="plots")
    return out
