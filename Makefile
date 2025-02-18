SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PYPROJECT_TOML := pyproject.toml
PYPI_VERSION := 0.1.7
PYTHON_VERSION := 3.11
TARGET := src/pdflex tests
TARGET_TEST := tests
DIST_NAME := dist/pdflex-$(PYPI_VERSION)-py3-none-any.whl


# -- Clean ---------------------------


.PHONY: clean
clean: ## Clean build and virtual environment directories
	@echo -e "\n► Cleaning up project environment and directories..."
	-rm -rf dist/ .venv/ build/ *.egg-info/
	-find . -name "__pycache__" -type d -exec rm -rf {} +
	-find . -name "*.pyc" -type f -exec rm -f {} +


# -- Dev ---------------------------


.PHONY: build
build: ## Build the distribution package using uv
	@echo "Distribution Name: $(DIST_NAME)..."
	uv build
	uv pip install $(DIST_NAME)

.PHONY: install
install: ## Install all dependencies from pyproject.toml
	uv sync --dev --group test --group docs --group lint --all-extras

.PHONY: lock
lock: ## Lock dependencies declared in pyproject.toml
	uv pip compile $(PYPROJECT_TOML) --all-extras

.PHONY: requirements
requirements: ## Generate requirements files from pyproject.toml
	uv pip compile $(PYPROJECT_TOML) -o requirements.txtiu
	uv pip compile $(PYPROJECT_TOML) --all-extras -o requirements-dev.txt

.PHONY: sync
sync: ## Sync environment with pyproject.toml
	uv sync --all-groups --dev

.PHONY: update
update: ## Update all dependencies from pyproject.toml
	uv lock --upgrade

.PHONY: venv
venv: ## Create a virtual environment
	uv venv --python $(PYTHON_VERSION)


# -- Docs ---------------------------


.PHONY: docs
docs: ## Build documentation site using mkdocs
	@echo -e "\n► Building documentation site... (not implemented)"


# -- Lint ---------------------------


.PHONY: format-toml
format-toml: ## Format TOML files using pyproject-fmt
	uvx --isolated pyproject-fmt $(TOML_FILE) --indent 4

.PHONY: format
format: ## Format Python files using Ruff
	@echo -e "\n► Running the Ruff formatter..."
	uvx --isolated ruff format $(TARGET) --config .ruff.toml

.PHONY: lint
lint: ## Lint Python files using Ruff
	@echo -e "\n ►Running the Ruff linter..."
	uvx --isolated ruff check $(TARGET) --fix --config .ruff.toml

.PHONY: format-and-lint
format-and-lint: format lint ## Format and lint Python files

.PHONY: typecheck-mypy
typecheck-mypy: ## Type-check Python files using MyPy
	uv run mypy $(TARGET)

.PHONY: typecheck-pyright
typecheck-pyright: ## Type-check Python files using Pyright
	uv run pyright $(TARGET)


# -- Release ----------------------------


RELEASE_FILES ?= .
RELEASE_MSG   ?= "Add pymupdf dependency, release $(PYPI_VERSION)"
RELEASE_BRANCH ?= main
TAG_PREFIX    ?= v

.PHONY: release
release:  ## Create and push a new version release
ifndef version
	$(error version parameter is required. Use 'make release version=X.Y.Z')
endif
	# make release version=1.2.3 RELEASE_FILES="file1 file2" RELEASE_MSG="Custom release message" RELEASE_BRANCH=develop TAG_PREFIX=release-"
	@echo "Creating release version $(PYPI_VERSION)..."
	@git add $(RELEASE_FILES)
	@git commit -m "$(RELEASE_MSG)"
	@git tag -a $(TAG_PREFIX)$(PYPI_VERSION) -m "$(RELEASE_MSG)"
	@git push origin $(RELEASE_BRANCH)
	@git push origin $(TAG_PREFIX)$(PYPI_VERSION)


# -- Tests ----------------------------


.PHONY: test
test: ## Run test suite using Pytest
	uv run pytest $(TARGET_TEST) --config-file $(PYPROJECT_TOML)


# -- Utils ---------------------------


.PHONY: convert-slides
convert-slides: ## Convert slides to PDF
	@echo -e "\n► Converting slides to PDF..."
	python \
		src/pdflex/slides_to_text.py tests/data/slide-deck-math.pdf \
		--output .pdflex/convert/30-slides-to-text.txt


.PHONY: help
help: ## Display this help
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "; printf "\033[1m%-20s %-50s\033[0m\n", "Target", "Description"; \
	              printf "%-20s %-50s\n", "------", "-----------";} \
	      /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %-50s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
