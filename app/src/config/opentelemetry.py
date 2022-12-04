import os

import opentelemetry.instrumentation.fastapi as otel_fastapi
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

from .env import STAGE


def setup_span_exporter():
    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider=tracer_provider)

    if STAGE == "local":
        tracer_provider.add_span_processor(
            span_processor=SimpleSpanProcessor(span_exporter=ConsoleSpanExporter()),
        )
    else:
        tracer_provider.add_span_processor(
            span_processor=BatchSpanProcessor(
                span_exporter=CloudTraceSpanExporter(
                    project_id=os.environ.get("GCP_PROJECT"),
                ),
            ),
        )


def setup_fastapi_instrumentor(app):
    instrumentor = otel_fastapi.FastAPIInstrumentor()
    instrumentor.instrument_app(
        app=app,
        server_request_hook=_server_request_hook,
        client_request_hook=_client_request_hook,
        client_response_hook=_client_response_hook,
    )


def _server_request_hook(span, scope):
    span.update_name("name from server hook")


def _client_request_hook(receive_span, request):
    receive_span.update_name("name from client hook")
    receive_span.set_attribute("attr-from-request-hook", "set")


def _client_response_hook(send_span, response):
    send_span.update_name("name from response hook")
    send_span.set_attribute("attr-from-response-hook", "value")
