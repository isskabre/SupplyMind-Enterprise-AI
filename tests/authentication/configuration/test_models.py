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
    OAuth2ClientCredentialsConfiguration,
)
from supplymind.authentication.constants import API_KEY_HEADER


def test_api_key_configuration_defaults() -> None:
    """
    Default values should be applied correctly.
    """
    configuration = ApiKeyAuthenticationConfiguration(
        api_key="secret",
    )

    assert configuration.header_name == API_KEY_HEADER
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


def test_oauth2_configuration_defaults() -> None:
    """
    Optional OAuth2 configuration should use the expected defaults.
    """
    configuration = OAuth2ClientCredentialsConfiguration(
        client_id="client-id",
        client_secret="client-secret",
        token_url="https://example.com/oauth/token",
    )

    assert configuration.scope is None


def test_oauth2_configuration_normalizes_values() -> None:
    """
    OAuth2 configuration values should be normalized.
    """
    configuration = OAuth2ClientCredentialsConfiguration(
        client_id="  client-id  ",
        client_secret="  client-secret  ",
        token_url="  https://example.com/oauth/token  ",
        scope="  api.read  ",
    )

    assert configuration.client_id == "client-id"
    assert configuration.client_secret == "client-secret"
    assert configuration.token_url == "https://example.com/oauth/token"
    assert configuration.scope == "api.read"


@pytest.mark.parametrize(
    "client_id",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_oauth2_configuration_rejects_empty_client_id(
    client_id: str,
) -> None:
    """
    OAuth2 configuration requires a non-empty client ID.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="non-empty client ID",
    ):
        OAuth2ClientCredentialsConfiguration(
            client_id=client_id,
            client_secret="client-secret",
            token_url="https://example.com/oauth/token",
        )


@pytest.mark.parametrize(
    "client_secret",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_oauth2_configuration_rejects_empty_client_secret(
    client_secret: str,
) -> None:
    """
    OAuth2 configuration requires a non-empty client secret.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="non-empty client secret",
    ):
        OAuth2ClientCredentialsConfiguration(
            client_id="client-id",
            client_secret=client_secret,
            token_url="https://example.com/oauth/token",
        )


@pytest.mark.parametrize(
    "token_url",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_oauth2_configuration_rejects_empty_token_url(
    token_url: str,
) -> None:
    """
    OAuth2 configuration requires a non-empty token URL.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="non-empty token URL",
    ):
        OAuth2ClientCredentialsConfiguration(
            client_id="client-id",
            client_secret="client-secret",
            token_url=token_url,
        )


@pytest.mark.parametrize(
    "scope",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_oauth2_configuration_rejects_empty_scope(
    scope: str,
) -> None:
    """
    A supplied OAuth2 scope must contain a meaningful value.
    """
    with pytest.raises(
        AuthenticationConfigurationException,
        match="scope must be non-empty",
    ):
        OAuth2ClientCredentialsConfiguration(
            client_id="client-id",
            client_secret="client-secret",
            token_url="https://example.com/oauth/token",
            scope=scope,
        )


def test_oauth2_configuration_hides_credentials() -> None:
    """
    OAuth2 credentials must not appear in repr output.
    """
    client_id = "sensitive-client-id"
    client_secret = "highly-sensitive-client-secret"
    token_url = "https://example.com/oauth/token"

    configuration = OAuth2ClientCredentialsConfiguration(
        client_id=client_id,
        client_secret=client_secret,
        token_url=token_url,
        scope="api.read",
    )

    representation = repr(configuration)

    assert client_id not in representation
    assert client_secret not in representation
    assert token_url in representation
    assert "api.read" in representation
