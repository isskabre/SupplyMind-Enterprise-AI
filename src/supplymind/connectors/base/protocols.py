"""
SupplyMind Enterprise AI

Connector Protocols

Defines the common protocol implemented by all enterprise connectors.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from supplymind.connectors.base.models import ConnectorHealth


@runtime_checkable
class ConnectorProtocol(Protocol):
    """
    Base protocol for all enterprise connectors.

    Every connector should expose a lightweight health check
    so the application can verify external dependencies.
    """

    async def health_check(self) -> ConnectorHealth:
        """
        Verify that the external system is reachable.

        Returns:
            True if the connector is healthy.
        """
        ...
