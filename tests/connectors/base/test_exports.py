"""
SupplyMind Enterprise AI

Connector Package Export Tests
"""

from supplymind.connectors.base import (
    ConnectorAuthenticationException,
    ConnectorAuthorizationException,
    ConnectorException,
    ConnectorHealth,
    ConnectorProtocol,
    ConnectorRateLimitException,
    ConnectorResponseException,
    ConnectorTimeoutException,
    ConnectorUnavailableException,
)


def test_connector_foundation_public_exports_are_available() -> None:
    assert ConnectorProtocol is not None
    assert ConnectorHealth is not None
    assert ConnectorException is not None
    assert ConnectorAuthenticationException is not None
    assert ConnectorAuthorizationException is not None
    assert ConnectorTimeoutException is not None
    assert ConnectorRateLimitException is not None
    assert ConnectorUnavailableException is not None
    assert ConnectorResponseException is not None