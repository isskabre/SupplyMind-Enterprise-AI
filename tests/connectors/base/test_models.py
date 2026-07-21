"""
SupplyMind Enterprise AI

Connector Model Tests
"""

from supplymind.connectors.base.models import ConnectorHealth


def test_connector_health_defaults() -> None:
    health = ConnectorHealth(
        healthy=True,
    )

    assert health.healthy is True
    assert health.message is None


def test_connector_health_with_message() -> None:
    health = ConnectorHealth(
        healthy=False,
        message="Authentication failed.",
    )

    assert health.healthy is False
    assert health.message == "Authentication failed."
