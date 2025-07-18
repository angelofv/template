# ────────────────────────────────────────────────
# Image unique pour :
#   • MLflow (mode server ou file‑store)
#   • Build pipeline (stages builder/runtime/pipeline)
#   • Streamlit front
# ────────────────────────────────────────────────

############################
# 1) Builder : wheels offline
############################
FROM python:3.10-slim AS builder

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

COPY pyproject.toml requirements.txt README.md LICENSE ./
COPY src/ ./src/

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip wheel --wheel-dir /tmp/wheels -r requirements.txt

############################
# 2) Runtime commun
############################
FROM python:3.10-slim AS runtime

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser
ENV PYTHONUNBUFFERED=1 MPLCONFIGDIR=/tmp GIT_PYTHON_REFRESH=quiet \
    GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

WORKDIR /opt/app

COPY --from=builder /tmp/wheels /tmp/wheels
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir /tmp/wheels/* && rm -rf /tmp/wheels

############################
# 3) MLflow Server / file‑store (image de base)
############################
FROM ghcr.io/mlflow/mlflow:latest AS mlflow-base
RUN pip install --no-cache-dir psycopg2-binary boto3

############################
# 4) MLflow final avec entrypoint intelligent
############################
FROM mlflow-base AS mlflow
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


############################
# 5) Pipeline
############################
FROM runtime AS pipeline
COPY --chown=appuser:appuser . .
USER appuser
ENTRYPOINT ["python", "-m", "src.run"]

############################
# 6) Streamlit App
############################
FROM runtime AS app
WORKDIR /opt/app
COPY --chown=appuser:appuser app/app.py ./app.py
EXPOSE 8501
USER appuser
ENTRYPOINT ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
