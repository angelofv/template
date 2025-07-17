# 1) Builder: compiler toutes les dépendances en wheels
FROM python:3.10-slim AS builder

# Installer git (pour GitPython / MLflow)
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

# Copier métadonnées du projet et code pour pip -e .
COPY pyproject.toml requirements.txt README.md LICENSE ./
COPY src/ ./src/

# Construire les wheels hors‑ligne
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip wheel --wheel-dir /tmp/wheels -r requirements.txt

# 2) Runtime de base: installer les wheels
FROM python:3.10-slim AS runtime

# Git pour GitPython warnings
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Créer un user non-root
RUN useradd -m -u 1000 appuser

ENV PYTHONUNBUFFERED=1 \
    MLFLOW_TRACKING_URI=file:///tmp/mlruns \
    MPLCONFIGDIR=/tmp \
    GIT_PYTHON_REFRESH=quiet \
    GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

WORKDIR /opt/app

# Installer les wheels générés
COPY --from=builder /tmp/wheels /tmp/wheels
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir /tmp/wheels/* && \
    rm -rf /tmp/wheels

# 3) Stage "pipeline"
FROM runtime AS pipeline

# Copier tout le projet (code, configs, notebooks ignorés par .dockerignore)
COPY --chown=appuser:appuser . .

USER appuser

ENTRYPOINT ["python", "-m", "src.run"]

# 4) Stage "app" (Streamlit)
FROM runtime AS app

WORKDIR /opt/app
COPY --chown=appuser:appuser app/app.py ./app.py
EXPOSE 8501

USER appuser
ENTRYPOINT ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]