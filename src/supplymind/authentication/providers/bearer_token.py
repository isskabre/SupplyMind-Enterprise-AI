"""
SupplyMind Enterprise AI

Bearer Token Authentication Provider

Produces immutable HTTP Authorization headers using a bearer token.
"""

from __future__ import annotations

from dataclasses import dataclass

from supplymind.authentication.base.models import AuthenticationHeaders
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


@dataclass(frozen=True, slots=True)
class BearerTokenAuthenticationProvider(
    AuthenticationProviderProtocol,
):
    """
    Produce Authorization headers using validated configuration.
    """

    configuration: BearerTokenAuthenticationConfiguration

    async def get_headers(self) -> AuthenticationHeaders:
        """
        Produce immutable bearer authentication headers.
        """
        configuration = self.configuration

        return AuthenticationHeaders(
            {
                AUTHORIZATION_HEADER: (
                    f"{BEARER_PREFIX} {configuration.token}"
                )
            }
        )