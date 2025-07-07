from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from kedro.config import OmegaConfigLoader
from kedro.io import KedroDataCatalog
from omegaconf import DictConfig, OmegaConf

# Charger les variables d'environnement depuis un fichier .env si présent
load_dotenv()

# Racine du dépôt
_REPO_ROOT = Path(__file__).resolve().parent.parent


def _to_repo_path(path: str | Path) -> Path:
    """Convertit un chemin relatif en absolu depuis la racine du repo."""
    p = Path(path)
    return p if p.is_absolute() else _REPO_ROOT / p


def load_config(
    *,
    preproc: str | Path = "configs/preprocessing.yaml",
    model: str | Path = "configs/modeling.yaml",
    plot: str | Path = "configs/plotting.yaml",
) -> DictConfig:
    """Charge et fusionne les configs YAML (prétraitement, modélisation, plot)."""
    preproc = os.getenv("PREPROC_CONFIG", str(preproc))
    model = os.getenv("MODEL_CONFIG", str(model))
    plot = os.getenv("PLOT_CONFIG", str(plot))

    paths = [_to_repo_path(p) for p in (preproc, model, plot)]
    for p in paths:
        if not p.exists():
            raise FileNotFoundError(f"Config manquante : {p}")

    return OmegaConf.merge(*(OmegaConf.load(p) for p in paths))


def load_catalog() -> KedroDataCatalog:
    """Charge le DataCatalog Kedro en utilisant la nouvelle classe KedroDataCatalog."""
    catalog_dir = _to_repo_path("configs")
    loader = OmegaConfigLoader(str(catalog_dir))
    catalog_conf = loader.get("catalog")
    return KedroDataCatalog.from_config(catalog_conf)
