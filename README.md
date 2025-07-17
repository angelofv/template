# Template – ML Pipeline Starter

[![CI](https://github.com/angelofv/template/actions/workflows/ci.yml/badge.svg)](https://github.com/angelofv/template/actions/workflows/ci.yml)
[![CD](https://github.com/angelofv/template/actions/workflows/cd.yml/badge.svg)](https://github.com/angelofv/template/actions/workflows/cd.yml)
[![codecov](https://codecov.io/gh/angelofv/template/graph/badge.svg?token=RD0GRZMER0)](https://codecov.io/gh/angelofv/template)

> **A ready‑to‑use scaffold for building, tracking, and deploying small machine‑learning projects.**
>
> Mix & match **Prefect 3** flows, **MLflow** tracking, **Kedro** data catalogues, **FastAPI** micro‑services, and **Streamlit** demos — all shipped in reproducible **Docker** images and guarded by GitHub Actions **CI / CD**.

---

## ✨ Highlights

| Capability          | What’s inside                   | Why care?                                                            |
| ------------------- | ------------------------------- | -------------------------------------------------------------------- |
| Orchestration       | Prefect 3 `@flow` tasks         | Dependency graph, logs, retries & scheduling **without extra infra** |
| Experiment tracking | MLflow *file store* (local)     | Compare runs; rich UI served on port `5000`                          |
| Data layer          | Kedro `DataCatalog`             | Declarative datasets (CSV, Parquet, Pickle …)                        |
| Serving             | FastAPI (+ uvicorn) & Streamlit | From REST inference to an interactive playground                     |
| Dev ergonomics      | Makefile, Ruff, Conda, Docker   | One‑liners & consistent environments                                 |
| Quality gates       | pytest‑cov, Ruff, Codecov badge | Keep tech‑debt under control                                         |
| CI / CD             | GitHub Actions ⇆ GHCR + Trivy   | Push‑to‑image pipeline with security scans                           |

---

## ⚡ Quick‑start

### 0. Prerequisites

* **Python 3.10+**
* **Docker Desktop** (or Podman/Colima)
* (optional) **Conda** ≥ 4.10
* **Codecov** – create a free account, enable your repository, and add a `CODECOV_TOKEN` secret under **Settings → Secrets → Actions**.

### 1‑A. Local workflow (no Docker)

```bash
make create_env          # one‑shot Conda env ‘template’
conda activate template
make requirements        # install Python deps

make local-infra         # spin up MLflow :5000 + Prefect :4200
make local-pipeline      # run the full flow
make local-serve         # start API :8000 + Streamlit :8501
# … hack, commit, profit! …
make local-down          # stop all local services
```

### 1‑B. Docker‑first workflow

```bash
make infra      # spin up MLflow + Prefect in containers
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

`docker compose` will launch *everything*, but you will lose the pretty, colour‑coded logs provided by the Makefile 🙃.

</details>

---

## 🛠️ Every‑day commands

| Command                                                        | Purpose                                   |
| -------------------------------------------------------------- | ----------------------------------------- |
| `make format`                                                  | Auto‑format the whole code‑base with Ruff |
| `make lint`                                                    | Static analysis                           |
| `make test`                                                    | pytest + coverage                         |
| `make clean`                                                   | Remove Python artifacts & caches          |
| `make mlflow-clean`                                            | Wipe local `mlruns/` folder               |
| `make infra / pipeline / serve / down`                         | **Docker** helpers                        |
| `make local-infra / local-pipeline / local-serve / local-down` | **Local** helpers                         |

Run `make help` to list every available target and its description.

---

## 🧪 Running tests locally

Tests require the repository root on **PYTHONPATH** so that `import src` resolves.

```bash
make test
```

If you must, run manually:

```bash
python -m pytest -q
```

---

## 📦 CI / CD pipeline (GitHub Actions)

* **ci.yml** – on every push / PR
  1. Set up Python & cache pip
  2. `make lint` & `make test`
  3. Upload coverage to Codecov
* **cd.yml** – after a successful CI
  1. Build a multi‑stage image & push to **GHCR** (`:latest` + SHA)
  2. Scan with **Trivy** (fail on critical / high vulnerabilities)
  3. Run a smoke test (`import src`) inside the container

Badges at the top of this file always reflect the latest run.

---

## 🗂 Project layout

```
├── README.md
├── Dockerfile             # Multi‑stage build (pipeline / api / app)
├── docker-compose.yaml    # Local orchestration
├── Makefile               # Dev helpers
├── pyproject.toml         # Project metadata (PEP 621)
├── requirements.txt       # Runtime + dev Python deps
├── .dockerignore
├── LICENSE
├── configs/               # Global YAML config + Kedro DataCatalog
│   ├── catalog.yaml
│   └── config.yaml
├── data/                  # 01_raw / 02_processed / 03_models / 04_reports
├── notebooks/             # Exploratory notebooks (ignored by Docker)
│   └── 00_exploration.ipynb
├── app/              # User‑facing layers
│   ├── api.py             # FastAPI inference service
│   └── app.py             # Streamlit demo UI
├── src/                   # Pipeline code (Prefect flows, modelling, utils)
│   ├── __init__.py
│   ├── config.py
│   ├── extract.py
│   ├── train.py
│   ├── plot_metrics.py
│   └── run.py
├── tests/                 # Unit & smoke tests
│   ├── test_modeling.py
│   ├── test_plotting.py
│   ├── test_preprocessing.py
│   ├── test_services.py
│   └── .coveragerc
└── .github/workflows/     # CI / CD definitions
    ├── ci.yml
    └── cd.yml
```

---

## ⚙️ Configuration

All pipeline tunables live in a single YAML file:

| File                  | Consumed by                            | Notes               |
| --------------------- | -------------------------------------- | ------------------- |
| `configs/config.yaml` | every Prefect task via `load_config()` | See `src/config.py` |

The Kedro **DataCatalog** is defined in `configs/catalog.yaml`.

---

## 🏗️ Extending

1. **Change the model** – edit `train_model()` and add hyper‑params to `config.yaml`.
2. **Add new tasks** – write a Prefect `@flow` function and wire it up in `src/run.py`.
3. **Ship notebooks** – mount them inside the image or copy them in the `Dockerfile` when needed.
4. **Deploy** – pull `ghcr.io/<user>/template:<tag>` on any container platform.

---

## 📜 License

Released under the **MIT License** – see [`LICENSE`](LICENSE) for details.
