from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from supplymind.core.configuration_validator import validate_configuration
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from supplymind import __version__
from supplymind.api.router import api_router
from supplymind.core.config import settings
from supplymind.core.errors.exceptions import SupplyMindException
from supplymind.core.errors.handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    supplymind_exception_handler,
    unexpected_exception_handler,
)
from supplymind.core.logger import configure_logging


configure_logging()

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown activities."""

    validate_configuration(settings)

    yield

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description="Enterprise AI platform for supply chain intelligence.",
    lifespan=lifespan,
)

app.add_exception_handler(
    SupplyMindException,
    supplymind_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    request_validation_exception_handler,
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)

app.include_router(api_router)


@app.get("/", tags=["Application"])
def root() -> dict[str, str]:
    """Return basic application information."""
    return {
        "application": settings.app_name,
        "version": __version__,
        "status": "running",
    }
