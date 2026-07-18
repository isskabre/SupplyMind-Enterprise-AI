"""
Tests for enterprise HTTP client protocols.
"""

from collections.abc import Mapping
from typing import Any

from supplymind.connectors.api.models import HttpResponse
from supplymind.connectors.api.protocols import HttpClientProtocol


class FakeHttpClient:
    """Minimal HTTP client implementation used for protocol testing."""

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        json: Any | None = None,
    ) -> HttpResponse:
        """Return a controlled response for any HTTP request."""

        return HttpResponse(
            status_code=200,
            content=b'{"method": "request"}',
        )

    async def get(
        self,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> HttpResponse:
        """Return a controlled response for a GET request."""

        return HttpResponse(
            status_code=200,
            content=b'{"method": "get"}',
        )

    async def close(self) -> None:
        """Release fake resources."""

        return None


def accepts_http_client(
    client: HttpClientProtocol,
) -> HttpClientProtocol:
    """Return a client that satisfies the HTTP protocol."""

    return client


def test_structural_http_client_satisfies_protocol() -> None:
    """A structurally compatible client should satisfy the contract."""

    client = FakeHttpClient()

    accepted_client = accepts_http_client(client)

    assert accepted_client is client