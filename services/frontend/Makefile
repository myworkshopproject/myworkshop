################################################################################
# Commands to be executed inside the container.                                #
################################################################################

default: help

.PHONY: install-dev
install-dev: ## Installs or updates development dependencies.
	npm install

.PHONY: sleep
sleep: install-dev ## Installs development dependencies and wait.
	sleep infinity

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
