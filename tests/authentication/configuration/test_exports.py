"""
SupplyMind Enterprise AI

Authentication Configuration Export Tests
"""

from supplymind.authentication.configuration import (
    ApiKeyAuthenticationConfiguration,
    BearerTokenAuthenticationConfiguration,
)


def test_public_exports() -> None:
    """
    Verify that the configuration package exports its public API.
    """
    assert ApiKeyAuthenticationConfiguration
    assert BearerTokenAuthenticationConfiguration