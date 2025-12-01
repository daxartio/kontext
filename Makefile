.DEFAULT_GOAL := help
CODE = kontext tests examples
UV_RUN = uv run --group dev
TEST = $(UV_RUN) pytest $(args)

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: format lint test  ## Run format lint test

.PHONY: install
install:  ## Install dependencies
	uv sync --group dev

.PHONY: publish
publish:  ## Publish package
	uv build
	uv publish --username=$(pypi_username) --password=$(pypi_password)

.PHONY: test
test:  ## Test with coverage
	$(TEST) --cov=./

.PHONY: test-fast
test-fast:  ## Test until error
	$(TEST) --exitfirst

.PHONY: test-failed
test-failed:  ## Test failed
	$(TEST) --last-failed

.PHONY: test-report
test-report:  ## Report testing
	$(TEST) --cov --cov-report html
	$(POETRY_RUN) python -m webbrowser 'htmlcov/index.html'

.PHONY: lint
lint:  ## Check code
	$(UV_RUN) ruff check $(CODE)
	$(UV_RUN) ruff format $(CODE) --check
	$(UV_RUN) mypy $(CODE)

.PHONY: format
format:  ## Formatting code
	$(UV_RUN) ruff format $(CODE)

.PHONY: bump
bump:  ## Bump version (commit and tag)
	$(UV_RUN) cz bump

.PHONY: clean
clean:  ## Clean
	rm -rf site || true
	rm -rf dist || true
	rm -rf htmlcov || true
