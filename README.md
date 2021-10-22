# My Workshop
A decentralized application to create and share your project documentation.

## Disclaimer
This project is at a very early stage of development: It can evolve dramatically at the next commits!

## Features
- Generates beautiful documentation for your projects;
- Provides a laboratory notebook to document your experiments;
- Simplifies the management of your workshop, your fab lab or your makerspace.

## Installation

### Requirements
- [Docker](https://docs.docker.com/get-docker/): we use _Docker_ to develop and run __My Workshop__. This is a strict requirement to use this project.
- [Docker Compose](https://docs.docker.com/compose/install/): we use _Docker Compose_ to simplify the orchestration of all __My Workshop__ application services, using configuration files for different environments (such as _dev_, _test_, _staging_ or _prod_).

Download this repository and unzip it on your computer. You should rename the folder `myworkshop-main` in `myworkshop`.

Or clone the repository directly on your computer:
```
$ git clone git@github.com:myworkshopproject/myworkshop.git
```

### Quickstart
To start the demo application, please run:
``` bash
$ docker-compose up
```

Or if the `make` application is available on your operating system:
``` bash
$ make quickstart
```

Wait a bit for the application to build, then you can access it with your favorite internet browser at the address `http://localhost:8080/`.

There may be a conflict if port `8080` on your machine is already in use. In this case, you can change it with the following command with a suitable port number:
``` bash
$ NGINX_HOST_PORT=8080 docker-compose up
```

<!--
remplacer par la commande automatique dans docker compose !!!!!!

When launching the application for the first time, you will need to create a super user to manage it.
You can do this using the following command:
``` bash
$ docker exec -it myworkshop_core_1 make createsuperuser
``` -->


### Install and run a development environment
__My Workshop__ stores config in environment variables.
When using _Docker Compose_ to run __My Workshop__, the `.env` file is used to define all required environment variables.
You should never edit this `.env` file directly or store sensitive information in it, but you can override one or more of these variables by defining them directly in the shell before launching docker compose (values in the shell take precedence over those specified in the `.env` file.).

Once you have customized your environment variables, you can build and start a development environment with the following command:
``` bash
$ make dev
```

This previous command builds all the required services for development and starts them all except the _core_ web server and workers.

To start the _Django_ web server, please open a terminal in the container:
``` bash
$ make shell-core
```

Then run:
``` bash
(core) $ make venv
(core) $ make install-dev
(core) $ make migrate
(core) $ make populate-db
(core) $ make createsuperuser
(core) $ make runserver
```

To start a _Celery_ worker in another _core_ container, please run:
``` bash
(core) $ make worker
```

Frontend assets (_Elm_, _JavaScript_, _CSS_ files, etc.) are built using _webpack_. To make the dev easier, the development environment provides a _Node.js Docker_ container.

To start the frontend dev environment, please open a terminal in the dedicated container:
``` bash
$ make shell-frontend
```

Then run:
``` bash
(frontend) $ npm install
(frontend) $ npm run build
```

### Exposed ports when using Docker Compose to run My Workshop

| port  | service       | environment variable          | mode     | description                            |
|-------|---------------|-------------------------------|----------|----------------------------------------|
| 8080  | reverse-proxy | NGINX_HOST_PORT               | all      | NGINX server (My Workshop entry point) |
| 15672 | broker        | RABBITMQ_MANAGEMENT_HOST_PORT | all      | RabbitMQ management and monitoring     |
| 5432  | db            | POSTGRES_HOST_PORT_DEV        | dev only | PostgreSQL server                      |
| 5672  | broker        | RABBITMQ_HOST_PORT_DEV        | dev only | RabbitMQ server                        |
| 8000  | core          | CORE_HOST_PORT_DEV            | dev only | Django dev server                      |

### Install and run a production environment
Regarding production deployment, when you deploy the different services independently, you must define a number of environment variables. For example, for `core` and `worker` services, be sure to set the following variables:

``` env
DEBUG=False
ALLOWED_HOSTS=example.com
SITE_NAME=My Workshop
MEDIA_ROOT=/path/to/media/
DJANGO_SECRET_KEY=********
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=********
DJANGO_SUPERUSER_EMAIL=admin@example.com

POSTGRES_HOST=postgres.example.com
POSTGRES_PORT=5432
POSTGRES_DB=myworkshop
POSTGRES_USER=user
POSTGRES_PASSWORD=********

RABBITMQ_HOST=rabbitmq.example.com
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_VHOST=myworkshop
RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=********

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=webmaster@example.com
EMAIL_HOST_PASSWORD=********
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

## Tech/framework used
- [NGINX](https://www.nginx.com/): a free and open-source web server used as a reverse proxy;
- [Django](https://www.djangoproject.com/): a Python-based free and open-source web framework;
- [Django REST framework](https://www.django-rest-framework.org/): a powerful and flexible toolkit for building Web APIs.
- [Celery](https://docs.celeryproject.org/): Distributed Task Queue for Python;
- [PostgreSQL](https://www.postgresql.org/): a free and open-source relational database management system;
- [RabbitMQ](https://www.rabbitmq.com/): the most widely deployed open source message broker.
- [webpack](https://webpack.js.org/): a module bundler, to bundle JavaScript files.

## Contributing
For the sake of simplicity, to ease interaction with the community, we use the [GitHub flow](https://guides.github.com/introduction/flow/index.html) for open-source projects. In a few words:
- The `main` branch is always stable and deployable;
- Tags from the `main` branch are considered as releases;
- Contributors have to fork or create a new feature-branch to work on (if they are allowed to in the original repository) and propose a pull request to merge their branch to `main`.

If you'd like to contribute, please raise an issue or fork the repository and use a feature branch. Pull requests are warmly welcome!

## Versioning
We use [SemVer](http://semver.org/) for versioning. See the [CHANGELOG.md](CHANGELOG.md) file for details.

## Licensing
The code in this project is licensed under MIT license. See the [LICENSE](LICENSE) file for details.

## Contributors
- **Julien Lebunetel** - [jlebunetel](https://github.com/jlebunetel).
- **Guillaume Collet** - [gcollet](https://gitlab.com/gcollet).
- **Tony Vanpoucke** - [EdulabRennes2](https://gitlab.com/EdulabRennes2).
