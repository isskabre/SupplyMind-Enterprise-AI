"""
Tests for the enterprise HTTPX client.
"""

import httpx
import pytest

from supplymind.connectors.api.client import HttpxClient
from supplymind.core.errors.codes import ErrorCode
from supplymind.core.errors.exceptions import ConnectorException


@pytest.mark.anyio
async def test_get_returns_normalized_response() -> None:
    """A successful GET should return a SupplyMind HTTP response."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/health"

        return httpx.Response(
            status_code=200,
            headers={"X-Service": "mock-api"},
            json={"status": "healthy"},
        )

    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
    )
    client = HttpxClient(client=async_client)

    try:
        response = await client.get(
            "https://example.test/health",
        )
    finally:
        await client.close()

    assert response.status_code == 200
    assert response.is_success is True
    assert response.headers["x-service"] == "mock-api"
    assert response.json() == {"status": "healthy"}


@pytest.mark.anyio
async def test_request_forwards_query_parameters_and_headers() -> None:
    """Request data should be forwarded to the HTTP transport."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["limit"] == "10"
        assert request.headers["X-Correlation-ID"] == "test-123"

        return httpx.Response(
            status_code=200,
            json={"received": True},
        )

    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
    )
    client = HttpxClient(client=async_client)

    try:
        response = await client.get(
            "https://example.test/items",
            params={"limit": 10},
            headers={"X-Correlation-ID": "test-123"},
        )
    finally:
        await client.close()

    assert response.json() == {"received": True}


@pytest.mark.anyio
async def test_request_normalizes_http_method() -> None:
    """HTTP methods should be stripped and converted to uppercase."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"

        return httpx.Response(
            status_code=201,
            json={"created": True},
        )

    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
    )
    client = HttpxClient(client=async_client)

    try:
        response = await client.request(
            method=" post ",
            url="https://example.test/items",
            json={"name": "forecast"},
        )
    finally:
        await client.close()

    assert response.status_code == 201


@pytest.mark.anyio
async def test_http_error_status_is_returned_without_translation() -> None:
    """HTTP error statuses should remain available to connectors."""

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=404,
            json={"message": "not found"},
        )

    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
    )
    client = HttpxClient(client=async_client)

    try:
        response = await client.get(
            "https://example.test/missing",
        )
    finally:
        await client.close()

    assert response.status_code == 404
    assert response.is_success is False
    assert response.json() == {"message": "not found"}


@pytest.mark.anyio
async def test_timeout_is_translated_to_connector_exception() -> None:
    """HTTPX timeout failures should use the enterprise exception."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout(
            "The external service timed out.",
            request=request,
        )

    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
    )
    client = HttpxClient(client=async_client)

    try:
        with pytest.raises(ConnectorException) as exc_info:
            await client.get(
                "https://example.test/slow",
            )
    finally:
        await client.close()

    exception = exc_info.value

    assert exception.code == ErrorCode.CONNECTOR_ERROR
    assert exception.message == "External HTTP request timed out."
    assert exception.details == {
        "method": "GET",
        "url": "https://example.test/slow",
        "error_type": "timeout",
    }
    assert isinstance(exception.__cause__, httpx.ReadTimeout)


@pytest.mark.anyio
async def test_request_error_is_translated_to_connector_exception() -> None:
    """HTTPX transport failures should use the enterprise exception."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError(
            "Unable to connect.",
            request=request,
        )

    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
    )
    client = HttpxClient(client=async_client)

    try:
        with pytest.raises(ConnectorException) as exc_info:
            await client.get(
                "https://example.test/unavailable",
            )
    finally:
        await client.close()

    exception = exc_info.value

    assert exception.code == ErrorCode.CONNECTOR_ERROR
    assert exception.message == "External HTTP request failed."
    assert exception.details == {
        "method": "GET",
        "url": "https://example.test/unavailable",
        "error_type": "request_error",
    }
    assert isinstance(exception.__cause__, httpx.ConnectError)


@pytest.mark.anyio
async def test_request_rejects_empty_method() -> None:
    """An empty HTTP method should fail before transport execution."""

    client = HttpxClient(
        client=httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(200),
            ),
        ),
    )

    try:
        with pytest.raises(
            ValueError,
            match="method must not be empty",
        ):
            await client.request(
                method=" ",
                url="https://example.test",
            )
    finally:
        await client.close()


@pytest.mark.anyio
async def test_request_rejects_empty_url() -> None:
    """An empty URL should fail before transport execution."""

    client = HttpxClient(
        client=httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(200),
            ),
        ),
    )

    try:
        with pytest.raises(
            ValueError,
            match="url must not be empty",
        ):
            await client.get(" ")
    finally:
        await client.close()


def test_client_rejects_non_positive_timeout() -> None:
    """Internally created clients require a positive timeout."""

    with pytest.raises(
        ValueError,
        match="timeout_seconds must be greater than zero",
    ):
        HttpxClient(timeout_seconds=0)


@pytest.mark.anyio
async def test_request_forwards_form_data() -> None:
    """
    The client should forward form-compatible request data to HTTPX.
    """

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url == "https://example.com/oauth/token"
        assert request.headers["content-type"].startswith(
            "application/x-www-form-urlencoded"
        )
        assert request.content == (
            b"grant_type=client_credentials"
            b"&client_id=test-client"
            b"&client_secret=test-secret"
        )

        return httpx.Response(
            status_code=200,
            json={
                "access_token": "access-token",
                "token_type": "Bearer",
                "expires_in": 3600,
            },
        )

    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
    )
    client = HttpxClient(client=async_client)

    try:
        response = await client.request(
            method="POST",
            url="https://example.com/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": "test-client",
                "client_secret": "test-secret",
            },
        )
    finally:
        await client.close()

    assert response.status_code == 200
