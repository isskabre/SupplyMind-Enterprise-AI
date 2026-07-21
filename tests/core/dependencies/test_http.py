"""
Tests for the HTTP client dependency provider.
"""

from fastapi import FastAPI
from starlette.requests import Request

import pytest

from supplymind.connectors.api import HttpxClient
from supplymind.core.dependencies import get_http_client


def build_request(application: FastAPI) -> Request:
    """Create a minimal request associated with an application."""

    return Request(
        {
            "type": "http",
            "app": application,
            "method": "GET",
            "path": "/",
            "headers": [],
            "query_string": b"",
            "server": ("testserver", 80),
            "client": ("testclient", 50000),
            "scheme": "http",
        }
    )


@pytest.mark.anyio
async def test_get_http_client_returns_application_resource() -> None:
    """The provider should return the application-owned client."""

    application = FastAPI()
    http_client = HttpxClient()
    application.state.http_client = http_client
    request = build_request(application)

    try:
        resolved_client = get_http_client(request)
    finally:
        await http_client.close()

    assert resolved_client is http_client


def test_get_http_client_rejects_missing_resource() -> None:
    """The provider should fail clearly before lifecycle startup."""

    application = FastAPI()
    request = build_request(application)

    with pytest.raises(
        RuntimeError,
        match="HTTP client has not been initialized",
    ):
        get_http_client(request)
