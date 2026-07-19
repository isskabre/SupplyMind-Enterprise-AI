"""
SupplyMind Enterprise AI

API Key Authentication Provider

Produces immutable HTTP authentication headers from an API key.
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
from supplymind.authentication.constants import API_KEY_HEADER


@dataclass(frozen=True, slots=True)
class ApiKeyAuthenticationProvider(AuthenticationProviderProtocol):
    """
    Produce authentication headers using a configured API key.

    The API key is excluded from the object's representation to reduce
    the risk of credentials appearing in logs or debugging output.

    Attributes:
        api_key: Secret API credential.
        header_name: HTTP header used to transmit the credential.
        prefix: Optional value placed before the API key, such as "Bearer".
    """

    api_key: str = field(repr=False)
    header_name: str = API_KEY_HEADER
    prefix: str | None = None

    def __post_init__(self) -> None:
        """
        Validate and normalize provider configuration.

        Raises:
            AuthenticationConfigurationException:
                If required configuration values are missing or invalid.
        """
        normalized_api_key = self.api_key.strip()
        normalized_header_name = self.header_name.strip()
        normalized_prefix = (
            self.prefix.strip()
            if self.prefix is not None
            else None
        )

        if not normalized_api_key:
            raise AuthenticationConfigurationException(
                message="API key authentication requires a non-empty API key.",
            )

        if not normalized_header_name:
            raise AuthenticationConfigurationException(
                message=(
                    "API key authentication requires a non-empty "
                    "header name."
                ),
            )

        if self.prefix is not None and not normalized_prefix:
            raise AuthenticationConfigurationException(
                message=(
                    "API key authentication prefix must be non-empty "
                    "when provided."
                ),
            )

        object.__setattr__(self, "api_key", normalized_api_key)
        object.__setattr__(
            self,
            "header_name",
            normalized_header_name,
        )
        object.__setattr__(self, "prefix", normalized_prefix)

    async def get_headers(self) -> AuthenticationHeaders:
        """
        Produce immutable authentication headers.

        Returns:
            Authentication headers containing the configured API key.
        """
        header_value = (
            f"{self.prefix} {self.api_key}"
            if self.prefix is not None
            else self.api_key
        )

        return AuthenticationHeaders(
            {
                self.header_name: header_value,
            }
        )