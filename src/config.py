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
    preprocessing: str | Path = "configs/preprocessing.yaml",
    modeling: str | Path = "configs/modeling.yaml",
    plotting: str | Path = "configs/plotting.yaml",
) -> DictConfig:
    """
    Charge séparément les fichiers YAML de preprocessing, modeling et plotting,
    et les expose sous cfg.preprocessing, cfg.modeling, cfg.plotting.
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
    # Vérification d'existence
    for name, p in paths.items():
        if not p.exists():
            raise FileNotFoundError(f"Config manquante : {name} -> {p}")

    # Chargement individuel
    cfg_pre = OmegaConf.load(paths["preprocessing"])
    cfg_mod = OmegaConf.load(paths["modeling"])
    cfg_plt = OmegaConf.load(paths["plotting"])

    # Regroupement dans un unique DictConfig
    full_cfg = OmegaConf.create({
        "preprocessing": cfg_pre,
        "modeling": cfg_mod,
        "plotting": cfg_plt,
    })
    return full_cfg

def load_catalog() -> KedroDataCatalog:
    """Charge le DataCatalog Kedro en utilisant la nouvelle classe KedroDataCatalog."""
    catalog_dir = _to_repo_path("configs")
    loader = OmegaConfigLoader(str(catalog_dir))
    catalog_conf = loader.get("catalog")
    return KedroDataCatalog.from_config(catalog_conf)
