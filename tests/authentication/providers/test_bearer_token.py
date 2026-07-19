"""
SupplyMind Enterprise AI

Bearer Token Authentication Provider Tests
"""

import pytest

from supplymind.authentication.base.exceptions import (
    AuthenticationConfigurationException,
)
from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
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
    provider = BearerTokenAuthenticationProvider(
        token="test-token",
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        AUTHORIZATION_HEADER: f"{BEARER_PREFIX} test-token",
    }


@pytest.mark.anyio
async def test_provider_normalizes_token_whitespace() -> None:
    """
    Surrounding token whitespace should be removed during construction.
    """
    provider = BearerTokenAuthenticationProvider(
        token="  test-token  ",
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        AUTHORIZATION_HEADER: f"{BEARER_PREFIX} test-token",
    }


def test_provider_implements_authentication_protocol() -> None:
    """
    The concrete provider should satisfy the authentication protocol.
    """
    provider = BearerTokenAuthenticationProvider(
        token="test-token",
    )

    assert isinstance(
        provider,
        AuthenticationProviderProtocol,
    )


@pytest.mark.parametrize(
    "token",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_provider_rejects_empty_token(token: str) -> None:
    """
    Empty or whitespace-only bearer tokens should be rejected.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="non-empty token",
    ):
        BearerTokenAuthenticationProvider(
            token=token,
        )


def test_provider_representation_does_not_expose_token() -> None:
    """
    The bearer token must not appear in repr output.
    """
    token = "highly-sensitive-bearer-token"

    provider = BearerTokenAuthenticationProvider(
        token=token,
    )

    provider_representation = repr(provider)

    assert token not in provider_representation
    assert provider_representation == (
        "BearerTokenAuthenticationProvider()"
    )


def test_invalid_token_exception_does_not_expose_raw_input() -> None:
    """
    Invalid-token errors must not expose the raw credential input.
    """
    raw_token = "\t\n"

    with pytest.raises(
        AuthenticationConfigurationException,
    ) as exception_info:
        BearerTokenAuthenticationProvider(
            token=raw_token,
        )

    assert raw_token not in str(exception_info.value)