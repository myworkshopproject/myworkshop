FROM python:3.10

# Update distribution
USER root
RUN apt update
RUN apt -y dist-upgrade

# Intall usefull tools
RUN apt install -y gettext
RUN apt install -y netcat

# Install and configure Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create default user
ARG USER_NAME=docker_user
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd ${USER_NAME} --non-unique --gid ${USER_GID}
RUN useradd ${USER_NAME} --non-unique --uid ${USER_UID} --gid ${USER_GID} --create-home --shell /bin/bash

# Create required directories
RUN mkdir -p /code/services/core
RUN mkdir /code/services/core/.tox
RUN mkdir /code/services/core/media
RUN mkdir /code/services/core/static
RUN mkdir /code/services/core/venv

# Copy source code
WORKDIR /code
COPY . .
RUN chown -R ${USER_UID}:${USER_GID} /code/services/core

# App install
WORKDIR /code/services/core
USER ${USER_NAME}
RUN make venv
RUN make install

# Change directory
WORKDIR /code
