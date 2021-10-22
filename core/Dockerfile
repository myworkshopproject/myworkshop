ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

# Distribution upgrade
USER root
RUN apt update
RUN apt -y dist-upgrade

# Utils
RUN apt install -y netcat
RUN apt install -y gettext

# Python config
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Django install
WORKDIR /code
COPY Makefile Makefile
RUN make venv
COPY requirements.txt requirements.txt
RUN make install
COPY . .
