# Template – ML Pipeline Starter

[![CI](https://github.com/angelofv/template/actions/workflows/ci.yml/badge.svg)](https://github.com/angelofv/template/actions/workflows/ci.yml)
[![CD](https://github.com/angelofv/template/actions/workflows/cd.yml/badge.svg)](https://github.com/angelofv/template/actions/workflows/cd.yml)
[![codecov](https://codecov.io/gh/angelofv/template/graph/badge.svg?token=RD0GRZMER0)](https://codecov.io/gh/angelofv/template)

> **A ready-to-use template for building, tracking and deploying your machine-learning side-projects.**
>
> Mix & match **Prefect 3** flows, **MLflow** tracking, **Kedro** data‑catalogs, **FastAPI** micro‑services, **Streamlit** demos, all shipped in reproducible **Docker** images and guarded by GitHub Actions **CI ↔ CD**.

---

## ✨ Highlights

|  Capability            |  What’s inside                  |  Why care?                                                   |
| ---------------------- | ------------------------------- | ------------------------------------------------------------ |
| Orchestration          | Prefect 3 `@flow` tasks         | Dependency graph, logs, retries & scheduling with zero infra |
| Experiment tracking    | MLflow file‑store (local)       | Tracking experiments, UI at `:5000`                          |
| Data management        | Kedro `DataCatalog`             | Declarative dataset layer (CSV, Parquet, Pickle…)            |
| Serving                | FastAPI (+ uvicorn) & Streamlit | From REST inference to interactive demo                      |
| Dev ergonomics         | Makefile, Ruff, Conda, Docker   | One‑liners & consistent environments                         |
| Quality gates          | pytest‑cov, Ruff, Codecov badge | Keep tech debt under control                                 |
| CI / CD                | GH Actions 🔁 GHCR + Trivy      | Push‑to‑image pipeline with security scan                    |

---
> **Heads-up 🖼️**
> The Streamlit dashboard is a template.  
> Personalise it by editing `services/app/app.py` **or** by exporting environment
> variables such as `PROFILE_NAME`, `PROFILE_DESC`, `PROFILE_AVATAR`, `LINK_GITHUB`, etc.

## ⚡ Quick start

### 0. Prerequisites

* **Python 3.10+**
* **Docker Desktop**
* (optional) **Conda** ≥ 4.10
* **Codecov** – create a free account at [Codecov](https://codecov.io/), enable your repository there, then add the resulting `CODECOV_TOKEN` as a secret in your GitHub repository settings.

### 1. Option A – Native (no Docker)

```bash
make create_environment   # conda env ‘template’ (1×)
conda activate template
make requirements         # pip install (1×)

make local-infra          # spin up MLflow (5000) + Prefect (4200)
make local-pipeline       # run full flow
make local-serve          # spin up API (8000) + Streamlit (8501)
# … hack, commit, profit! …
make local-down           # stop all local services
```

### 1. Option B – Docker‑first

```bash
make infra     # pull & spin up MLflow (5000) + Prefect (4200)
make pipeline  # build pipeline image & run full flow
make serve     # build & spin up API (8000) + Streamlit app (8501)

# same ports as native; tear‑down:
make down
```

> **TL;DR** – `docker compose up --build` launches *everything* at once (but loses the nice logs & coloured prompts our Makefile gives 🙃).

---

## 🛠️ Every‑day commands

| Command                                                        | Purpose                          |
| --------------------------------------                         | -------------------------------- |
| `make format`                                                  | Ruff‑format the entire code‑base |
| `make lint`                                                    | Ruff static analysis             |
| `make test`                                                    | pytest + coverage XML (Codecov)  |
| `make clean`                                                   | remove Python artefacts & caches |
| `make mlflow-clean`                                            | wipe local `mlruns/` folder      |
| `make infra / pipeline / serve / down`                         | Docker workflow helpers          |
| `make local-infra / local-pipeline / local-serve / local-down` | Local workflow helpers           |
---
> **Tip:** run `make help` to see *all* available targets and their descriptions.

## 🧪 Running tests locally

The tests expect the repo root to be on **PYTHONPATH** so that `import src` and `import services` resolve. Two paths:

1. **Use Makefile** (recommended) – already sets the env var:

   ```bash
   make test          # 🚦 all green
   ```
2. **Manual run** – export once per shell:

   ```bash
   export PYTHONPATH="$PWD:$PYTHONPATH"
   pytest -q          #   <1 s
   ```

> Got `ModuleNotFoundError: src`? You probably ran `pytest` from a parent directory **or** forgot the `PYTHONPATH` export.

---

## 📦 CI / CD pipeline (GitHub Actions)

* **CI workflow** `ci.yml` – on every push / PR
  1. Set‑up Python, cache pip.
  2. Install deps; run `make lint` & `make test`.
  3. Upload coverage to Codecov.
* **CD workflow** `cd.yml` – after successful CI
  1. Build multi‑stage image; push to **GHCR** (`:latest` + SHA).
  2. Scan with **Trivy** (fail on critical/high vulns).
  3. Spin‑up container & import package as smoke test.

Badges at the top of this file reflect the latest run status.

---

## 🗂 Project layout

```
├── src/            # Prefect tasks, model, plots
│   ├── preprocessing/
│   ├── modeling/
│   ├── plotting/
│   └── run.py
├── services/       # API (FastAPI) + frontend (Streamlit)
│   ├── api/
│   └── app/
├── configs/        # YAML configs + Kedro catalog
├── data/           # 01_raw / 02_processed / 03_models / 04_reports
├── notebooks/      # Exploratory stuff (ignored by Dockerfile)
├── Dockerfile      # Pipeline image (multi‑stage)
├── docker-compose.yaml
├── Makefile        # Dev utilities
└── tests/          # tiny unit + smoke suite
```

---

## ⚙️ Configuration

| File                         | Consumed by                    | Notes                     |
| ---------------------------- | ------------------------------ | ------------------------- |
| `configs/preprocessing.yaml` | `src.preprocessing.preprocess` | adjust cleaning steps     |
| `configs/modeling.yaml`      | `src.modeling.train_model`     | hyper‑parameters          |
| `configs/plotting.yaml`      | `src.plotting.plot_metrics`    | figure tuning             |
| `configs/catalog.yaml`       | Kedro `DataCatalog`            | logical names ↔ artefacts |

Override any path by exporting env vars `PREPROCESSING_CONFIG`, `MODELING_CONFIG`, … (see `src/config.py`).

---

## 🌐 Environment variables

All tasks read their configuration from **environment variables** first, then fall back to sane defaults. (Optional) Create a `.env` file at the repo root or export them in your shell.

| Variable                                         | Default                      | Component          | Purpose                                                                                        |
| ------------------------------------------------ | ---------------------------- | ------------------ | ---------------------------------------------------------------------------------------------- |
| `MLFLOW_TRACKING_URI`                            | `file:./mlruns`              | pipeline, API      | Where MLflow stores runs & artefacts (set to `http://host.docker.internal:5000` inside Docker) |
| `MLFLOW_EXPERIMENT`                              | `Default`                    | pipeline           | MLflow experiment name                                                                         |
| `PREFECT_API_URL`                                | `http://localhost:4200/api`  | pipeline           | Connect Prefect client to a remote server (`http://localhost:4200/api`)   |
| `PREPROCESSING_CONFIG`                           | `configs/preprocessing.yaml` | pipeline           | Custom YAML for cleaning steps                                                                 |
| `MODELING_CONFIG`                                | `configs/modeling.yaml`      | pipeline           | Hyper‑parameters YAML                                                                          |
| `PLOTTING_CONFIG`                                | `configs/plotting.yaml`      | pipeline           | Plot options YAML                                                                              |
| `MODEL_PATH`                                     | `data/03_models/model.pkl`   | FastAPI, Streamlit | Location of the pickled model used for inference                                               |
| `API_URL`                                        | `http://localhost:8000`      | Streamlit          | Endpoint for prediction requests                                                               |
| `PROFILE_NAME`, `PROFILE_DESC`, `PROFILE_LOC`, … | –                            | Streamlit          | Sidebar personalisation (avatar, links)                                                        |

---

## 🏗️ Extending

1. **Swap model** – edit `train_model()`; update config.
2. **Add task** – new `@flow` in appropriate module; wire in `src/run.py`.
3. **Ship notebooks** – mount inside the image or add to `Dockerfile` if you really need them.
4. **Deploy** – pull `ghcr.io/<user>/template:<tag>` on any container platform.

---

## 📜 License

Released under the **MIT License**. See [`LICENSE`](LICENSE) for full text.

