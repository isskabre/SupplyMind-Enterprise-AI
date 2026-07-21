"""
SupplyMind Enterprise AI

Authentication Models

Runtime models shared across authentication providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from supplymind.authentication.base.exceptions import (
    AuthenticationConfigurationException,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OAuth2AccessToken:
    """
    Immutable OAuth2 access token returned by an authorization server.

    Attributes:
        access_token:
            Token used to authenticate future HTTP requests.
        token_type:
            Usually "Bearer".
        expires_in:
            Lifetime of the token in seconds.
        scope:
            Granted OAuth2 scope, if provided.
    """

    access_token: str = field(repr=False)
    token_type: str
    expires_in: int
    scope: str | None = None

    def __post_init__(self) -> None:
        """
        Validate and normalize the OAuth2 access token.

        Raises:
            AuthenticationConfigurationException:
                If required token values are missing or invalid.
        """
        normalized_access_token = self.access_token.strip()
        normalized_token_type = self.token_type.strip()
        normalized_scope = self.scope.strip() if self.scope is not None else None

        if not normalized_access_token:
            raise AuthenticationConfigurationException(
                message=("OAuth2 access token requires a non-empty access token."),
            )

        if not normalized_token_type:
            raise AuthenticationConfigurationException(
                message=("OAuth2 access token requires a non-empty token type."),
            )

        if self.expires_in <= 0:
            raise AuthenticationConfigurationException(
                message=("OAuth2 access token requires a positive expiration time."),
            )

        if self.scope is not None and not normalized_scope:
            raise AuthenticationConfigurationException(
                message=("OAuth2 access token scope must be non-empty when provided."),
            )

        object.__setattr__(
            self,
            "access_token",
            normalized_access_token,
        )
        object.__setattr__(
            self,
            "token_type",
            normalized_token_type,
        )
        object.__setattr__(
            self,
            "scope",
            normalized_scope,
        )
