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
        normalized_prefix = self.prefix.strip() if self.prefix is not None else None

        if not normalized_api_key:
            raise AuthenticationConfigurationException(
                message=(
                    "API key authentication configuration requires a non-empty API key."
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


@dataclass(frozen=True, slots=True)
class OAuth2ClientCredentialsConfiguration:
    """
    Immutable OAuth2 Client Credentials configuration.

    Secret values are excluded from the object's representation to reduce
    the risk of credentials appearing in logs or debugging output.

    Attributes:
        client_id: OAuth2 application client identifier.
        client_secret: Secret used to authenticate the client.
        token_url: OAuth2 authorization server token endpoint.
        scope: Optional OAuth2 scope requested during token acquisition.
    """

    client_id: str = field(repr=False)
    client_secret: str = field(repr=False)
    token_url: str
    scope: str | None = None

    def __post_init__(self) -> None:
        """
        Validate and normalize OAuth2 Client Credentials configuration.

        Raises:
            AuthenticationConfigurationException:
                If required configuration values are missing or invalid.
        """
        normalized_client_id = self.client_id.strip()
        normalized_client_secret = self.client_secret.strip()
        normalized_token_url = self.token_url.strip()
        normalized_scope = self.scope.strip() if self.scope is not None else None

        if not normalized_client_id:
            raise AuthenticationConfigurationException(
                message=(
                    "OAuth2 Client Credentials configuration requires "
                    "a non-empty client ID."
                ),
            )

        if not normalized_client_secret:
            raise AuthenticationConfigurationException(
                message=(
                    "OAuth2 Client Credentials configuration requires "
                    "a non-empty client secret."
                ),
            )

        if not normalized_token_url:
            raise AuthenticationConfigurationException(
                message=(
                    "OAuth2 Client Credentials configuration requires "
                    "a non-empty token URL."
                ),
            )

        if self.scope is not None and not normalized_scope:
            raise AuthenticationConfigurationException(
                message=(
                    "OAuth2 Client Credentials configuration scope must "
                    "be non-empty when provided."
                ),
            )

        object.__setattr__(
            self,
            "client_id",
            normalized_client_id,
        )
        object.__setattr__(
            self,
            "client_secret",
            normalized_client_secret,
        )
        object.__setattr__(
            self,
            "token_url",
            normalized_token_url,
        )
        object.__setattr__(
            self,
            "scope",
            normalized_scope,
        )
