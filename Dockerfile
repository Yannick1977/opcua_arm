FROM python:3 AS base

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    bash \
    curl \
    libffi-dev \
    python3-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    python3 \
    python3-pip \
    python3-dev \
    python3-lxml \
    python3-venv \
    libyaml-dev \
    cargo \
    rustc

RUN pip install asyncua

