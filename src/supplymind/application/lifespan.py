"""
SupplyMind Enterprise AI

Application Lifespan Management

Defines application startup and shutdown lifecycle behavior.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from supplymind.connectors.api import HttpxClient
from supplymind.core.config import settings
from supplymind.core.configuration_validator import validate_configuration


@asynccontextmanager
async def application_lifespan(
    application: FastAPI,
) -> AsyncIterator[None]:
    """
    Manage application startup and shutdown activities.

    Validates configuration and initializes application-scoped
    infrastructure before the service begins accepting requests.
    Owned resources are released during graceful shutdown.

    Args:
        application: FastAPI application whose resources are managed.

    Yields:
        Control to the running FastAPI application.
    """

    validate_configuration(settings)

    http_client = HttpxClient(
        timeout_seconds=settings.http_timeout_seconds,
    )
    application.state.http_client = http_client

    try:
        yield
    finally:
        await http_client.close()
        del application.state.http_client
