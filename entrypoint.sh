#!/usr/bin/env bash
set -euo pipefail

# ────────────────────────────────────────────────
#  MLflow entrypoint “auto” :
#    – Si MLFLOW_S3_BUCKET est défini  →  mode S3 + Postgres
#    – Sinon                           →  mode local (SQLite + ./mlruns)
# ────────────────────────────────────────────────

echo "MLflow server – autodetecting storage backend …"

if [[ -z "${MLFLOW_S3_BUCKET:-}" ]]; then
  echo "↪  Local mode  (artifacts in ./mlruns)"
  exec mlflow server \
    --backend-store-uri "sqlite:///mlflow.db" \
    --artifacts-destination "./mlruns" \
    --serve-artifacts \
    --host 0.0.0.0 --port 5000
else
  : "${MLFLOW_BACKEND_URI:=postgresql+psycopg2://mlflow:mlflow@db/mlflow}"
  echo "↪  S3 mode     (bucket: ${MLFLOW_S3_BUCKET}, backend: ${MLFLOW_BACKEND_URI})"
  exec mlflow server \
    --backend-store-uri "${MLFLOW_BACKEND_URI}" \
    --artifacts-destination "${MLFLOW_S3_BUCKET}" \
    --serve-artifacts \
    --host 0.0.0.0 --port 5000
fi
