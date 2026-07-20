"""
SupplyMind Enterprise AI

Authentication Configuration Models

Immutable configuration models for authentication providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from supplymind.authentication.base.exceptions import (
    AuthenticationConfigurationException,
)
from supplymind.authentication.constants import API_KEY_HEADER


@dataclass(frozen=True, slots=True)
class ApiKeyAuthenticationConfiguration:
    """
    Immutable configuration for API key authentication.

    Secret values are excluded from the object's representation to reduce
    the risk of credentials appearing in logs or debugging output.

    Attributes:
        api_key: Secret API credential.
        header_name: HTTP header used to transmit the credential.
        prefix: Optional value placed before the API key.
    """

    api_key: str = field(repr=False)
    header_name: str = API_KEY_HEADER
    prefix: str | None = None

    def __post_init__(self) -> None:
        """
        Validate and normalize API key authentication configuration.

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
                message=(
                    "API key authentication configuration requires "
                    "a non-empty API key."
                ),
            )

        if not normalized_header_name:
            raise AuthenticationConfigurationException(
                message=(
                    "API key authentication configuration requires "
                    "a non-empty header name."
                ),
            )

        if self.prefix is not None and not normalized_prefix:
            raise AuthenticationConfigurationException(
                message=(
                    "API key authentication configuration prefix must "
                    "be non-empty when provided."
                ),
            )

        object.__setattr__(
            self,
            "api_key",
            normalized_api_key,
        )
        object.__setattr__(
            self,
            "header_name",
            normalized_header_name,
        )
        object.__setattr__(
            self,
            "prefix",
            normalized_prefix,
        )


@dataclass(frozen=True, slots=True)
class BearerTokenAuthenticationConfiguration:
    """
    Immutable configuration for bearer-token authentication.

    The bearer token is excluded from the object's representation to reduce
    the risk of credentials appearing in logs or debugging output.

    Attributes:
        token: Secret bearer token.
    """

    token: str = field(repr=False)

    def __post_init__(self) -> None:
        """
        Validate and normalize bearer-token authentication configuration.

        Raises:
            AuthenticationConfigurationException:
                If the token is empty or contains only whitespace.
        """
        normalized_token = self.token.strip()

        if not normalized_token:
            raise AuthenticationConfigurationException(
                message=(
                    "Bearer token authentication configuration requires "
                    "a non-empty token."
                ),
            )

        object.__setattr__(
            self,
            "token",
            normalized_token,
        )