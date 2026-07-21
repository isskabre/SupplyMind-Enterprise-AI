"""
SupplyMind Enterprise AI

OAuth2 Client Credentials Authentication Provider Tests
"""

from typing import Any

import pytest

from supplymind.authentication.configuration import (
    OAuth2ClientCredentialsConfiguration,
)
from supplymind.authentication.providers.oauth2_client_credentials import (
    OAuth2ClientCredentialsAuthenticationProvider,
)
from supplymind.connectors.api.models import HttpResponse
from supplymind.authentication.base.exceptions import (
    TokenAcquisitionException,
)
from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)


class StubHttpClient:
    """
    Record HTTP requests and return a configured response.
    """

    def __init__(self, response: HttpResponse) -> None:
        self.response = response
        self.method: str | None = None
        self.url: str | None = None
        self.data: dict[str, Any] | None = None

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Any | None = None,
        headers: Any | None = None,
        data: Any | None = None,
        json: Any | None = None,
    ) -> HttpResponse:
        self.method = method
        self.url = url
        self.data = dict(data) if data is not None else None

        return self.response

    async def get(
        self,
        url: str,
        *,
        params: Any | None = None,
        headers: Any | None = None,
    ) -> HttpResponse:
        raise NotImplementedError

    async def close(self) -> None:
        return None


@pytest.mark.anyio
async def test_request_access_token_returns_normalized_token() -> None:
    """
    The provider should request and normalize a successful token response.
    """
    response = HttpResponse(
        status_code=200,
        content=(
            b'{"access_token":" access-token ",'
            b'"token_type":" Bearer ",'
            b'"expires_in":3600,'
            b'"scope":" api.read "}'
        ),
    )
    http_client = StubHttpClient(response)

    configuration = OAuth2ClientCredentialsConfiguration(
        client_id="client-id",
        client_secret="client-secret",
        token_url="https://example.com/oauth/token",
        scope="api.read",
    )
    provider = OAuth2ClientCredentialsAuthenticationProvider(
        configuration=configuration,
        http_client=http_client,
    )

    token = await provider._request_access_token()

    assert http_client.method == "POST"
    assert http_client.url == "https://example.com/oauth/token"
    assert http_client.data == {
        "grant_type": "client_credentials",
        "client_id": "client-id",
        "client_secret": "client-secret",
        "scope": "api.read",
    }

    assert token.access_token == "access-token"
    assert token.token_type == "Bearer"
    assert token.expires_in == 3600
    assert token.scope == "api.read"


@pytest.mark.anyio
async def test_request_access_token_rejects_http_error() -> None:
    """
    A non-success HTTP response should raise TokenAcquisitionException.
    """
    response = HttpResponse(
        status_code=401,
        content=b'{"error":"invalid_client"}',
    )

    http_client = StubHttpClient(response)

    configuration = OAuth2ClientCredentialsConfiguration(
        client_id="client-id",
        client_secret="client-secret",
        token_url="https://example.com/oauth/token",
    )

    provider = OAuth2ClientCredentialsAuthenticationProvider(
        configuration=configuration,
        http_client=http_client,
    )

    with pytest.raises(
        TokenAcquisitionException,
        match="OAuth2 access token request failed",
    ):
        await provider._request_access_token()


@pytest.mark.anyio
async def test_request_access_token_rejects_invalid_payload() -> None:
    """
    Missing required token fields should raise TokenAcquisitionException.
    """
    response = HttpResponse(
        status_code=200,
        content=b'{"unexpected":"value"}',
    )

    http_client = StubHttpClient(response)

    configuration = OAuth2ClientCredentialsConfiguration(
        client_id="client-id",
        client_secret="client-secret",
        token_url="https://example.com/oauth/token",
    )

    provider = OAuth2ClientCredentialsAuthenticationProvider(
        configuration=configuration,
        http_client=http_client,
    )

    with pytest.raises(
        TokenAcquisitionException,
        match="OAuth2 token response was invalid",
    ):
        await provider._request_access_token()


@pytest.mark.anyio
async def test_get_headers_returns_bearer_authorization_header() -> None:
    """
    The provider should convert the acquired token into bearer headers.
    """
    response = HttpResponse(
        status_code=200,
        content=(
            b'{"access_token":"access-token","token_type":"Bearer","expires_in":3600}'
        ),
    )
    http_client = StubHttpClient(response)

    configuration = OAuth2ClientCredentialsConfiguration(
        client_id="client-id",
        client_secret="client-secret",
        token_url="https://example.com/oauth/token",
    )
    provider = OAuth2ClientCredentialsAuthenticationProvider(
        configuration=configuration,
        http_client=http_client,
    )

    headers = await provider.get_headers()

    assert headers.as_dict() == {
        "Authorization": "Bearer access-token",
    }


def test_provider_implements_authentication_protocol() -> None:
    """
    The OAuth2 provider should satisfy the shared authentication protocol.
    """
    response = HttpResponse(
        status_code=200,
        content=(
            b'{"access_token":"access-token","token_type":"Bearer","expires_in":3600}'
        ),
    )
    provider = OAuth2ClientCredentialsAuthenticationProvider(
        configuration=OAuth2ClientCredentialsConfiguration(
            client_id="client-id",
            client_secret="client-secret",
            token_url="https://example.com/oauth/token",
        ),
        http_client=StubHttpClient(response),
    )

    assert isinstance(
        provider,
        AuthenticationProviderProtocol,
    )
