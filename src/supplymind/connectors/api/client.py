"""
SupplyMind Enterprise AI

Enterprise HTTP Client

Provides the HTTPX-based implementation of outbound HTTP
communication.
"""

from collections.abc import Mapping
from typing import Any

import httpx

from supplymind.connectors.api.models import HttpResponse
from supplymind.core.errors.exceptions import ConnectorException


class HttpxClient:
    """
    Execute asynchronous outbound requests using HTTPX.

    The client normalizes third-party HTTP responses into SupplyMind
    response models and translates transport failures into enterprise
    connector exceptions.
    """

    def __init__(
        self,
        *,
        client: httpx.AsyncClient | None = None,
        timeout_seconds: float = 10.0,
    ) -> None:
        """
        Initialize the enterprise HTTP client.

        Args:
            client: Optional HTTPX client supplied through dependency
                injection.
            timeout_seconds: Default timeout used when creating an
                internally managed HTTPX client.

        Raises:
            ValueError: If timeout_seconds is not positive.
        """

        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero.")

        self._client = client or httpx.AsyncClient(
            timeout=httpx.Timeout(timeout_seconds),
        )

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        json: Any | None = None,
    ) -> HttpResponse:
        """
        Execute an asynchronous HTTP request.

        Args:
            method: HTTP method such as GET, POST, PUT, or DELETE.
            url: Absolute or client-relative request URL.
            params: Optional query-string parameters.
            headers: Optional request headers.
            json: Optional JSON-compatible request body.

        Returns:
            A normalized HTTP response.

        Raises:
            ConnectorException: If the request cannot be completed.
        """

        normalized_method = method.strip().upper()

        if not normalized_method:
            raise ValueError("method must not be empty.")

        if not url.strip():
            raise ValueError("url must not be empty.")

        try:
            response = await self._client.request(
                method=normalized_method,
                url=url,
                params=params,
                headers=headers,
                json=json,
            )
        except httpx.TimeoutException as exc:
            raise ConnectorException(
                message="External HTTP request timed out.",
                details={
                    "method": normalized_method,
                    "url": url,
                    "error_type": "timeout",
                },
            ) from exc
        except httpx.RequestError as exc:
            raise ConnectorException(
                message="External HTTP request failed.",
                details={
                    "method": normalized_method,
                    "url": url,
                    "error_type": "request_error",
                },
            ) from exc

        return HttpResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            content=response.content,
        )

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

        return await self.request(
            method="GET",
            url=url,
            params=params,
            headers=headers,
        )

    async def close(self) -> None:
        """Close the underlying HTTPX client and its connection pool."""

        await self._client.aclose()