.ONESHELL:
SHELL := /bin/bash

WORKING_DIR = /home/node/website
CONTAINER_NAME = pymusas-docs:latest

create-docs: build-docker-docs
	@docker run -it --name docusaurus ${CONTAINER_NAME} -c "npm init docusaurus@latest docs classic"
	@docker cp docusaurus:${WORKING_DIR}/docs ${PWD}/docs
	@docker rm -f docusaurus

develop-docs: build-docker-docs
	@docker run -p 127.0.0.1:3000:3000 --rm -it -v ${PWD}/docs:${WORKING_DIR} ${CONTAINER_NAME} -c "yarn start -h 0.0.0.0"

build-docs: build-docker-docs
	@docker run --rm -v ${PWD}/docs:${WORKING_DIR} ${CONTAINER_NAME} -c "yarn build"

serve-built-docs: build-docs
	@docker run -p 127.0.0.1:3000:3000 --rm -it -v ${PWD}/docs:${WORKING_DIR} ${CONTAINER_NAME} -c "yarn serve -h 0.0.0.0"

install-package-for-docs: build-docker-docs
	@docker run --rm -v ${PWD}/docs:${WORKING_DIR} ${CONTAINER_NAME} -c "yarn install"

interactive: build-docker-docs
	@docker run -it --rm --name docusaurus -v ${PWD}/docs:${WORKING_DIR} ${CONTAINER_NAME}

build-docker-docs:
	@docker build -t ${CONTAINER_NAME} -f Docs_Docker.dockerfile .