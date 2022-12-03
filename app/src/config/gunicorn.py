from .env import ON_CLOUD_RUN

if ON_CLOUD_RUN:
    worker_class = "uvicorn.workers.UvicornWorker"
    # https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7
    workers = 1
    threads = 8
else:
    worker_class = "uvicorn.workers.UvicornWorker"
    workers = 1
    threads = 8

timeout = 0
graceful_timeout = 10