from contextvars import ContextVar
from typing import Mapping

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

trace_id_ctx_var: ContextVar[str] = ContextVar("trace_id", default="")

class Middlewares:
    def __init__(self, app: FastAPI) -> None:
        app.add_middleware(TraceidMiddleware)
        app.add_middleware(ResponseHeaderMiddleware)


class TraceidMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id_token = None

        if trace_id := self.get_trace_id_from_headers(request.headers):
            trace_id_token = trace_id_ctx_var.set(trace_id)

        response = await call_next(request)

        if trace_id_token:
            trace_id_ctx_var.reset(trace_id_token)
        return response

    def get_trace_id_from_headers(self, headers: Mapping[str, str]) -> str | None:
        try:
            if gcp_trace_header_value := headers.get("x-cloud-trace-context", None):
                return gcp_trace_header_value.split("/", 1)[0]
            return None
        except Exception:
            return None


class ResponseHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # ref: https://www.ipa.go.jp/security/vuln/websecurity-HTML-1_9.html
        response.headers["X-Frame-Options"] = "DENY"
        return response