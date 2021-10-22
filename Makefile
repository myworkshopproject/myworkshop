MYAPP_INSTANCE_NAME := $(if $(MYAPP_INSTANCE_NAME),$(MYAPP_INSTANCE_NAME),"myworkshop")
default: help

.PHONY: quickstart
quickstart: ## Runs a demo app.
	docker-compose -p myworkshop \
		-f docker-compose.yml \
		-f docker-compose.override.yml \
		up \
		--build \
		--remove-orphans \
		--renew-anon-volumes

.PHONY: clean-quickstart
clean-quickstart: ## Cleans quickstart environment (Docker containers and volumes).
	docker rm myworkshop_reverse-proxy_1; exit 0
	docker rm myworkshop_db_1; exit 0
	docker rm myworkshop_brocker_1; exit 0
	docker rm myworkshop_core_1; exit 0
	docker rm myworkshop_worker_1; exit 0
	docker volume rm myworkshop_quickstart_db-data; exit 0
	docker volume rm myworkshop_quickstart_brocker-data; exit 0
	docker volume rm myworkshop_quickstart_core-media; exit 0

.PHONY: dev
dev: ## Runs all services in development mode.
	docker-compose -p $(MYAPP_INSTANCE_NAME)_dev \
		-f docker-compose.yml \
		-f docker-compose.dev.yml \
		up \
		--build \
		--remove-orphans \
		--renew-anon-volumes

.PHONY: shell-core
shell-core: ## Runs a shell into the core container (in development mode only).
	docker exec -it $(MYAPP_INSTANCE_NAME)_dev_core_1 /bin/bash

.PHONY: shell-frontend
shell-frontend: ## Runs a shell into the frontend container (in development mode only).
	docker exec -it $(MYAPP_INSTANCE_NAME)_dev_frontend_1 /bin/bash

.PHONY: clean-dev
clean-dev: ## Cleans development environment (Docker containers and volumes).
	docker rm $(MYAPP_INSTANCE_NAME)_dev_reverse-proxy_1; exit 0
	docker rm $(MYAPP_INSTANCE_NAME)_dev_db_1; exit 0
	docker rm $(MYAPP_INSTANCE_NAME)_dev_brocker_1; exit 0
	docker rm $(MYAPP_INSTANCE_NAME)_dev_core_1; exit 0
	docker rm $(MYAPP_INSTANCE_NAME)_dev_worker_1; exit 0
	docker rm $(MYAPP_INSTANCE_NAME)_dev_frontend_1; exit 0
	docker volume rm $(MYAPP_INSTANCE_NAME)_dev_db-data; exit 0
	docker volume rm $(MYAPP_INSTANCE_NAME)_dev_brocker-data; exit 0
	docker volume rm $(MYAPP_INSTANCE_NAME)_dev_core-media; exit 0

.PHONY: clean-dev-db
clean-dev-db: ## Cleans development databases (Docker containers and volumes).
	docker rm $(MYAPP_INSTANCE_NAME)_dev_db_1; exit 0
	docker volume rm $(MYAPP_INSTANCE_NAME)_dev_db-data; exit 0

.PHONY: prod
prod: ## Runs all services in production mode.
	docker-compose -p $(MYAPP_INSTANCE_NAME)_prod \
		-f docker-compose.yml \
		up \
		--build \
		--remove-orphans \
		--renew-anon-volumes

.PHONY: detach
detach: ## Runs all services in production mode, in detached mode.
	docker-compose -p $(MYAPP_INSTANCE_NAME)_prod \
		-f docker-compose.yml \
		up -d \
		--build \
		--remove-orphans \
		--renew-anon-volumes

.PHONY: stop
stop: ## Stops all services running in production mode.
	docker-compose -p $(MYAPP_INSTANCE_NAME)_prod \
		-f docker-compose.yml \
		stop

.PHONY: clean-prod
clean-prod: ## Cleans production environment (Docker containers only).
	docker rm $(MYAPP_INSTANCE_NAME)_prod_reverse-proxy_1; exit 0
	docker rm $(MYAPP_INSTANCE_NAME)_prod_db_1; exit 0
	docker rm $(MYAPP_INSTANCE_NAME)_prod_brocker_1; exit 0
	docker rm $(MYAPP_INSTANCE_NAME)_prod_core_1; exit 0
	docker rm $(MYAPP_INSTANCE_NAME)_prod_worker_1; exit 0

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
