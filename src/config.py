from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from kedro.config import OmegaConfigLoader
from kedro.io import DataCatalog
from omegaconf import OmegaConf

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
    preprocessing: str | Path = "configs/preprocessing.yaml",
    modeling: str | Path = "configs/modeling.yaml",
    plotting: str | Path = "configs/plotting.yaml",
) -> dict:
    """
    Charge séparément les fichiers YAML de preprocessing, modeling et plotting,
    et renvoie un dict Python pur :
      {
        "preprocessing": {...},
        "modeling": {...},
        "plotting": {...},
      }
    """
    # Récupère les chemins via les variables d'environnement (facultatif)
    preprocessing = os.getenv("PREPROCESSING_CONFIG", str(preprocessing))
    modeling = os.getenv("MODELING_CONFIG", str(modeling))
    plotting = os.getenv("PLOTTING_CONFIG", str(plotting))

    # Construction des chemins absolus
    paths = {
        "preprocessing": _to_repo_path(preprocessing),
        "modeling": _to_repo_path(modeling),
        "plotting": _to_repo_path(plotting),
    }
    for name, p in paths.items():
        if not p.exists():
            raise FileNotFoundError(f"Config manquante : {name} -> {p}")

    # Chargement individuel en DictConfig
    cfg_pre = OmegaConf.load(paths["preprocessing"])
    cfg_mod = OmegaConf.load(paths["modeling"])
    cfg_plt = OmegaConf.load(paths["plotting"])

    # Fusion en un seul DictConfig
    full_cfg = OmegaConf.create(
        {
            "preprocessing": cfg_pre,
            "modeling": cfg_mod,
            "plotting": cfg_plt,
        }
    )

    # Conversion en containers Python purs
    return OmegaConf.to_container(full_cfg, resolve=True)


def load_catalog() -> DataCatalog:
    """Charge le DataCatalog Kedro en utilisant la classe DataCatalog."""
    catalog_dir = _to_repo_path("configs")
    loader = OmegaConfigLoader(str(catalog_dir))
    catalog_conf = loader.get("catalog")
    return DataCatalog.from_config(catalog_conf)
