# ---------- build stage ----------
FROM python:3.10-slim AS builder

# 1. Installer Git (nécessaire pour GitPython utilisé par MLflow)
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

# 2. Copier les métadonnées du projet nécessaires à Flit
COPY pyproject.toml requirements.txt README.md LICENSE ./

# 3. Copier le code source et les configs
COPY src/ src/
COPY configs/ configs/

# 4. Construire les wheels hors-ligne
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip wheel --wheel-dir /tmp/wheels -r requirements.txt

# ---------- runtime stage ----------
FROM python:3.10-slim

# 5. Installer Git pour runtime (silence GitPython warning)
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# 6. Créer un utilisateur non-root
RUN useradd -m -u 1000 app

# 7. Variables d’environnement
ENV PYTHONUNBUFFERED=1 \
    MLFLOW_TRACKING_URI=file:///tmp/mlruns \
    MPLCONFIGDIR=/tmp \
    GIT_PYTHON_REFRESH=quiet \
    GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

# 8. Préparer le répertoire mlruns et lui donner la propriété à app
RUN mkdir -p /tmp/mlruns && chown app:app /tmp/mlruns

WORKDIR /opt/app

# 9. Installer les dépendances compilées
COPY --from=builder /tmp/wheels /tmp/wheels
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir /tmp/wheels/* && \
    rm -rf /tmp/wheels

# 10. Copier le reste du projet en tant qu’app
COPY --chown=app:app . .

# 11. Passer à l’utilisateur non-root
USER app

# 12. Lancer le pipeline par défaut
ENTRYPOINT ["python", "-m", "src.run"]
