FROM python:3.12-alpine as base

WORKDIR /app

#SHELL ["/bin/sh", "-o", "pipefail", "-c"]

# Install dependencies
RUN apk update && apk add --no-cache \
    git \
    build-base \
    bash \
    curl \
    libffi-dev \
    python3-dev \
    libressl-dev \
    libxml2-dev \
    libxslt-dev \
    python3 \
    py3-pip \
    py3-lxml \
    yaml-dev \
    rust

RUN apk add gcc musl-dev python3-dev libffi-dev libressl-dev cargo

RUN pip install --upgrade pip setuptools

#RUN pip install cryptography
RUN pip install asyncua

# WORKDIR /app

# COPY requirements.txt requirements.txt

# RUN pip install -r requirements.txt

# COPY . /app/

# EXPOSE 1308

# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "1308"]