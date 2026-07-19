"""
SupplyMind Enterprise AI

Enterprise Connector Foundations

Public exports for shared connector contracts, models, and exceptions.
"""

from supplymind.connectors.base.exceptions import (
    ConnectorAuthenticationException,
    ConnectorAuthorizationException,
    ConnectorException,
    ConnectorRateLimitException,
    ConnectorResponseException,
    ConnectorTimeoutException,
    ConnectorUnavailableException,
)
from supplymind.connectors.base.models import ConnectorHealth
from supplymind.connectors.base.protocols import ConnectorProtocol

__all__ = [
    "ConnectorAuthenticationException",
    "ConnectorAuthorizationException",
    "ConnectorException",
    "ConnectorHealth",
    "ConnectorProtocol",
    "ConnectorRateLimitException",
    "ConnectorResponseException",
    "ConnectorTimeoutException",
    "ConnectorUnavailableException",
]