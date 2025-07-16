# Template – ML Pipeline Starter

[![CI](https://github.com/angelofv/template/actions/workflows/ci.yml/badge.svg)](https://github.com/angelofv/template/actions/workflows/ci.yml)
[![CD](https://github.com/angelofv/template/actions/workflows/cd.yml/badge.svg)](https://github.com/angelofv/template/actions/workflows/cd.yml)
[![codecov](https://codecov.io/gh/angelofv/template/graph/badge.svg?token=RD0GRZMER0)](https://codecov.io/gh/angelofv/template)

> **A ready‑to‑use scaffold for building, tracking and deploying small machine‑learning projects.**
>
> Mix & match **Prefect 3** flows, **MLflow** tracking, **Kedro** data‑catalogs, **FastAPI** micro‑services and **Streamlit** demos – all shipped in reproducible **Docker** images and guarded by GitHub Actions **CI ↔ CD**.

---

## ✨ Highlights

| Capability       | What’s inside                   | Why care?                                                            |
| ---------------- | ------------------------------- | -------------------------------------------------------------------- |
| Orchestration    | Prefect 3 `@flow` tasks         | Dependency graph, logs, retries & scheduling **without extra infra** |
| Experiment track | MLflow file‑store (local)       | Compare runs; rich UI exposed at port `5000`                         |
| Data layer       | Kedro `DataCatalog`             | Declarative datasets (CSV, Parquet, Pickle …)                        |
| Serving          | FastAPI (+ uvicorn) & Streamlit | From REST inference to an interactive playground                     |
| Dev ergonomics   | Makefile, Ruff, Conda, Docker   | One‑liners & consistent environments                                 |
| Quality gates    | pytest‑cov, Ruff, Codecov badge | Keep tech‑debt under control                                         |
| CI / CD          | GH Actions ⇆ GHCR + Trivy       | Push‑to‑image pipeline with security scans                           |

---

> **Heads‑up 🖼️**
> The Streamlit dashboard is only a starting point.
> Make it yours by editing `services/app.py` **or** by exporting environment variables such as `PROFILE_NAME`, `PROFILE_DESC`, `PROFILE_AVATAR`, `LINK_GITHUB`, etc.

---

## ⚡ Quick start

### 0. Prerequisites

* **Python 3.10+**
* **Docker Desktop** (or Podman/Colima)
* (optional) **Conda** ≥ 4.10
* **Codecov** – create a free account, enable your repo and add `CODECOV_TOKEN` as a secret in **Settings → Secrets → Actions**.

### 1‑A. Native workflow (no Docker)

```bash
make create_env          # conda env ‘template’ (one‑shot)
conda activate template
make requirements        # pip install

make local-infra         # spin‑up MLflow :5000 + Prefect :4200
make local-pipeline      # run full flow
make local-serve         # start API :8000 + Streamlit :8501
# … hack, commit, profit! …
make local-down          # stop all local services
```

### 1‑B. Docker‑first workflow

```bash
make infra      # spin‑up MLflow + Prefect in containers
make pipeline   # build pipeline image & run full flow
make serve      # build & start API + Streamlit

# Tear‑down
make down
```

<details>
<summary>TL;DR</summary>

```bash
docker compose up --build
```

`docker compose` will launch everything, but you will lose the pretty, colour‑coded logs provided by the Makefile 🙃.

</details>

---

## 🛠️ Every‑day commands

| Command                                                        | Purpose                                   |
| -------------------------------------------------------------- | ----------------------------------------- |
| `make format`                                                  | Auto‑format the whole code‑base with Ruff |
| `make lint`                                                    | Static analysis                           |
| `make test`                                                    | pytest + coverage                         |
| `make clean`                                                   | Remove Python artefacts & caches          |
| `make mlflow-clean`                                            | Wipe local `mlruns/` folder               |
| `make infra / pipeline / serve / down`                         | **Docker** helpers                        |
| `make local-infra / local-pipeline / local-serve / local-down` | **Native** helpers                        |

Run `make help` to see every available target and its description.

---

## 🧪 Running tests locally

Tests require the repo root on **PYTHONPATH** so that `import src` resolves.

```bash
make test                # recommended – sets env var automatically
```

If you must, run manually:

```bash
export PYTHONPATH="$PWD:$PYTHONPATH"
pytest -q
```

> `ModuleNotFoundError: src`? Check the current working directory or `$PYTHONPATH`.

---

## 📦 CI / CD pipeline (GitHub Actions)

* **ci.yml** – on every push / PR
  1. Set‑up Python & cache pip
  2. `make lint` & `make test`
  3. Upload coverage to Codecov
* **cd.yml** – after successful CI
  1. Build multi‑stage image; push to **GHCR** (`:latest` + SHA)
  2. Scan with **Trivy** (fail on critical/high vulns)
  3. Run smoke test (`import src`) inside the container

Badges at the top of this file always reflect the last run.

---

## 🗂 Project layout

```
├── src/                  # Prefect flows, model, plotting
│   ├── extract.py        # load_raw_data & preprocess tasks
│   ├── train.py          # train_model task
│   ├── plot_metrics.py   # plot_metrics task
│   └── run.py            # orchestrates the flow
├── services/             # FastAPI (api.py) & Streamlit (app.py)
├── configs/              # config.yaml + Kedro catalog
├── data/                 # 01_raw / 02_processed / 03_models / 04_reports
├── notebooks/            # Exploratory notebooks (ignored by Docker)
├── Dockerfile            # Multi‑stage build (pipeline / api / app)
├── docker-compose.yaml
├── Makefile              # Dev helpers
└── tests/                # tiny unit + smoke suite
```

---

## ⚙️ Configuration

All pipeline tunables live in a single YAML file:

| File                  | Consumed by                            | Notes               |
| --------------------- | -------------------------------------- | ------------------- |
| `configs/config.yaml` | every Prefect task via `load_config()` | See `src/config.py` |

Override the path by exporting `CONFIG_PATH`.

The Kedro **DataCatalog** is defined in `configs/catalog.yaml`.

---

## 🌐 Environment variables

Tasks read their configuration from **environment variables** first, then fall back to defaults. Create a `.env` file or export them in your shell.

| Variable              | Default                     | Component          | Purpose                              |
| --------------------- | --------------------------- | ------------------ | ------------------------------------ |
| `MLFLOW_TRACKING_URI` | `file:./mlruns`             | pipeline, API      | Where MLflow stores runs & artefacts |
| `MLFLOW_EXPERIMENT`   | `Default`                   | pipeline           | MLflow experiment name               |
| `PREFECT_API_URL`     | `http://localhost:4200/api` | pipeline           | Prefect REST endpoint                |
| `MODEL_PATH`          | `data/03_models/model.pkl`  | FastAPI, Streamlit | Pickled model used for inference     |
| `API_URL`             | `http://localhost:8000`     | Streamlit          | Endpoint for prediction requests     |
| `PROFILE_*`, `LINK_*` | –                           | Streamlit          | Dashboard personalisation            |

---

## 🏗️ Extending

1. **Change the model** – edit `train_model()` and add hyper‑params to `config.yaml`.
2. **Add new tasks** – write a Prefect `@flow` function and wire it in `src/run.py`.
3. **Ship notebooks** – mount them inside the image or copy in `Dockerfile` when needed.
4. **Deploy** – pull `ghcr.io/<user>/template:<tag>` on any container platform.

---

## 📜 License

Released under the **MIT License** – see [`LICENSE`](LICENSE) for details.
