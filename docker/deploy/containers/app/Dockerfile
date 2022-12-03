# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.10

# # libs
FROM python:${PYTHON_VERSION}-buster as libs

WORKDIR /workdir
COPY requirements/requirements.txt .

RUN pip install --no-cache-dir -t /app-libs -r requirements.txt

# https://github.com/Yelp/dumb-init
ENV DUMP_INIT_VERSION 1.2.5
RUN wget -nv -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v${DUMP_INIT_VERSION}/dumb-init_${DUMP_INIT_VERSION}_x86_64
RUN chmod +x /usr/local/bin/dumb-init

# app: multi-stage build
FROM python:${PYTHON_VERSION}-slim as app
ARG PYTHON_VERSION
ARG PORT
ARG STAGE
ARG REVISION

ENV PYTHONBUFFERED True \
    PYTHONDONTWRITEBYTECODE True

ENV STAGE=${STAGE}
ENV REVISION=${REVISION}

WORKDIR /app
COPY ./app /app

# ref: https://future-architect.github.io/articles/20200513/
RUN test -d /usr/local/lib/python3.10/site-packages
COPY ./docker/deploy/containers/app/sitecustomize.py /usr/local/lib/python3.10/site-packages/

COPY --from=libs /workdir/requirements.txt /app-libs /app-libs/
COPY --from=libs /usr/local/bin/dumb-init /usr/local/bin/dumb-init

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD python /app-libs/bin/gunicorn src.main:app \
    --config=python:src.config.gunicorn \
    --bind=0.0.0.0:$PORT
