"""
SupplyMind Enterprise AI

Authentication Package Export Tests
"""

from supplymind.authentication import (
    ApiKeyAuthenticationProvider,
    AuthenticationConfigurationException,
    AuthenticationException,
    AuthenticationFactory,
    AuthenticationHeaders,
    AuthenticationProviderProtocol,
    BearerTokenAuthenticationProvider,
    CredentialUnavailableException,
    TokenAcquisitionException,
    OAuth2AccessToken,
    OAuth2ClientCredentialsAuthenticationProvider,
)


def test_public_exports() -> None:
    """
    Verify that the authentication package exports its public API.
    """
    assert ApiKeyAuthenticationProvider
    assert BearerTokenAuthenticationProvider
    assert AuthenticationConfigurationException
    assert AuthenticationException
    assert AuthenticationHeaders
    assert AuthenticationProviderProtocol
    assert CredentialUnavailableException
    assert TokenAcquisitionException
    assert AuthenticationFactory
    assert OAuth2AccessToken
    assert OAuth2ClientCredentialsAuthenticationProvider
