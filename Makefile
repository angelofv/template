# GLOBALS
PROJECT_NAME   = template
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python

# COMMANDS

## Install Python dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Delete all compiled Python files & tool caches
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache .ruff_cache

## Lint using ruff
.PHONY: lint
lint:
	ruff check .

## Format source code with ruff (autofix)
.PHONY: format
format:
	ruff check --fix .

## Run tests with pytest
.PHONY: test
test:
	$(PYTHON_INTERPRETER) -m pytest tests

## Run the Prefect pipeline (equivalent to `python -m src.main`)
.PHONY: run
run:
	$(PYTHON_INTERPRETER) -m src.main

## Set up a Conda environment (one‑liner convenience)
.PHONY: create_environment
create_environment:
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"


# PREFECT / MLFLOW
MLFLOW_URI  ?= file:./mlruns     # dossier backend MLflow local par défaut
MLFLOW_PORT ?= 5000              # port UI MLflow
SERVER_PORT ?= 4200              # port Prefect (API + UI)

## Alias: exécuter le flow (identique à `make run`)
.PHONY: pipeline
pipeline: run

## Démarre le serveur Prefect + UI sur http://127.0.0.1:$(SERVER_PORT)
.PHONY: prefect-ui
prefect-ui:
	prefect server start --host 127.0.0.1 --port $(SERVER_PORT)

## Arrête Prefect (Unix/macOS) – Windows: Ctrl‑C dans le terminal qui l'exécute
.PHONY: prefect-stop
prefect-stop:
	-pkill -f "prefect server start" || true

## Lance l'interface MLflow sur http://127.0.0.1:$(MLFLOW_PORT)
.PHONY: mlflow-ui
mlflow-ui:
	mlflow ui --backend-store-uri $(MLFLOW_URI) \
	          --host 127.0.0.1 --port $(MLFLOW_PORT)

## Réinitialise les expériences MLflow locales (supprime le dossier `mlruns`)
.PHONY: mlflow-clean
mlflow-clean:
	rm -rf $(MLFLOW_URI:file:=)

# Self‑Documenting Commands

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; lines = '\n'.join(sys.stdin)
for name, target in re.findall(r'## (.*)\n[^#]*?^([A-Za-z0-9_-]+):', lines, re.M):
    print(f"{target:<20} {name}")
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
