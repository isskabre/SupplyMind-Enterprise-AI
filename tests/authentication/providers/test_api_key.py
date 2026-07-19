"""
SupplyMind Enterprise AI

API Key Authentication Provider Tests
"""

import pytest

from supplymind.authentication.base.exceptions import (
    AuthenticationConfigurationException,
)
from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)
from supplymind.authentication.providers import (
    ApiKeyAuthenticationProvider,
)


@pytest.mark.anyio
async def test_get_headers_returns_default_api_key_header() -> None:
    """
    The provider should return the API key using the default header name.
    """
    provider = ApiKeyAuthenticationProvider(
        api_key="test-secret",
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        "X-API-Key": "test-secret",
    }


@pytest.mark.anyio
async def test_get_headers_supports_custom_header_name() -> None:
    """
    The provider should support APIs that require a custom header name.
    """
    provider = ApiKeyAuthenticationProvider(
        api_key="test-secret",
        header_name="api-key",
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        "api-key": "test-secret",
    }


@pytest.mark.anyio
async def test_get_headers_supports_prefix() -> None:
    """
    The provider should prepend a configured prefix to the API key.
    """
    provider = ApiKeyAuthenticationProvider(
        api_key="test-secret",
        header_name="Authorization",
        prefix="Bearer",
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        "Authorization": "Bearer test-secret",
    }


@pytest.mark.anyio
async def test_provider_normalizes_surrounding_whitespace() -> None:
    """
    Provider configuration should be normalized during construction.
    """
    provider = ApiKeyAuthenticationProvider(
        api_key="  test-secret  ",
        header_name="  X-Internal-Key  ",
        prefix="  Token  ",
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        "X-Internal-Key": "Token test-secret",
    }


def test_provider_implements_authentication_protocol() -> None:
    """
    The concrete provider should satisfy the authentication protocol.
    """
    provider = ApiKeyAuthenticationProvider(
        api_key="test-secret",
    )

    assert isinstance(
        provider,
        AuthenticationProviderProtocol,
    )


@pytest.mark.parametrize(
    "api_key",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_provider_rejects_empty_api_key(api_key: str) -> None:
    """
    Empty or whitespace-only API keys should be rejected.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="non-empty API key",
    ):
        ApiKeyAuthenticationProvider(
            api_key=api_key,
        )


@pytest.mark.parametrize(
    "header_name",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_provider_rejects_empty_header_name(
    header_name: str,
) -> None:
    """
    Empty or whitespace-only header names should be rejected.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="non-empty header name",
    ):
        ApiKeyAuthenticationProvider(
            api_key="test-secret",
            header_name=header_name,
        )


@pytest.mark.parametrize(
    "prefix",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_provider_rejects_empty_prefix(prefix: str) -> None:
    """
    A supplied prefix must contain a meaningful value.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="prefix must be non-empty",
    ):
        ApiKeyAuthenticationProvider(
            api_key="test-secret",
            prefix=prefix,
        )


def test_provider_representation_does_not_expose_api_key() -> None:
    """
    The API key must not appear in repr output.
    """
    api_key = "highly-sensitive-api-key"

    provider = ApiKeyAuthenticationProvider(
        api_key=api_key,
        header_name="Authorization",
        prefix="Bearer",
    )

    provider_representation = repr(provider)

    assert api_key not in provider_representation
    assert "Authorization" in provider_representation
    assert "Bearer" in provider_representation


def test_configuration_exception_does_not_expose_api_key() -> None:
    """
    Invalid-configuration errors must not include credential values.
    """
    api_key = "   "

    with pytest.raises(
        AuthenticationConfigurationException,
    ) as exception_info:
        ApiKeyAuthenticationProvider(
            api_key=api_key,
        )

    assert api_key not in str(exception_info.value)