from fastapi import FastAPI

from .config.middleware import Middlewares
from .config.opentelemetry import (
    initialize_tracer_provider,
    setup_fastapi_instrumentor,
    setup_span_exporter,
)
from .router.sample import sample_router

app = FastAPI()
app.include_router(sample_router)

initialize_tracer_provider()
setup_fastapi_instrumentor(app)
setup_span_exporter()

Middlewares(app)
