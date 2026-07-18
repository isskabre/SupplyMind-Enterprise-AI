"""
SupplyMind Enterprise AI

Application Factory

Creates and configures the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from supplymind import __version__
from supplymind.api.router import api_router
from supplymind.application.lifespan import application_lifespan
from supplymind.core.config import settings
from supplymind.core.errors.exceptions import SupplyMindException
from supplymind.core.errors.handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    supplymind_exception_handler,
    unexpected_exception_handler,
)
from supplymind.core.logger import configure_logging
from supplymind.middleware.correlation_id import CorrelationIdMiddleware
from supplymind.middleware.request_logging import RequestLoggingMiddleware


def create_application() -> FastAPI:
    """
    Create and configure a SupplyMind FastAPI application instance.

    Returns:
        A fully configured FastAPI application.
    """

    configure_logging()

    application = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Enterprise AI platform for supply chain intelligence.",
        lifespan=application_lifespan,
    )

    application.add_middleware(RequestLoggingMiddleware)
    application.add_middleware(CorrelationIdMiddleware)

    application.add_exception_handler(
        SupplyMindException,
        supplymind_exception_handler,
    )

    application.add_exception_handler(
        RequestValidationError,
        request_validation_exception_handler,
    )

    application.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    application.add_exception_handler(
        Exception,
        unexpected_exception_handler,
    )

    application.include_router(api_router)

    @application.get("/", tags=["Application"])
    def root() -> dict[str, str]:
        """Return basic application information."""
        return {
            "application": settings.app_name,
            "version": __version__,
            "status": "running",
        }

    return application