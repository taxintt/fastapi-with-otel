ARG PYTHON_VERSION=3.10

# libs
FROM python:${PYTHON_VERSION}-buster as libs

WORKDIR /workdir
COPY requirements/requirements-dev.txt .

RUN pip install --no-cache-dir -t /app-libs -r requirements-dev.txt

# app
FROM python:${PYTHON_VERSION}-buster as app
ARG PYTHON_VERSION

ENV PYTHONBUFFERED True \
    PYTHONDONTWRITEBYTECODE True

WORKDIR /app

RUN test -d /usr/local/lib/python${PYTHON_VERSION}/site-packages/
COPY ./docker/local/containers/app/sitecustomize.py /usr/local/lib/python${PYTHON_VERSION}/site-packages/
COPY --from=libs /workdir/requirements-dev.txt /app-libs /app-libs/

CMD exec gunicorn src.main:app \
    --config=python:src/config/gunicorn \
    --bind=0.0.0.0:$PORT
