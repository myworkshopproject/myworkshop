ARG NODE_VERSION
FROM node:${NODE_VERSION}

# Update distribution
RUN apt update
RUN apt -y dist-upgrade

# Create default user
ARG USER_NAME=docker_user
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd ${USER_NAME} --non-unique --gid ${USER_GID}
RUN useradd ${USER_NAME} --non-unique --uid ${USER_UID} --gid ${USER_GID} --shell /bin/bash --create-home

# Create required directories
RUN mkdir -p /code/services/frontend/node_modules
RUN chown -R ${USER_UID}:${USER_GID} /code

# App install
WORKDIR /code
USER ${USER_NAME}
