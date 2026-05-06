from uuid import uuid4
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from py_common.logging.context import set_correlation_id


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-Id", str(uuid4()))
        set_correlation_id(correlation_id)
        response = await call_next(request)
        response.headers["X-Correlation-Id"] = correlation_id
        return response
