"""
SupplyMind Enterprise AI

Authentication Runtime Model Tests
"""

from dataclasses import FrozenInstanceError

import pytest

from supplymind.authentication.base.exceptions import (
    AuthenticationConfigurationException,
)
from supplymind.authentication.models import OAuth2AccessToken


def test_oauth2_access_token_normalizes_values() -> None:
    """
    OAuth2 access token values should be normalized.
    """
    token = OAuth2AccessToken(
        access_token="  access-token  ",
        token_type="  Bearer  ",
        expires_in=3600,
        scope="  api.read  ",
    )

    assert token.access_token == "access-token"
    assert token.token_type == "Bearer"
    assert token.expires_in == 3600
    assert token.scope == "api.read"


def test_oauth2_access_token_allows_missing_scope() -> None:
    """
    OAuth2 access token responses may omit the granted scope.
    """
    token = OAuth2AccessToken(
        access_token="access-token",
        token_type="Bearer",
        expires_in=3600,
    )

    assert token.scope is None


@pytest.mark.parametrize(
    "access_token",
    ["", " ", "   ", "\t", "\n"],
)
def test_oauth2_access_token_rejects_empty_access_token(
    access_token: str,
) -> None:
    """
    The access token must contain a meaningful value.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="non-empty access token",
    ):
        OAuth2AccessToken(
            access_token=access_token,
            token_type="Bearer",
            expires_in=3600,
        )


@pytest.mark.parametrize(
    "token_type",
    ["", " ", "   ", "\t", "\n"],
)
def test_oauth2_access_token_rejects_empty_token_type(
    token_type: str,
) -> None:
    """
    The token type must contain a meaningful value.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="non-empty token type",
    ):
        OAuth2AccessToken(
            access_token="access-token",
            token_type=token_type,
            expires_in=3600,
        )


@pytest.mark.parametrize(
    "expires_in",
    [0, -1, -3600],
)
def test_oauth2_access_token_rejects_non_positive_expiration(
    expires_in: int,
) -> None:
    """
    Token expiration must be positive.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="positive expiration time",
    ):
        OAuth2AccessToken(
            access_token="access-token",
            token_type="Bearer",
            expires_in=expires_in,
        )


@pytest.mark.parametrize(
    "scope",
    ["", " ", "   ", "\t", "\n"],
)
def test_oauth2_access_token_rejects_empty_scope(
    scope: str,
) -> None:
    """
    A supplied scope must contain a meaningful value.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="scope must be non-empty",
    ):
        OAuth2AccessToken(
            access_token="access-token",
            token_type="Bearer",
            expires_in=3600,
            scope=scope,
        )


def test_oauth2_access_token_hides_secret() -> None:
    """
    The access token must not appear in repr output.
    """
    access_token = "highly-sensitive-access-token"

    token = OAuth2AccessToken(
        access_token=access_token,
        token_type="Bearer",
        expires_in=3600,
    )

    assert access_token not in repr(token)


def test_oauth2_access_token_is_immutable() -> None:
    """
    Runtime token models should be immutable.
    """
    token = OAuth2AccessToken(
        access_token="access-token",
        token_type="Bearer",
        expires_in=3600,
    )

    with pytest.raises(FrozenInstanceError):
        token.expires_in = 7200
