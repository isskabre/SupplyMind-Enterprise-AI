"""
SupplyMind Enterprise AI

Request Logging Middleware

Logs every HTTP request processed by the application.
"""

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from supplymind.core.logger import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log every HTTP request.

    Records the request method, path, response status,
    and execution time.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)
        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            "%s %s | Status=%s | Duration=%.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response