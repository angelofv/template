from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from omegaconf import DictConfig, OmegaConf

load_dotenv()

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

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


# -----------------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------------

def load_config(
    *,
    preproc: str | Path = "configs/preprocessing.yaml",
    model: str | Path = "configs/modeling.yaml",
    plot: str | Path = "configs/plotting.yaml",
) -> DictConfig:
    """Load the three YAML files (preproc, model, plot) and merge them.

    The paths can be overridden via environment variables ``PREPROC_CONFIG``,
    ``MODEL_CONFIG`` and ``PLOT_CONFIG``.  Whatever the source, paths are first
    converted to absolute by :pyfunc:`_to_repo_path`, so they are resolved
    relative to the *project root* if they are not already absolute.

    Returns
    -------
    DictConfig
        A single *OmegaConf* configuration containing all three sub‑configs.
    """
    # Environment variable overrides (highest priority)
    preproc = os.getenv("PREPROC_CONFIG", str(preproc))
    model = os.getenv("MODEL_CONFIG", str(model))
    plot = os.getenv("PLOT_CONFIG", str(plot))

    # Resolve to absolute paths anchored at the repo root if necessary
    paths = [_to_repo_path(p) for p in (preproc, model, plot)]

    # Sanity‑check existence
    for p in paths:
        if not p.exists():
            raise FileNotFoundError(f"Config manquante : {p}")

    # Load then merge with OmegaConf (order matters!)
    cfgs = [OmegaConf.load(p) for p in paths]
    return OmegaConf.merge(*cfgs)
