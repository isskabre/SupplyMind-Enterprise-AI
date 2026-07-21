"""
SupplyMind Enterprise AI

HTTP Client Protocols

Defines framework-independent contracts for outbound HTTP
communication.
"""

from collections.abc import Mapping
from typing import Any, Protocol

from supplymind.connectors.api.models import HttpResponse


class HttpClientProtocol(Protocol):
    """
    Define the contract for asynchronous outbound HTTP clients.

    Implementations are responsible for executing requests, normalizing
    responses, translating transport failures, and releasing owned
    resources.
    """

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        data: Mapping[str, Any] | None = None,
        json: Any | None = None,
    ) -> HttpResponse:
        """
        Execute an asynchronous HTTP request.

        Args:
            method: HTTP method such as GET, POST, PUT, or DELETE.
            url: Absolute or client-relative request URL.
            params: Optional query-string parameters.
            headers: Optional request headers.
            data: Optional form-compatible request body.
            json: Optional JSON-compatible request body.

        Returns:
            A normalized HTTP response.
        """

        ...

    async def get(
        self,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> HttpResponse:
        """
        Execute an asynchronous HTTP GET request.

        Args:
            url: Absolute or client-relative request URL.
            params: Optional query-string parameters.
            headers: Optional request headers.

        Returns:
            A normalized HTTP response.
        """

        ...

    async def close(self) -> None:
        """Release resources owned by the HTTP client."""

        ...
