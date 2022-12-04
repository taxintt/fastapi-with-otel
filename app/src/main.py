from fastapi import FastAPI

from .config.opentelemetry import setup_fastapi_instrumentor, setup_span_exporter
from .router.sample import sample_router

app = FastAPI()
app.include_router(sample_router)

setup_fastapi_instrumentor(app)
setup_span_exporter()
