"""
SupplyMind Enterprise AI

API Key Authentication Provider Tests
"""

import pytest

from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)
from supplymind.authentication.configuration import (
    ApiKeyAuthenticationConfiguration,
)
from supplymind.authentication.providers import (
    ApiKeyAuthenticationProvider,
)


@pytest.mark.anyio
async def test_get_headers_returns_default_api_key_header() -> None:
    """
    The provider should return the API key using the default header name.
    """
    configuration = ApiKeyAuthenticationConfiguration(
        api_key="test-secret",
    )
    provider = ApiKeyAuthenticationProvider(
        configuration=configuration,
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        "X-API-Key": "test-secret",
    }


@pytest.mark.anyio
async def test_get_headers_supports_custom_header_name() -> None:
    """
    The provider should use the configured custom header name.
    """
    configuration = ApiKeyAuthenticationConfiguration(
        api_key="test-secret",
        header_name="api-key",
    )
    provider = ApiKeyAuthenticationProvider(
        configuration=configuration,
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        "api-key": "test-secret",
    }


@pytest.mark.anyio
async def test_get_headers_supports_prefix() -> None:
    """
    The provider should prepend the configured prefix to the API key.
    """
    configuration = ApiKeyAuthenticationConfiguration(
        api_key="test-secret",
        header_name="Authorization",
        prefix="Bearer",
    )
    provider = ApiKeyAuthenticationProvider(
        configuration=configuration,
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        "Authorization": "Bearer test-secret",
    }


@pytest.mark.anyio
async def test_provider_uses_normalized_configuration() -> None:
    """
    The provider should use values normalized by its configuration.
    """
    configuration = ApiKeyAuthenticationConfiguration(
        api_key="  test-secret  ",
        header_name="  X-Internal-Key  ",
        prefix="  Token  ",
    )
    provider = ApiKeyAuthenticationProvider(
        configuration=configuration,
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        "X-Internal-Key": "Token test-secret",
    }


def test_provider_implements_authentication_protocol() -> None:
    """
    The concrete provider should satisfy the authentication protocol.
    """
    configuration = ApiKeyAuthenticationConfiguration(
        api_key="test-secret",
    )
    provider = ApiKeyAuthenticationProvider(
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
    configuration = ApiKeyAuthenticationConfiguration(
        api_key="test-secret",
    )
    provider = ApiKeyAuthenticationProvider(
        configuration=configuration,
    )

    assert provider.configuration is configuration


def test_provider_representation_does_not_expose_api_key() -> None:
    """
    The API key must not appear in the provider representation.
    """
    api_key = "highly-sensitive-api-key"
    configuration = ApiKeyAuthenticationConfiguration(
        api_key=api_key,
        header_name="Authorization",
        prefix="Bearer",
    )
    provider = ApiKeyAuthenticationProvider(
        configuration=configuration,
    )

    provider_representation = repr(provider)

    assert api_key not in provider_representation
    assert "Authorization" in provider_representation
    assert "Bearer" in provider_representation