"""
SupplyMind Enterprise AI

HTTP Client Dependency Provider

Provides access to the application-scoped outbound HTTP client.
"""

from fastapi import Request

from supplymind.connectors.api import HttpClientProtocol


def get_http_client(
    request: Request,
) -> HttpClientProtocol:
    """
    Return the application-scoped outbound HTTP client.

    Args:
        request: Current FastAPI request containing application state.

    Returns:
        The HTTP client owned by the running application.

    Raises:
        RuntimeError: If the application lifecycle has not initialized
            the HTTP client.
    """

    http_client = getattr(
        request.app.state,
        "http_client",
        None,
    )

    if http_client is None:
        raise RuntimeError(
            "HTTP client has not been initialized. "
            "Ensure the application lifespan is running."
        )

    return http_client