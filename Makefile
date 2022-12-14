UID := $(shell id -u)
DKR_CMP := env UID=$(UID) docker-compose --project-directory=.

define dkr_cmp
	$(DKR_CMP) --env-file=docker/$1/compose.env $2
endef

.PHONY: help
help: ## Display the descriptions of make tasks
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | sed -e 's/^Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1,$$2}'


.PHONY: build-local
build-local: ## build local
	env COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILD_KIT=1 $(DKR_CMP) --env-file=docker/local/compose.env build --pull

.PHONY: freshup-local
freshup-local: ## freshup local env
	poetry env remove --all
	poetry config virtualenvs.in-project true --local
	poetry install

.PHONY: local
local: ## run local env
	$(DKR_CMP) --env-file=docker/local/compose.env up --remove-orphans

# https://cocoatomo.github.io/poetry-ja/cli/#export
.PHONY: build-requirements
build-requirements:  ## Export requirements
	poetry export -f requirements.txt --output requirements/requirements.txt

.PHONY: build-requirements-dev
build-requirements-dev:  ## Export requirements includes dev packages
	poetry export -f requirements.txt --with dev --output requirements/requirements-dev.txt


.PHONY: all
all: test lint


.PHONY: lint
lint:  ## Run linter
	poetry run pre-commit run --all-files


.PHONY: test
test:  ## Run test
	poetry run tox


.PHONY: deploy
deploy:  ## Run gcloud run deploy command (e.g. make deploy PROJECT=${gcp_project_id})
	 gcloud builds submit --region=us-central1 --project=$(PROJECT)


.PHONY: pytest
pytest:  ## Run pytest
	PYTHONPATH=app/src poetry run pytest tests -x --ff
	# PYTHONPATH=app/src poetry run pytest tests -x --ff --cov=app/src --cov-report html


.PHONY: distclean
distclean:  ## Clean up environment
	rm -rf build dist app/src/*.egg-info .tox .mypy_cache .pytest_cache .coverage .coverage.* htmlcov
	find app/src tests -name __pycache__ -type d | xargs rm -rf __pycache__
