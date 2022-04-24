################################################################################
# Docker and Docker Compose commands to be executed outside the container.     #
################################################################################

# Environment variables
# If the following required environment variables are not set,
# we try to get them from the .env file:

ifndef APP_VERSION
	APP_VERSION=$$(grep '^APP_VERSION=' .env | cut -d= -f2-)
endif

ifndef APP_NAME
	APP_NAME=$$(grep '^APP_NAME=' .env | cut -d= -f2-)
endif

ifndef APP_SITE_NAME
	APP_SITE_NAME=$$(grep '^APP_SITE_NAME=' .env | cut -d= -f2-)
endif

# Commands

default: help

.PHONY: clean-python
clean-python: ## Cleans Python environment.
	find . -path "*.pyc" -delete
	find . -path "*/__pycache__" -delete

.PHONY: build
build: clean-python ## Builds Docker image.
	docker build \
		--tag ${APP_NAME}:${APP_VERSION} \
		--tag ${APP_NAME}:latest \
		--tag ${APP_NAME}/${APP_NAME}:${APP_VERSION} \
		--tag ${APP_NAME}/${APP_NAME}:latest \
		--file services/core/Dockerfile \
		.
	@echo "[ OK ] The '${APP_NAME}/${APP_NAME}:${APP_VERSION}' image was build successfully!"

.PHONY: demo
demo: build ## Builds Docker image and runs it in demo mode.
	@docker run \
		--detach \
		--name ${APP_NAME}_demo \
		--rm \
		--env DEBUG=True \
		--env APP_SITE_NAME="${APP_SITE_NAME} (Demo)" \
		--env APP_LANGUAGE_CODE=en \
		--env DJANGO_SUPERUSER_USERNAME=demo \
		--env DJANGO_SUPERUSER_PASSWORD=demo \
		--env DJANGO_SUPERUSER_EMAIL=demo@example.com \
		--publish 127.0.0.1:8000:8000 \
		--entrypoint \
		make \
		${APP_NAME}:latest \
		-C \
		/code/services/core \
		demo
	@echo "[ OK ] '${APP_NAME}_demo' is running on http://localhost:8000"
	@echo "[INFO] You can log in with 'demo' / 'demo'."
	@echo "[INFO] Please use 'make stop' to stop the running '${APP_NAME}_demo' application."

.PHONY: stop
stop: ## Stops the runing demo application.
	@docker stop ${APP_NAME}_demo
	@echo "[ OK ] '${APP_NAME}_demo' is stopped and deleted."

.PHONY: quickstart
quickstart: build ## Builds Docker image and runs it in production mode using Docker Compose.
	docker-compose \
		--file docker-compose.yml \
		--project-name ${APP_NAME}_prod \
		up \
		--build \
		--remove-orphans \
		--renew-anon-volumes

.PHONY: clean-quickstart
clean-quickstart: ## Cleans production environment (Docker containers and volumes).
	docker rm ${APP_NAME}_prod_reverse-proxy_1; exit 0
	docker rm ${APP_NAME}_prod_core_1; exit 0
	docker rm ${APP_NAME}_prod_core-worker-gateway_1; exit 0
	docker rm ${APP_NAME}_prod_core-worker-computation_1; exit 0
	docker rm ${APP_NAME}_prod_core-db_1; exit 0
	docker rm ${APP_NAME}_prod_brocker_1; exit 0
	docker rm ${APP_NAME}_prod_cache_1; exit 0
	docker volume rm ${APP_NAME}_prod_core-media; exit 0
	docker volume rm ${APP_NAME}_prod_core-static; exit 0
	docker volume rm ${APP_NAME}_prod_core-db-data; exit 0
	docker volume rm ${APP_NAME}_prod_brocker-data; exit 0
	docker volume rm ${APP_NAME}_prod_cache-data; exit 0

.PHONY: dev
dev: clean-python ## Runs all services in development mode.
	mkdir -p services/core/.tox
	mkdir -p services/core/media
	mkdir -p services/core/static
	mkdir -p services/core/venv
	mkdir -p services/frontend/node_modules
	docker-compose \
		--file docker-compose.yml \
		--file docker-compose.override.yml \
		--project-name ${APP_NAME}_dev \
		up \
		--build \
		--remove-orphans \
		--renew-anon-volumes

.PHONY: tests
tests: ## Tests Docker image.
	docker exec -it ${APP_NAME}_dev_core_1 make -C /code/services/core tests

.PHONY: clean-dev
clean-dev: clean-python ## Cleans development environment (Docker containers and volumes).
	docker rm ${APP_NAME}_dev_reverse-proxy_1; exit 0
	docker rm ${APP_NAME}_dev_core_1; exit 0
	docker rm ${APP_NAME}_dev_core-worker-gateway_1; exit 0
	docker rm ${APP_NAME}_dev_core-worker-computation_1; exit 0
	docker rm ${APP_NAME}_dev_core-db_1; exit 0
	docker rm ${APP_NAME}_dev_brocker_1; exit 0
	docker rm ${APP_NAME}_dev_cache_1; exit 0
	docker rm ${APP_NAME}_dev_frontend_1; exit 0
	docker volume rm ${APP_NAME}_dev_core-media; exit 0
	docker volume rm ${APP_NAME}_dev_core-static; exit 0
	docker volume rm ${APP_NAME}_dev_core-db-data; exit 0
	docker volume rm ${APP_NAME}_dev_brocker-data; exit 0
	docker volume rm ${APP_NAME}_dev_cache-data; exit 0
	docker volume rm ${APP_NAME}_dev_core-venv; exit 0
	docker volume rm ${APP_NAME}_dev_core-tox; exit 0
	docker volume rm ${APP_NAME}_dev_frontend-node_modules; exit 0
	rm -rf services/core/.tox
	rm -rf services/core/media
	rm -rf services/core/static
	rm -rf services/core/venv
	rm -rf services/frontend/node_modules

.PHONY: clean-dev-db
clean-dev-db: ## Cleans development databases (Docker containers and volumes).
	docker rm ${APP_NAME}_dev_core-db_1; exit 0
	docker rm ${APP_NAME}_dev_brocker_1; exit 0
	docker rm ${APP_NAME}_dev_cache_1; exit 0
	docker volume rm ${APP_NAME}_dev_brocker-data; exit 0
	docker volume rm ${APP_NAME}_dev_cache-data; exit 0
	docker volume rm ${APP_NAME}_dev_core-db-data; exit 0

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
