"""
SupplyMind Enterprise AI

Authentication Factory

Centralized creation of enterprise authentication providers.
"""

from __future__ import annotations

from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)
from supplymind.authentication.configuration import (
    ApiKeyAuthenticationConfiguration,
    BearerTokenAuthenticationConfiguration,
)
from supplymind.authentication.constants import API_KEY_HEADER
from supplymind.authentication.providers import (
    ApiKeyAuthenticationProvider,
    BearerTokenAuthenticationProvider,
)


class AuthenticationFactory:
    """
    Create authentication providers through a centralized construction API.

    The factory creates validated configuration objects, injects them into
    concrete providers, and returns the shared authentication abstraction.
    """

    @staticmethod
    def create_api_key(
        api_key: str,
        header_name: str = API_KEY_HEADER,
        prefix: str | None = None,
    ) -> AuthenticationProviderProtocol:
        """
        Create an API key authentication provider.

        Args:
            api_key: Secret API credential.
            header_name: HTTP header used to transmit the API key.
            prefix: Optional value placed before the API key.

        Returns:
            An authentication provider implementing the shared protocol.
        """
        configuration = ApiKeyAuthenticationConfiguration(
            api_key=api_key,
            header_name=header_name,
            prefix=prefix,
        )

        return ApiKeyAuthenticationProvider(
            configuration=configuration,
        )

    @staticmethod
    def create_bearer(
        token: str,
    ) -> AuthenticationProviderProtocol:
        """
        Create a bearer-token authentication provider.

        Args:
            token: Secret bearer token.

        Returns:
            An authentication provider implementing the shared protocol.
        """
        configuration = BearerTokenAuthenticationConfiguration(
            token=token,
        )

        return BearerTokenAuthenticationProvider(
            configuration=configuration,
        )
