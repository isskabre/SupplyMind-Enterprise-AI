"""
SupplyMind Enterprise AI

Request Logging Middleware

Records operational information for every HTTP request processed
by the application.
"""

import logging
import time
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from supplymind.core.logging import get_logger


logger = get_logger(__name__)

CallNext = Callable[[Request], Awaitable[Response]]


def _get_log_level(status_code: int) -> int:
    """
    Return the appropriate logging level for an HTTP status code.
    """
    if status_code >= 500:
        return logging.ERROR

    if status_code >= 400:
        return logging.WARNING

    return logging.INFO


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log every HTTP request processed by the application.

    Records the request method, path, response status code,
    and execution duration without logging sensitive request data.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: CallNext,
    ) -> Response:
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (
                time.perf_counter() - start_time
            ) * 1000

            logger.exception(
                "HTTP request failed | Method=%s | Path=%s | "
                "Duration=%.2f ms",
                request.method,
                request.url.path,
                duration_ms,
                extra={
                    "http_method": request.method,
                    "http_path": request.url.path,
                    "http_status_code": 500,
                    "duration_ms": duration_ms,
                },
            )

            raise

        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.log(
            _get_log_level(response.status_code),
            "HTTP request completed | Method=%s | Path=%s | "
            "Status=%s | Duration=%.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            extra={
                "http_method": request.method,
                "http_path": request.url.path,
                "http_status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )

        return response