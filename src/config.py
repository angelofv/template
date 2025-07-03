from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from omegaconf import DictConfig, OmegaConf

# Load environment variables from a .env file if present
load_dotenv()

# Resolve the repository root once at import time.  ``config.py`` lives in
# ``<repo>/src/``, so two ``.parent`` calls go back to the repository root.
_REPO_ROOT = Path(__file__).resolve().parent.parent


def _to_repo_path(path: str | Path) -> Path:
    """Return an *absolute* path interpreted from the repo root if needed.

    Parameters
    ----------
    path
        A string or Path. If it is already absolute, it is returned unchanged.
        Otherwise, it is considered relative to the repository root.
    """
    p = Path(path)
    return p if p.is_absolute() else _REPO_ROOT / p


# Public API


def load_config(
    *,
    preproc: str | Path = "configs/preprocessing.yaml",
    model: str | Path = "configs/modeling.yaml",
    plot: str | Path = "configs/plotting.yaml",
    mlflow: str | Path = "configs/mlflow.yaml",
) -> DictConfig:
    """Load YAML config files (preproc, model, plot, mlflow), merge them, and apply env overrides.

    Environment variables (PREPROC_CONFIG, MODEL_CONFIG, PLOT_CONFIG, MLFLOW_CONFIG) can override file paths.
    MLflow settings (MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT) override YAML values.
    """
    # 1. Override config file paths from environment variables if set
    preproc = os.getenv("PREPROC_CONFIG", str(preproc))
    model = os.getenv("MODEL_CONFIG", str(model))
    plot = os.getenv("PLOT_CONFIG", str(plot))
    mlflow = os.getenv("MLFLOW_CONFIG", str(mlflow))

    # 2. Resolve to absolute paths anchored at the repo root if necessary
    paths = [_to_repo_path(p) for p in (preproc, model, plot, mlflow)]

    # 3. Sanity-check existence
    for p in paths:
        if not p.exists():
            raise FileNotFoundError(f"Config manquante : {p}")

    # 4. Load and merge all configs (order matters)
    cfg = OmegaConf.merge(*(OmegaConf.load(p) for p in paths))

    # 5. Override MLflow settings from environment or keep YAML defaults
    cfg.tracking.uri = os.getenv("MLFLOW_TRACKING_URI", cfg.tracking.uri)
    cfg.tracking.experiment_name = os.getenv("MLFLOW_EXPERIMENT", cfg.tracking.experiment_name)

    return cfg
