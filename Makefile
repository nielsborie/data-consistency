SHELL := /bin/bash
BRANCH_NAME ?= $(shell git branch | grep \* | cut -d ' ' -f2)
PROJECT_NAME ?= streamlit-data-consistency
GIT_COMMIT ?= $(shell git rev-parse HEAD)
PYTHON_INTERPRETER = python3
PYTHON_VERSION = 3.10

REGISTRY_URL ?= nielsborie
DOCKER_TAG_NAME = $(BRANCH_NAME)
export REGISTRY_URL

.DEFAULT_GOAL:=help

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

docker-build: ## Build streamlit-data-consistency docker image
	docker build --force-rm -t ${REGISTRY_URL}/${PROJECT_NAME}:${DOCKER_TAG_NAME} .
	docker tag ${REGISTRY_URL}/${PROJECT_NAME}:${DOCKER_TAG_NAME} ${REGISTRY_URL}/${PROJECT_NAME}:latest

docker-push: ## Push streamlit-data-consistency image to registry
	docker push ${REGISTRY_URL}/${PROJECT_NAME}:${DOCKER_TAG_NAME}
	if [ "${BRANCH_NAME}" = "main" ]; then \
        docker push ${REGISTRY_URL}/${PROJECT_NAME}:latest; \
    fi;

run: ## Run streamlit-data-consistency using docker image
	docker run -d -p 8501:8501 --rm --name streamlit-data-consistency ${REGISTRY_URL}/${PROJECT_NAME}:latest

stop: ## Stop the streamlit-data-consistency container
	docker stop streamlit-data-consistency

run-locally:
	source activate ${PROJECT_NAME} && streamlit run dashboard.py --server.maxUploadSize=1028
