#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME   = template
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

.PHONY: requirements clean lint format test run create_environment \
        pipeline prefect-ui prefect-stop mlflow-ui mlflow-clean help

requirements: ## Install Python dependencies
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

clean: ## Delete compiled Python files & caches
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache .ruff_cache

lint: ## Lint using ruff
	ruff check .

format: ## Auto‑format code with ruff
	ruff check --fix .

test: ## Run unit tests with pytest
	$(PYTHON_INTERPRETER) -m pytest tests

run: ## Run the Prefect pipeline (python -m src.main)
	$(PYTHON_INTERPRETER) -m src.main

create_environment: ## Create a Conda env $(PROJECT_NAME)
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"

#################################################################################
# PREFECT / MLFLOW                                                              #
#################################################################################

MLFLOW_URI  ?= file:./mlruns     # MLflow backend dir
MLFLOW_PORT ?= 5000              # MLflow UI port
SERVER_PORT ?= 4200              # Prefect server port
MLFLOW_DIR := $(patsubst file:%,%,$(MLFLOW_URI))

prefect-ui: ## Start Prefect server + UI
	prefect server start --host 127.0.0.1 --port $(SERVER_PORT)

mlflow-ui: ## Launch MLflow UI
	mlflow ui --backend-store-uri $(MLFLOW_URI) \
	          --host 127.0.0.1 --port $(MLFLOW_PORT)

mlflow-clean: ## Delete local mlruns directory
	rm -rf "$(MLFLOW_DIR)"

#################################################################################
# Self‑documenting help                                                         #
#################################################################################

.DEFAULT_GOAL := help

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | \
	  awk -F':|##' '{printf "%-18s %s\n", $$1, $$NF}'
