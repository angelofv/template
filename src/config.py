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
    config_file: str | Path = "configs/config.yaml",
    env_var: str = "CONFIG_PATH",
) -> dict:
    """
    Charge un fichier YAML unique de configuration et renvoie son contenu
    en tant que dictionnaire Python pur.

    - Si la variable d'environnement CONFIG_PATH est définie, elle l'emporte.
    - Aucun formatage interne n'est imposé au YAML; toutes les clés sont retournées.
    """
    # Détermination du chemin de configuration
    cfg_path = Path(os.getenv(env_var, str(config_file)))
    cfg_path = _to_repo_path(cfg_path)

    if not cfg_path.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable : {cfg_path}")

    # Chargement du YAML
    cfg = OmegaConf.load(cfg_path)

    # Conversion en container Python pur (dict, list, etc.)
    return OmegaConf.to_container(cfg, resolve=True)


def load_catalog() -> DataCatalog:
    """Charge le DataCatalog Kedro en utilisant la classe DataCatalog."""
    catalog_dir = _to_repo_path("configs")
    loader = OmegaConfigLoader(str(catalog_dir))
    catalog_conf = loader.get("catalog")
    return DataCatalog.from_config(catalog_conf)
