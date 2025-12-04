.ONESHELL:
SHELL := /bin/bash

SRC = pymusas

DOCS_API_DIR = ./docs/docs/api
DOCS_SRC_TMP = $(filter-out $(SRC)/__main__.py %/__init__.py ,$(shell find $(SRC) -type f -name '*.py'))
DOCS_SRC = $(subst .py,,$(subst /,.,${DOCS_SRC_TMP}))
VERSION_CMD = "uv run scripts/get_version.py ./pyproject.toml"


.PHONY: develop-docs
develop-docs: install-package-for-docs
	@cd docs
	@yarn start -h "0.0.0.0"

.PHONY: remove-built-docs
remove-built-docs:
	@cd docs
	@rm -rf build

docs/build: install-package-for-docs remove-built-docs
	@cd docs
	@rm -rf build
	@yarn build

.PHONY: serve-built-docs
serve-built-docs: install-package-for-docs docs/build
	@cd docs
	@yarn serve -h 0.0.0.0

.PHONY: install-package-for-docs
install-package-for-docs:
	@cd docs
	@yarn install

.PHONY: create-api-docs
create-api-docs:
	@rm -rf ${DOCS_API_DIR}
	@./scripts/py2md.py ${DOCS_SRC}

.PHONY: create-docs
create-docs:
	@npx create-docusaurus@latest new_docs classic --typescript
	@rm -rf ./new_docs/docs ./new_docs/blog ./new_docs/static/img ./new_docs/src/pages
	@mkdir ./new_docs/static/img
	@cp -r ./docs/static/img/* ./new_docs/static/img/.
	@cp ./docs/docusaurus.config.ts ./new_docs/.
	@cp ./docs/sidebars.ts ./new_docs/.
	@cp -r ./docs/docs ./new_docs/.
	@rm -rf ./docs
	@mv ./new_docs ./docs

.PHONY: build-python-package
build-python-package:
	@uv lock --check
	@rm -rf ./dist
	@uv build

.PHONY: functional-tests
functional-tests:
	@uv run --with dist/pymusas-$$("${VERSION_CMD}")-py3-none-any.whl \
	--with pytest --no-project --isolated pytest --doctest-modules pymusas/
	@uv run --with dist/pymusas-$$("${VERSION_CMD}")-py3-none-any.whl \
	--with pytest --no-project --isolated pytest tests/functional_tests

.PHONY: release-notes
release-notes:
	@uv run --no-project --script \
	--with dist/pymusas-$$("${VERSION_CMD}")-py3-none-any.whl \
	./scripts/release_notes.py

.PHONY: lint
lint:
	@echo "ISort:"
	@uv run isort pymusas tests scripts
	@echo "Falke 8:"
	@uv run flake8 --config ./.flake8 pymusas/** tests/** scripts/**
	@echo "MyPy:"
	@uv run mypy
	@echo "Linting finished"

.PHONY: tests
tests:
	@uv run coverage run
	@uv run coverage report

.PHONY: failed-tests
failed-tests:
	@uv run pytest --last-failed -vvv

.PHONY: verbose-tests
verbose-tests:
	@uv run pytest -vvv

.PHONY: doc-tests
doc-tests:
	@uv run coverage run -m pytest --doctest-modules pymusas/
	@uv run coverage report

	