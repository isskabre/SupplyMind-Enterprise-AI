"""
SupplyMind Enterprise AI

Correlation ID Middleware

Assigns a unique correlation ID to every HTTP request.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from supplymind.core.logging.constants import CORRELATION_ID_HEADER
from supplymind.core.logging.context import correlation_id
from supplymind.core.logging.correlation import resolve_correlation_id


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Manage a request-scoped correlation ID.

    The middleware preserves a valid incoming X-Correlation-ID header.
    Otherwise, it generates a new UUID.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        request_correlation_id = resolve_correlation_id(
            request.headers.get(CORRELATION_ID_HEADER)
        )

        token = correlation_id.set(request_correlation_id)

        try:
            response = await call_next(request)
            response.headers[CORRELATION_ID_HEADER] = request_correlation_id
            return response
        finally:
            correlation_id.reset(token)
