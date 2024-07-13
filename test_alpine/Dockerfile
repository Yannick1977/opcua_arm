FROM arm32v7/python:3-slim AS compile-image

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip setuptools

RUN apt-get update &&\
    apt-get -y install gcc libffi-dev libssl-dev libuv1-dev libxslt-dev libz-dev &&\
    rm -rf /var/lib/apt/lists/*

RUN pip install --user -r requirements.txt


FROM arm32v7/python:3-slim AS build-image

RUN apt-get update -y &&\
    apt-get install -y libxml2-dev libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=compile-image /root/.local /root/.local
COPY . /root/.local/

ENV PATH=/root/.local/bin:$PATH

CMD ["python3", "/root/.local/app.py"]