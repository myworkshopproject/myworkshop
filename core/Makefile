NPROC=`nproc --all`
GUNICORN_WORKERS := $(if $(GUNICORN_WORKERS),$(GUNICORN_WORKERS),$$(($(NPROC) + 1)))
default: help

.PHONY: test
test:
	echo $(GUNICORN_WORKERS)

.PHONY: venv
venv: ## Creates a virtual environment.
	python -m venv venv

.PHONY: requirements
requirements: ## Builds or updates requirements.
	venv/bin/pip install --upgrade pip wheel setuptools pip-tools
	venv/bin/pip-compile requirements.in
	venv/bin/pip-compile requirements.dev.in

.PHONY: install
install: ## Installs production dependencies.
	venv/bin/pip install --upgrade pip wheel setuptools
	venv/bin/pip install -r requirements.txt

.PHONY: install-dev
install-dev: ## Installs or updates development dependencies.
	venv/bin/pip install --upgrade pip wheel setuptools pip-tools
	venv/bin/pip-sync requirements.txt requirements.dev.txt

.PHONY: migrations
migrations: ## Creates new migrations based on the changes detected to your models.
	venv/bin/python manage.py makemigrations

.PHONY: migrate
migrate: ## Synchronizes the database state with the current set of models and migrations.
	venv/bin/python manage.py migrate

.PHONY: populate-db
populate-db: ## Populates the database with initial values.
	venv/bin/python manage.py populate_db

.PHONY: createsuperuser
createsuperuser: ## Creates a default superuser.
	venv/bin/python manage.py createsuperuser --no-input; exit 0

.PHONY: collectstatic
collectstatic: ## Collects the static files into STATIC_ROOT.
	mkdir -p static
	venv/bin/python manage.py collectstatic --no-input --clear

.PHONY: clean-static
clean-static: ## Remove collected static files.
	rm -rf static

.PHONY: serve
serve: ## Starts the Gunicorn server.
	venv/bin/gunicorn myapp.wsgi:application \
		--bind 0.0.0.0:8000 \
		--workers $(GUNICORN_WORKERS) \
		--log-level=$(GUNICORN_LOG_LEVEL)

.PHONY: runserver
runserver: ## Starts the Django development server.
	venv/bin/python manage.py runserver 0.0.0.0:8000

.PHONY: worker
worker: ## Starts a Celery worker.
	sleep infinity

.PHONY: quickstart
quickstart: migrate populate-db createsuperuser serve ## Starts Django in demo mode.

.PHONY: prod
prod: migrate populate-db createsuperuser serve ## Starts Django in production mode.

.PHONY: generate_secret_key
generate_secret_key: ## Generates a Secret Key.
	venv/bin/python utils/secret_key.py

.PHONY: tests
tests: ## Runs all tests.
	venv/bin/tox

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
