"""
SupplyMind Enterprise AI

OAuth2 Client Credentials Authentication Provider

Obtains OAuth2 access tokens using the Client Credentials flow.
"""

from __future__ import annotations

from dataclasses import dataclass

from supplymind.authentication.base.exceptions import (
    TokenAcquisitionException,
)
from supplymind.authentication.base.models import AuthenticationHeaders
from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)
from supplymind.authentication.configuration import (
    BearerTokenAuthenticationConfiguration,
    OAuth2ClientCredentialsConfiguration,
)
from supplymind.authentication.models import OAuth2AccessToken
from supplymind.authentication.providers.bearer_token import (
    BearerTokenAuthenticationProvider,
)
from supplymind.connectors.api.protocols import HttpClientProtocol


@dataclass(
    frozen=True,
    slots=True,
)
class OAuth2ClientCredentialsAuthenticationProvider(
    AuthenticationProviderProtocol,
):
    """
    Acquire OAuth2 access tokens using the Client Credentials flow.
    """

    configuration: OAuth2ClientCredentialsConfiguration
    http_client: HttpClientProtocol

    def _build_token_request_data(self) -> dict[str, str]:
        """
        Build the OAuth2 Client Credentials request payload.

        Returns:
            Form data required by the OAuth2 token endpoint.
        """
        configuration = self.configuration

        request_data = {
            "grant_type": "client_credentials",
            "client_id": configuration.client_id,
            "client_secret": configuration.client_secret,
        }

        if configuration.scope is not None:
            request_data["scope"] = configuration.scope

        return request_data

    async def _request_access_token(self) -> OAuth2AccessToken:
        """
        Request and normalize an OAuth2 access token.

        Returns:
            A validated OAuth2 access token.

        Raises:
            TokenAcquisitionException:
                If the authorization server rejects the request or returns
                an invalid response.
        """
        response = await self.http_client.request(
            method="POST",
            url=self.configuration.token_url,
            data=self._build_token_request_data(),
        )

        if not response.is_success:
            raise TokenAcquisitionException(
                message="OAuth2 access token request failed.",
                details={
                    "status_code": response.status_code,
                    "token_url": self.configuration.token_url,
                },
            )

        try:
            payload = response.json()

            return OAuth2AccessToken(
                access_token=str(payload["access_token"]),
                token_type=str(payload["token_type"]),
                expires_in=int(payload["expires_in"]),
                scope=(
                    str(payload["scope"]) if payload.get("scope") is not None else None
                ),
            )
        except (
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            raise TokenAcquisitionException(
                message="OAuth2 token response was invalid.",
                details={
                    "status_code": response.status_code,
                    "token_url": self.configuration.token_url,
                },
            ) from exc

    async def get_headers(self) -> AuthenticationHeaders:
        """
        Acquire an OAuth2 token and produce authentication headers.

        Returns:
            Immutable bearer authentication headers.
        """
        access_token = await self._request_access_token()

        bearer_configuration = BearerTokenAuthenticationConfiguration(
            token=access_token.access_token,
        )
        bearer_provider = BearerTokenAuthenticationProvider(
            configuration=bearer_configuration,
        )

        return await bearer_provider.get_headers()
