import os
from pathlib import Path

from dotenv import load_dotenv
from omegaconf import DictConfig, OmegaConf

load_dotenv()


def load_config(
    *,
    preproc: str | Path = "configs/preprocessing.yaml",
    model: str | Path = "configs/modeling.yaml",
    plot: str | Path = "configs/plotting.yaml",
) -> DictConfig:
    """
    Charge et merge (dans l'ordre) les 3 fichiers YAML :
      - préprocessing
      - modeling
      - plotting

    Peut être overridé par les vars d'env :
      PREPROC_CONFIG, MODEL_CONFIG, PLOT_CONFIG
    """
    # override éventuel
    preproc = Path(os.getenv("PREPROC_CONFIG", preproc))
    model = Path(os.getenv("MODEL_CONFIG", model))
    plot = Path(os.getenv("PLOT_CONFIG", plot))

    # vérification existence
    for p in (preproc, model, plot):
        if not p.exists():
            raise FileNotFoundError(f"Config manquante : {p}")

    # chargement et fusion
    cfgs = [OmegaConf.load(str(p)) for p in (preproc, model, plot)]
    return OmegaConf.merge(*cfgs)
