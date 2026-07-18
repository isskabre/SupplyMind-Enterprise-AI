"""
Tests for the SupplyMind application factory.
"""

from fastapi import FastAPI

from supplymind.application.factory import create_application


def test_create_application_returns_fastapi_instance() -> None:
    """The application factory should return a FastAPI instance."""

    application = create_application()

    assert isinstance(application, FastAPI)


def test_create_application_returns_independent_instances() -> None:
    """Each factory call should return a new application instance."""

    first_application = create_application()
    second_application = create_application()

    assert first_application is not second_application


def test_create_application_registers_expected_routes() -> None:
    """The factory should register all required public API routes."""

    application = create_application()

    paths = set(application.openapi()["paths"])

    assert {
        "/",
        "/api/v1/",
        "/api/v1/health",
        "/api/v1/live",
        "/api/v1/ready",
        "/api/v1/info",
        "/api/v1/version",
    }.issubset(paths)