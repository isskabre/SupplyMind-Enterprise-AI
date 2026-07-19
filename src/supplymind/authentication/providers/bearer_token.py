"""
SupplyMind Enterprise AI

Bearer Token Authentication Provider

Produces immutable HTTP Authorization headers using a bearer token.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from supplymind.authentication.base.exceptions import (
    AuthenticationConfigurationException,
)
from supplymind.authentication.base.models import AuthenticationHeaders
from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
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
    Produce an Authorization header using a configured bearer token.

    The token is excluded from the object's representation to reduce the
    risk of credentials appearing in logs or debugging output.

    Attributes:
        token: Secret bearer token used to authorize an HTTP request.
    """

    token: str = field(repr=False)

    def __post_init__(self) -> None:
        """
        Validate and normalize provider configuration.

        Raises:
            AuthenticationConfigurationException:
                If the bearer token is empty or contains only whitespace.
        """
        normalized_token = self.token.strip()

        if not normalized_token:
            raise AuthenticationConfigurationException(
                message=(
                    "Bearer token authentication requires a non-empty token."
                ),
            )

        object.__setattr__(
            self,
            "token",
            normalized_token,
        )

    async def get_headers(self) -> AuthenticationHeaders:
        """
        Produce immutable bearer-token authentication headers.

        Returns:
            An Authorization header containing the configured bearer token.
        """
        return AuthenticationHeaders(
            {
                AUTHORIZATION_HEADER: (
                    f"{BEARER_PREFIX} {self.token}"
                ),
            }
        )