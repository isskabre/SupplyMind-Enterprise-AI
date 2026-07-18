"""
SupplyMind Enterprise AI

Application Lifespan Management

Defines application startup and shutdown lifecycle behavior.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from supplymind.core.config import settings
from supplymind.core.configuration_validator import validate_configuration


@asynccontextmanager
async def application_lifespan(
    _: FastAPI,
) -> AsyncIterator[None]:
    """
    Manage application startup and shutdown activities.

    Validates application configuration before the service begins
    accepting requests. Resources initialized during startup should
    be released after the yield statement during application shutdown.

    Yields:
        Control to the running FastAPI application.
    """

    validate_configuration(settings)

    yield