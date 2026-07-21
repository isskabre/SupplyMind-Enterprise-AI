"""
SupplyMind Enterprise AI

Authentication Configuration Export Tests
"""

from supplymind.authentication.configuration import (
    ApiKeyAuthenticationConfiguration,
    BearerTokenAuthenticationConfiguration,
    OAuth2ClientCredentialsConfiguration,
)


def test_public_exports() -> None:
    """
    Verify that the configuration package exports its public API.
    """
    assert ApiKeyAuthenticationConfiguration
    assert BearerTokenAuthenticationConfiguration
    assert OAuth2ClientCredentialsConfiguration
