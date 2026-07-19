"""
SupplyMind Enterprise AI

Authentication Protocol Tests
"""
import pytest

from supplymind.authentication.base.models import AuthenticationHeaders
from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)


class ValidAuthenticationProvider:
    """
    Test provider satisfying the authentication protocol.
    """

    async def get_headers(self) -> AuthenticationHeaders:
        return AuthenticationHeaders(
            {
                "Authorization": "Bearer test-token",
            }
        )


class InvalidAuthenticationProvider:
    """
    Test provider that does not satisfy the authentication protocol.
    """


def test_valid_provider_satisfies_protocol() -> None:
    provider = ValidAuthenticationProvider()

    assert isinstance(
        provider,
        AuthenticationProviderProtocol,
    )


def test_invalid_provider_does_not_satisfy_protocol() -> None:
    provider = InvalidAuthenticationProvider()

    assert not isinstance(
        provider,
        AuthenticationProviderProtocol,
    )


@pytest.mark.anyio
async def test_valid_provider_returns_authentication_headers() -> None:
    provider = ValidAuthenticationProvider()

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        "Authorization": "Bearer test-token",
    }