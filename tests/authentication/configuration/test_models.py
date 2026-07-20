"""
SupplyMind Enterprise AI

Authentication Configuration Model Tests
"""

import pytest

from supplymind.authentication.base.exceptions import (
    AuthenticationConfigurationException,
)
from supplymind.authentication.configuration import (
    ApiKeyAuthenticationConfiguration,
    BearerTokenAuthenticationConfiguration,
)


def test_api_key_configuration_defaults() -> None:
    """
    Default values should be applied correctly.
    """
    configuration = ApiKeyAuthenticationConfiguration(
        api_key="secret",
    )

    assert configuration.header_name == "X-API-Key"
    assert configuration.prefix is None


def test_api_key_configuration_normalizes_values() -> None:
    """
    Configuration values should be normalized.
    """
    configuration = ApiKeyAuthenticationConfiguration(
        api_key="  secret  ",
        header_name="  X-Test-Key  ",
        prefix="  Bearer  ",
    )

    assert configuration.api_key == "secret"
    assert configuration.header_name == "X-Test-Key"
    assert configuration.prefix == "Bearer"


@pytest.mark.parametrize(
    "api_key",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_api_key_configuration_rejects_empty_api_key(
    api_key: str,
) -> None:
    """
    API key configuration requires a non-empty API key.
    """
    with pytest.raises(AuthenticationConfigurationException):
        ApiKeyAuthenticationConfiguration(
            api_key=api_key,
        )


@pytest.mark.parametrize(
    "header_name",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_api_key_configuration_rejects_empty_header(
    header_name: str,
) -> None:
    """
    Header names cannot be empty.
    """
    with pytest.raises(AuthenticationConfigurationException):
        ApiKeyAuthenticationConfiguration(
            api_key="secret",
            header_name=header_name,
        )


def test_api_key_configuration_hides_secret() -> None:
    """
    Secret values must never appear in repr().
    """
    secret = "super-secret"

    configuration = ApiKeyAuthenticationConfiguration(
        api_key=secret,
    )

    assert secret not in repr(configuration)


def test_bearer_configuration_normalizes_token() -> None:
    """
    Bearer tokens should be normalized.
    """
    configuration = BearerTokenAuthenticationConfiguration(
        token="  secret-token  ",
    )

    assert configuration.token == "secret-token"


@pytest.mark.parametrize(
    "token",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_bearer_configuration_rejects_empty_token(
    token: str,
) -> None:
    """
    Bearer token configuration requires a non-empty token.
    """
    with pytest.raises(AuthenticationConfigurationException):
        BearerTokenAuthenticationConfiguration(
            token=token,
        )


def test_bearer_configuration_hides_token() -> None:
    """
    Bearer tokens must never appear in repr().
    """
    token = "very-secret"

    configuration = BearerTokenAuthenticationConfiguration(
        token=token,
    )

    assert token not in repr(configuration)