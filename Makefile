#################################################################################
# GLOBALS                                                                       #
#################################################################################

ENV_NAME        	= template
PYTHON_VERSION      = 3.10

# MLflow & Prefect settings
MLFLOW_URI          ?= ./mlruns
MLFLOW_PORT         ?= 5000
PREFECT_PORT        ?= 4200

# API & Frontend settings
API_PORT            ?= 8000
APP_PORT            ?= 8501
MODEL_PATH          ?= ./data/03_models/model.pkl

#################################################################################
# ENVIRONMENT & DEPENDENCIES                                                    #
#################################################################################

.PHONY: create_environment requirements clean lint format test help

create_env: ## Create a Conda env named $(ENV_NAME)
	conda create --name $(ENV_NAME) python=$(PYTHON_VERSION) -y
	@echo ">>> Environment created. Activate with: conda activate $(ENV_NAME)"

requirements: ## Install Python dependencies into active env
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

clean: ## Remove Python artifacts & caches
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache .ruff_cache
	rm -f .coverage tests/coverage.xml

mlflow-clean: ## Delete local mlruns directory
	rm -rf $(MLFLOW_URI)

lint: ## Lint code with ruff
	ruff check . --fix

format: ## Format code with ruff
	ruff format . && ruff check --fix .

test: ## Run pytest with coverage
	python -m pytest \
	  --rootdir=. \
	  --cov=src \
	  --cov-config=tests/.coveragerc \
	  --cov-report=xml:tests/coverage.xml \
	  --cov-report=term

#################################################################################
# LOCAL (NO DOCKER)                                                             #
#################################################################################

.PHONY: local-infra local-pipeline local-serve local-down

local-infra: ## Start MLflow & Prefect locally
	@echo "▶️  Launching MLflow server..."; \
	python -m mlflow server \
	  --backend-store-uri $(MLFLOW_URI) \
	  --artifacts-destination $(MLFLOW_URI) \
	  --serve-artifacts \
	  --host 0.0.0.0 \
	  --port $(MLFLOW_PORT) & \
	printf "   Waiting for MLflow"; \
	until curl -s http://localhost:$(MLFLOW_PORT)/ >/dev/null 2>&1; do printf "."; sleep 1; done; \
	echo " ✔ MLflow is up"; \
	\
	echo "▶️  Launching Prefect server..."; \
	prefect server start \
	  --host 0.0.0.0 \
	  --port $(PREFECT_PORT) & \
	printf "   Waiting for Prefect"; \
	until curl -s http://localhost:$(PREFECT_PORT)/api/health >/dev/null 2>&1; do printf "."; sleep 1; done; \
	echo " ✔ Prefect is up"; \
	\
	printf "\n👉 MLflow UI:   http://localhost:$(MLFLOW_PORT)\n"; \
	printf "👉 Prefect UI:  http://localhost:$(PREFECT_PORT)\n\n"

local-pipeline: ## Run pipeline locally (after local-infra)
	@echo "▶️  Launching pipeline …"
	@MLFLOW_TRACKING_URI=http://localhost:$(MLFLOW_PORT) \
	  PREFECT_API_URL=http://localhost:$(PREFECT_PORT)/api \
	  python -m src.run

local-serve: ## Start API & Streamlit locally (after local-pipeline)
	@echo "🚀  Starting API..." ; \
	MODEL_PATH=$(MODEL_PATH) python -m uvicorn services.api:app \
	  --host 0.0.0.0 --port $(API_PORT) & \
	echo -n "   Waiting for API" ; \
	until curl -s http://localhost:$(API_PORT)/health >/dev/null 2>&1; do echo -n "."; sleep 1; done ; \
	echo " ✔ API is up" ; \
	echo "🚀  Starting Streamlit..." ; \
	streamlit run services/app.py \
	  --server.address=0.0.0.0 --server.port=$(APP_PORT) & \
	echo -n "   Waiting for Streamlit" ; \
	until curl -s http://localhost:$(APP_PORT)/ >/dev/null 2>&1; do echo -n "."; sleep 1; done ; \
	echo " ✔ Streamlit is up" ; \
	printf "\n👉 API:        http://localhost:$(API_PORT)\n" ; \
	printf "👉 Streamlit:  http://localhost:$(APP_PORT)\n\n" ; \
	wait

local-down: ## Stop all local services by port
	@echo "🛑  Killing processes on ports $(MLFLOW_PORT), $(PREFECT_PORT), $(API_PORT), $(APP_PORT)…"
	-@lsof -ti tcp:$(MLFLOW_PORT)   | xargs -r kill
	-@lsof -ti tcp:$(PREFECT_PORT)  | xargs -r kill
	-@lsof -ti tcp:$(API_PORT)      | xargs -r kill
	-@lsof -ti tcp:$(APP_PORT)      | xargs -r kill

#################################################################################
# DOCKER                                                                        #
#################################################################################

.PHONY: infra pipeline serve down

infra: ## Start MLflow & Prefect via Docker
	docker compose up -d mlflow prefect
	@printf "⏳ Waiting for Prefect API… "
	@until curl -s http://localhost:$(PREFECT_PORT)/api/health >/dev/null; do \
	  printf "."; sleep 1; \
	done
	@echo " ✔ Ready!"
	@printf "\n👉 MLflow UI: http://localhost:$(MLFLOW_PORT)\n"
	@printf "👉 Prefect UI: http://localhost:$(PREFECT_PORT)\n\n"

pipeline: ## Run pipeline via Docker (after infra)
	@echo "▶️  Launching pipeline (Docker)…"
	docker compose build --pull pipeline
	docker compose up -d --no-deps pipeline
	docker compose logs -f --tail=0 pipeline | sed 's/host\.docker\.internal/localhost/g'

serve: ## Start API & Streamlit via Docker (after pipeline)
	@echo "🚀  Starting API & Streamlit (Docker)…"
	docker compose build api app
	docker compose up -d api app
	@printf "\n👉 API: http://localhost:$(API_PORT)\n"
	@printf "👉 Streamlit: http://localhost:$(APP_PORT)\n\n"

down: ## Stop & remove all Docker services & volumes
	@echo "→ Stopping and cleaning up Docker services…"
	docker compose down -v

#################################################################################
# HELP                                                                           #
#################################################################################

.DEFAULT_GOAL := help

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | \
	  awk -F':|##' '{printf "%-20s %s\n", $$1, $$NF}'