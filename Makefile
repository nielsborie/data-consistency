SHELL := /bin/bash
VERSION ?= $(shell cd .. && mvn help:evaluate -Dexpression=project.version -q -DforceStdout)
BRANCH_NAME ?= $(shell git branch | grep \* | cut -d ' ' -f2)
MODULE_NAME ?= streamlit-consistency
GIT_COMMIT ?= $(shell git rev-parse HEAD)
PYTHON_INTERPRETER = python3
PYTHON_VERSION = 3.10


REGISTRY_URL ?=
DOCKER_TAG_NAME = $(BRANCH_NAME)

ifeq ($(BRANCH_NAME), master)
	DOCKER_TAG_NAME = $(VERSION)
endif
ifeq ($(BRANCH_NAME), develop)
	DOCKER_TAG_NAME = $(VERSION)
endif

export REGISTRY_URL
export OPTIONAL_TAG:=:$(DOCKER_TAG_NAME)
export CONTAINER_NAME := "streamlit-consistency-$(shell date +"%Y%m%d-%H%M%S")"

.DEFAULT_GOAL:=help

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

docker-build: ## Build streamlit-consistency docker image
	docker build --force-rm -t ${REGISTRY_URL}/${MODULE_NAME}:${DOCKER_TAG_NAME} .
	docker tag ${REGISTRY_URL}/${MODULE_NAME}:${DOCKER_TAG_NAME} ${REGISTRY_URL}/${MODULE_NAME}:latest

docker-push: ## Push streamlit-consistency image to registry
	docker push ${REGISTRY_URL}/${MODULE_NAME}:${DOCKER_TAG_NAME}
	if [ "${BRANCH_NAME}" = "main" ]; then \
        docker push ${REGISTRY_URL}/${MODULE_NAME}:latest; \
    fi;

run: ## Run streamlit-consistency using docker image
	docker run -d -p 8501:8501 --rm --name streamlit-consistency ${REGISTRY_URL}/${MODULE_NAME}:latest

stop: ## Stop the streamlit-consistency container
	docker stop streamlit-consistency

run-locally:
	source activate ${PROJECT_NAME} && streamlit run dashboard.py --server.maxUploadSize=1028
