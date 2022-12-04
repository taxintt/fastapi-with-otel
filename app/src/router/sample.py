import random
import time

from fastapi import APIRouter
from opentelemetry import trace

sample_router = APIRouter()


# TODO: use decorator to implement easily
# ref: https://caddi.tech/archives/3312#OpenTelemetry
@sample_router.get("/sample")
async def get_sample():
    tracer = trace.get_tracer_provider().get_tracer(__name__)
    with tracer.start_as_current_span("get_sample"):
        time.sleep(2)
        return {"sample_id": random.randint(1, 10)}
