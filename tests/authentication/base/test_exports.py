"""
SupplyMind Enterprise AI

Authentication Package Export Tests
"""

from supplymind.authentication import (
    AuthenticationConfigurationException,
    AuthenticationException,
    AuthenticationHeaders,
    AuthenticationProviderProtocol,
    CredentialUnavailableException,
    TokenAcquisitionException,
)


def test_authentication_framework_public_exports_are_available() -> None:
    assert AuthenticationProviderProtocol is not None
    assert AuthenticationHeaders is not None
    assert AuthenticationException is not None
    assert AuthenticationConfigurationException is not None
    assert CredentialUnavailableException is not None
    assert TokenAcquisitionException is not None
