"""
SupplyMind Enterprise AI

Connector Models

Shared models used across enterprise connectors.
"""

from pydantic import BaseModel, Field


class ConnectorHealth(BaseModel):
    """
    Represents the health status of an enterprise connector.
    """

    healthy: bool = Field(
        description="Whether the connector is healthy.",
    )

    message: str | None = Field(
        default=None,
        description="Optional health status message.",
    )
