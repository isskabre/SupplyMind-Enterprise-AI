from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)
from supplymind.connectors.api.models import HttpResponse
from supplymind.connectors.api.protocols import HttpClientProtocol
from supplymind.connectors.sharepoint.exceptions import (
    SharePointAuthenticationException,
    SharePointAuthorizationException,
    SharePointSiteNotFoundException,
)
from supplymind.connectors.sharepoint.models import (
    SharePointConnectorConfiguration,
    SharePointDrive,
    SharePointSite,
)
from supplymind.connectors.sharepoint.urls import SharePointUrls


class SharePointConnector:
    """
    Connector for accessing SharePoint resources through Microsoft Graph.

    The connector receives its dependencies through constructor injection
    so that authentication and HTTP transport remain replaceable and
    independently testable.
    """

    def __init__(
        self,
        http_client: HttpClientProtocol,
        authentication_provider: AuthenticationProviderProtocol,
        configuration: SharePointConnectorConfiguration,
    ) -> None:
        self._http_client = http_client
        self._authentication_provider = authentication_provider
        self._configuration = configuration

    async def get_site(self) -> SharePointSite:
        """
        Retrieve the configured SharePoint site through Microsoft Graph.

        Returns:
            The resolved SharePoint site.

        Raises:
            SharePointAuthenticationException:
                If Microsoft Graph rejects the authentication credentials.

            SharePointAuthorizationException:
                If the authenticated identity lacks permission to access
                the SharePoint site.

            SharePointSiteNotFoundException:
                If Microsoft Graph cannot find the configured site.
        """
        authentication_headers = await self._authentication_provider.get_headers()

        response = await self._http_client.get(
            url=SharePointUrls.site(self._configuration),
            headers=authentication_headers.as_dict(),
        )

        self._raise_for_error(response)

        return SharePointSite.model_validate(
            response.content,
        )

    async def get_default_drive(self) -> SharePointDrive:
        """
        Retrieve the default SharePoint document library.

        Returns:
            The default SharePoint drive.

        Raises:
            SharePointAuthenticationException:
                If Microsoft Graph rejects the authentication credentials.

            SharePointAuthorizationException:
                If the authenticated identity lacks permission to access
                the SharePoint drive.

            SharePointSiteNotFoundException:
                If the configured SharePoint site cannot be found.
        """
        site = await self.get_site()

        authentication_headers = await self._authentication_provider.get_headers()

        response = await self._http_client.get(
            url=SharePointUrls.drive(
                self._configuration,
                site.id,
            ),
            headers=authentication_headers.as_dict(),
        )

        self._raise_for_error(response)

        return SharePointDrive.model_validate(
            response.content,
        )

    def _raise_for_error(
        self,
        response: HttpResponse,
    ) -> None:
        """
        Translate HTTP responses into SharePoint-specific exceptions.

        Args:
            response:
                Response returned by Microsoft Graph.

        Raises:
            SharePointAuthenticationException:
                If Microsoft Graph rejects the authentication credentials.

            SharePointAuthorizationException:
                If the authenticated identity lacks permission to access
                the SharePoint resource.

            SharePointSiteNotFoundException:
                If the configured SharePoint site does not exist.
        """
        if response.status_code == 401:
            raise SharePointAuthenticationException("SharePoint authentication failed.")

        if response.status_code == 403:
            raise SharePointAuthorizationException(
                "Access to the SharePoint resource was denied."
            )

        if response.status_code == 404:
            raise SharePointSiteNotFoundException(
                "The configured SharePoint site was not found."
            )
