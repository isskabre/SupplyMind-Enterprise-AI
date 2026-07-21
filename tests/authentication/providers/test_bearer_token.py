"""
SupplyMind Enterprise AI

Bearer Token Authentication Provider Tests
"""

import pytest

from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)
from supplymind.authentication.configuration import (
    BearerTokenAuthenticationConfiguration,
)
from supplymind.authentication.constants import (
    AUTHORIZATION_HEADER,
    BEARER_PREFIX,
)
from supplymind.authentication.providers import (
    BearerTokenAuthenticationProvider,
)


@pytest.mark.anyio
async def test_get_headers_returns_bearer_authorization_header() -> None:
    """
    The provider should return the standard bearer Authorization header.
    """
    configuration = BearerTokenAuthenticationConfiguration(
        token="test-token",
    )
    provider = BearerTokenAuthenticationProvider(
        configuration=configuration,
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        AUTHORIZATION_HEADER: f"{BEARER_PREFIX} test-token",
    }


@pytest.mark.anyio
async def test_provider_uses_normalized_configuration() -> None:
    """
    The provider should use the normalized token from its configuration.
    """
    configuration = BearerTokenAuthenticationConfiguration(
        token="  test-token  ",
    )
    provider = BearerTokenAuthenticationProvider(
        configuration=configuration,
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        AUTHORIZATION_HEADER: f"{BEARER_PREFIX} test-token",
    }


def test_provider_implements_authentication_protocol() -> None:
    """
    The concrete provider should satisfy the authentication protocol.
    """
    configuration = BearerTokenAuthenticationConfiguration(
        token="test-token",
    )
    provider = BearerTokenAuthenticationProvider(
        configuration=configuration,
    )

    assert isinstance(
        provider,
        AuthenticationProviderProtocol,
    )


def test_provider_preserves_configuration_instance() -> None:
    """
    The provider should retain the supplied immutable configuration.
    """
    configuration = BearerTokenAuthenticationConfiguration(
        token="test-token",
    )
    provider = BearerTokenAuthenticationProvider(
        configuration=configuration,
    )

    assert provider.configuration is configuration


def test_provider_representation_does_not_expose_token() -> None:
    """
    The bearer token must not appear in the provider representation.
    """
    token = "highly-sensitive-bearer-token"
    configuration = BearerTokenAuthenticationConfiguration(
        token=token,
    )
    provider = BearerTokenAuthenticationProvider(
        configuration=configuration,
    )

    provider_representation = repr(provider)

    assert token not in provider_representation
    assert provider_representation == (
        "BearerTokenAuthenticationProvider("
        "configuration=BearerTokenAuthenticationConfiguration()"
        ")"
    )
