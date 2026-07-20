"""
SupplyMind Enterprise AI

API Key Authentication Provider

Produces immutable HTTP authentication headers from validated configuration.
"""

from __future__ import annotations

from dataclasses import dataclass

from supplymind.authentication.base.models import AuthenticationHeaders
from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)
from supplymind.authentication.configuration import (
    ApiKeyAuthenticationConfiguration,
)


@dataclass(frozen=True, slots=True)
class ApiKeyAuthenticationProvider(
    AuthenticationProviderProtocol,
):
    """
    Produce authentication headers using validated API key configuration.

    Configuration validation and normalization are owned by
    `ApiKeyAuthenticationConfiguration`.

    Attributes:
        configuration: Validated immutable API key configuration.
    """

    configuration: ApiKeyAuthenticationConfiguration

    async def get_headers(self) -> AuthenticationHeaders:
        """
        Produce immutable authentication headers.

        Returns:
            Authentication headers containing the configured API key.
        """
        configuration = self.configuration

        header_value = (
            f"{configuration.prefix} {configuration.api_key}"
            if configuration.prefix is not None
            else configuration.api_key
        )

        return AuthenticationHeaders(
            {
                configuration.header_name: header_value,
            }
        )