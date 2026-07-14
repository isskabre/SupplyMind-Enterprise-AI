"""
SupplyMind Enterprise AI

Correlation ID Middleware

Assigns a unique correlation ID to every HTTP request.
"""

from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from supplymind.core.logging.context import correlation_id


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Manage a request-scoped correlation ID.

    The middleware accepts an incoming X-Correlation-ID header when supplied.
    Otherwise, it generates a new UUID.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        request_correlation_id = (
            request.headers.get("X-Correlation-ID")
            or str(uuid4())
        )

        token = correlation_id.set(request_correlation_id)

        try:
            response = await call_next(request)
            response.headers["X-Correlation-ID"] = request_correlation_id
            return response
        finally:
            correlation_id.reset(token)