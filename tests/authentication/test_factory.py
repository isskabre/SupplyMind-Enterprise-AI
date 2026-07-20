"""
SupplyMind Enterprise AI

Authentication Factory Tests
"""

import pytest

from supplymind.authentication.base.exceptions import (
    AuthenticationConfigurationException,
)
from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)
from supplymind.authentication.constants import API_KEY_HEADER
from supplymind.authentication.factory import AuthenticationFactory
from supplymind.authentication.providers import (
    ApiKeyAuthenticationProvider,
    BearerTokenAuthenticationProvider,
)


def test_create_api_key_returns_api_key_provider() -> None:
    """
    The factory should create an API key authentication provider.
    """
    provider = AuthenticationFactory.create_api_key(
        api_key="test-secret",
    )

    assert isinstance(
        provider,
        AuthenticationProviderProtocol,
    )
    assert isinstance(
        provider,
        ApiKeyAuthenticationProvider,
    )


def test_create_api_key_forwards_configuration() -> None:
    """
    The factory should pass API key configuration to the provider.
    """
    provider = AuthenticationFactory.create_api_key(
        api_key="test-secret",
        header_name="X-Internal-Key",
        prefix="Token",
    )

    assert isinstance(
        provider,
        ApiKeyAuthenticationProvider,
    )
    assert provider.header_name == "X-Internal-Key"
    assert provider.prefix == "Token"


def test_create_api_key_uses_default_header() -> None:
    """
    The factory should use the shared default API-key header.
    """
    provider = AuthenticationFactory.create_api_key(
        api_key="test-secret",
    )

    assert isinstance(
        provider,
        ApiKeyAuthenticationProvider,
    )
    assert provider.header_name == API_KEY_HEADER


def test_create_bearer_returns_bearer_provider() -> None:
    """
    The factory should create a bearer-token authentication provider.
    """
    provider = AuthenticationFactory.create_bearer(
        token="test-token",
    )

    assert isinstance(
        provider,
        AuthenticationProviderProtocol,
    )
    assert isinstance(
        provider,
        BearerTokenAuthenticationProvider,
    )


def test_factory_creates_independent_provider_instances() -> None:
    """
    Each factory call should create a new provider instance.
    """
    provider_one = AuthenticationFactory.create_api_key(
        api_key="secret-one",
    )
    provider_two = AuthenticationFactory.create_api_key(
        api_key="secret-two",
    )

    assert provider_one is not provider_two


def test_factory_does_not_expose_credentials_in_provider_repr() -> None:
    """
    Providers created by the factory should retain secret-safe representations.
    """
    api_key = "highly-sensitive-api-key"
    token = "highly-sensitive-token"

    api_key_provider = AuthenticationFactory.create_api_key(
        api_key=api_key,
    )
    bearer_provider = AuthenticationFactory.create_bearer(
        token=token,
    )

    assert api_key not in repr(api_key_provider)
    assert token not in repr(bearer_provider)


@pytest.mark.parametrize(
    "api_key",
    [
        "",
        " ",
        "\t",
        "\n",
    ],
)
def test_create_api_key_preserves_provider_validation(
    api_key: str,
) -> None:
    """
    The factory should allow provider validation errors to propagate.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="non-empty API key",
    ):
        AuthenticationFactory.create_api_key(
            api_key=api_key,
        )


@pytest.mark.parametrize(
    "token",
    [
        "",
        " ",
        "\t",
        "\n",
    ],
)
def test_create_bearer_preserves_provider_validation(
    token: str,
) -> None:
    """
    The factory should allow provider validation errors to propagate.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="non-empty token",
    ):
        AuthenticationFactory.create_bearer(
            token=token,
        )