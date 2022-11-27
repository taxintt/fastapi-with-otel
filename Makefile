.PHONY: help
help: ## Display the descriptions of make tasks
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | sed -e 's/^Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1,$$2}'


.PHONY: all
all: test lint


.PHONY: lint
lint:  ## Run linter
	poetry run pre-commit run --all-files


.PHONY: test
test:  ## Run test
	poetry run tox


.PHONY: pytest
pytest:  ## Run pytest
	PYTHONPATH=src poetry run pytest tests -x --ff --cov=src --cov-report html


.PHONY: distclean
distclean:  ## Clean up environment
	rm -rf build dist src/*.egg-info .tox .mypy_cache .pytest_cache .coverage .coverage.* htmlcov
	find src tests -name __pycache__ -type d | xargs rm -rf __pycache__
