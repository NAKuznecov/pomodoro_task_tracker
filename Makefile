SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000

run-uvicorn: ## Run the application using uvicorn with provided arguments or defaults
	poetry run uvicorn app.main:app --host $(HOST) --port $(PORT) --reload --env-file .local.env

run:
	poetry run gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker -c gunicorn_conf.py

install:  ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

migration-create:
	alembic revision --autogenerate -m '$(DESC)'

migration-apply:
	alembic upgrade head


help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands: "
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $1, $2}'