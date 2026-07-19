"""
SupplyMind Enterprise AI

Authentication Package Export Tests
"""

from supplymind.authentication import (
    ApiKeyAuthenticationProvider,
    AuthenticationConfigurationException,
    AuthenticationException,
    AuthenticationHeaders,
    AuthenticationProviderProtocol,
    CredentialUnavailableException,
    TokenAcquisitionException,
)


def test_public_exports() -> None:
    """
    Verify that the authentication package exports its public API.
    """
    assert ApiKeyAuthenticationProvider
    assert AuthenticationConfigurationException
    assert AuthenticationException
    assert AuthenticationHeaders
    assert AuthenticationProviderProtocol
    assert CredentialUnavailableException
    assert TokenAcquisitionException