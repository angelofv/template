# ---------- build stage ----------
FROM python:3.10-slim AS builder

# 1. Installer Git (nécessaire pour GitPython utilisé par MLflow)
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

# 2. Copier les métadonnées du projet nécessaires à Flit
COPY pyproject.toml requirements.txt README.md LICENSE ./

# 3. Copier le code source et les configs
COPY src/ src/
COPY configs/ configs/

# 4. Construire les wheels hors-ligne (inclut -e . via pyproject.toml)
RUN pip install --upgrade pip \
 && pip wheel --wheel-dir /tmp/wheels -r requirements.txt

# ---------- runtime stage ----------
FROM python:3.10-slim

# 5. Installer Git pour runtime (silence GitPython warning)
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

# 6. Créer un utilisateur non-root
RUN useradd -m -u 1000 app
WORKDIR /opt/app

# 7. Variables d’environnement
ENV PYTHONUNBUFFERED=1 \
    MLFLOW_TRACKING_URI=http://mlflow:5000 \
    GIT_PYTHON_REFRESH=quiet \
    GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

# 8. Installer les dépendances compilées
COPY --from=builder /tmp/wheels /tmp/wheels
RUN pip install --no-cache-dir /tmp/wheels/* \
 && rm -rf /tmp/wheels

# 9. Copier le reste du projet
COPY --chown=app:app . .

# 10. Passer à l’utilisateur non-root
USER app

# 11. Lancer le pipeline par défaut
ENTRYPOINT ["python", "-m", "src.main"]
