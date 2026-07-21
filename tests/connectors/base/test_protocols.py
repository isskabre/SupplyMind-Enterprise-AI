"""
SupplyMind Enterprise AI

Connector Protocol Tests
"""

from supplymind.connectors.base.models import ConnectorHealth
from supplymind.connectors.base.protocols import ConnectorProtocol


class HealthyConnector:
    """
    Test implementation satisfying the connector protocol.
    """

    async def health_check(self) -> ConnectorHealth:
        return ConnectorHealth(
            healthy=True,
            message="Connector is healthy.",
        )


class InvalidConnector:
    """
    Test implementation that does not satisfy the connector protocol.
    """


def test_valid_connector_satisfies_protocol() -> None:
    connector = HealthyConnector()

    assert isinstance(connector, ConnectorProtocol)


def test_invalid_connector_does_not_satisfy_protocol() -> None:
    connector = InvalidConnector()

    assert not isinstance(connector, ConnectorProtocol)
