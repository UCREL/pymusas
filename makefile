.ONESHELL:
SHELL := /bin/bash

SRC = pymusas

WORKING_DIR = /home/node/website
CONTAINER_NAME = pymusas-docs:latest

DOCS_API_DIR = ./docs/docs/api
DOCS_SRC_TMP = $(filter-out $(SRC)/__main__.py %/__init__.py ,$(shell find $(SRC) -type f -name '*.py'))
DOCS_SRC = $(subst .py,,$(subst /,.,${DOCS_SRC_TMP}))

create-docs: build-docker-docs
	@docker run -it --name docusaurus ${CONTAINER_NAME} -c "npm init docusaurus@latest docs classic"
	@docker cp docusaurus:${WORKING_DIR}/docs ${PWD}/docs
	@docker rm -f docusaurus

develop-docs: install-package-for-docs
	@docker run -p 127.0.0.1:3000:3000 --rm -it -v ${PWD}:${WORKING_DIR} ${CONTAINER_NAME} -c "cd docs && yarn start -h 0.0.0.0"

build-docs: install-package-for-docs
	@docker run --rm -v ${PWD}:${WORKING_DIR} ${CONTAINER_NAME} -c "cd docs && yarn build"

serve-built-docs: build-docs
	@docker run -p 127.0.0.1:3000:3000 --rm -it -v ${PWD}:${WORKING_DIR} ${CONTAINER_NAME} -c " cd docs && yarn serve -h 0.0.0.0"

install-package-for-docs: build-docker-docs
	@docker run --rm -v ${PWD}/docs:${WORKING_DIR} ${CONTAINER_NAME} -c "cd docs && yarn install"

interactive: build-docker-docs
	@docker run -it --rm --name docusaurus -v ${PWD}:${WORKING_DIR} ${CONTAINER_NAME}

build-docker-docs:
	@docker build -t ${CONTAINER_NAME} -f Docs_Docker.dockerfile .

create-api-docs:
	@rm -rf ${DOCS_API_DIR}
	@python ./scripts/py2md.py ${DOCS_SRC}

build-python-package:
	@python -m pip install --upgrade pip
	@pip install --upgrade build twine
	@python -m build

check-twine: build-python-package
	@python -m twine check --strict dist/*

	