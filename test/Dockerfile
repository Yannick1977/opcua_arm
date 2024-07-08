# syntax=docker/dockerfile:1
FROM arm32v7/ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y --no-install-recommends git build-essential bash curl \
   libffi-dev python3-dev libssl-dev libxml2-dev libxslt-dev \
   python3 python3-pip python3-dev python3-lxml python3-venv \
   libyaml-dev cargo rustc

# uncommenting this and trying this also fails the same way
# RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
# ENV PATH="/root/.cargo/bin:$HOME/.cargo/bin:${PATH}"
# RUN ln -s $HOME/.cargo/env /etc/profile.d/cargo_env.sh

ENV CARGO_NET_GIT_FETCH_WITH_CLI=true
ENV RUSTFLAGS="-C lto=n"
RUN python --version
RUN pip --version
RUN pip install -U pip setuptools
RUN pip --version
RUN pip install cryptography