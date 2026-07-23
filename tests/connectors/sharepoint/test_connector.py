from unittest.mock import AsyncMock, Mock

import pytest

from supplymind.authentication.base.models import AuthenticationHeaders
from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)
from supplymind.connectors.api.models import HttpResponse
from supplymind.connectors.api.protocols import HttpClientProtocol
from supplymind.connectors.sharepoint.connector import SharePointConnector
from supplymind.connectors.sharepoint.models import (
    SharePointConnectorConfiguration,
    SharePointDrive,
    SharePointDriveItem,
    SharePointSite,
)
from supplymind.connectors.sharepoint.exceptions import (
    SharePointAuthenticationException,
    SharePointSiteNotFoundException,
    SharePointAuthorizationException,
)


def test_sharepoint_connector_initialization() -> None:
    http_client = Mock(spec=HttpClientProtocol)

    authentication_provider = Mock(
        spec=AuthenticationProviderProtocol,
    )

    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    connector = SharePointConnector(
        http_client=http_client,
        authentication_provider=authentication_provider,
        configuration=configuration,
    )

    assert isinstance(connector, SharePointConnector)


@pytest.mark.anyio
async def test_get_site_returns_sharepoint_site() -> None:
    authentication_provider = Mock(
        spec=AuthenticationProviderProtocol,
    )
    authentication_provider.get_headers = AsyncMock(
        return_value=AuthenticationHeaders(
            {
                "Authorization": "Bearer test-token",
            }
        )
    )

    http_client = Mock(spec=HttpClientProtocol)
    http_client.get = AsyncMock(
        return_value=HttpResponse(
            status_code=200,
            headers={
                "content-type": "application/json",
            },
            content={
                "id": "site-id",
                "name": "Quality Analytics",
                "webUrl": ("https://contoso.sharepoint.com/sites/QualityAnalytics"),
            },
        )
    )

    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    connector = SharePointConnector(
        http_client=http_client,
        authentication_provider=authentication_provider,
        configuration=configuration,
    )

    site = await connector.get_site()

    assert site == SharePointSite(
        id="site-id",
        name="Quality Analytics",
        webUrl=("https://contoso.sharepoint.com/sites/QualityAnalytics"),
    )

    authentication_provider.get_headers.assert_awaited_once_with()

    http_client.get.assert_awaited_once_with(
        url=(
            "https://graph.microsoft.com/v1.0"
            "/sites/"
            "contoso.sharepoint.com:"
            "/sites/QualityAnalytics"
        ),
        headers={
            "Authorization": "Bearer test-token",
        },
    )


@pytest.mark.anyio
async def test_get_site_raises_when_site_is_not_found() -> None:
    authentication_provider = Mock(
        spec=AuthenticationProviderProtocol,
    )
    authentication_provider.get_headers = AsyncMock(
        return_value=AuthenticationHeaders(
            {
                "Authorization": "Bearer test-token",
            }
        )
    )

    http_client = Mock(spec=HttpClientProtocol)
    http_client.get = AsyncMock(
        return_value=HttpResponse(
            status_code=404,
            headers={
                "content-type": "application/json",
            },
            content={
                "error": {
                    "code": "itemNotFound",
                    "message": "The requested site was not found.",
                }
            },
        )
    )

    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/MissingSite",
    )

    connector = SharePointConnector(
        http_client=http_client,
        authentication_provider=authentication_provider,
        configuration=configuration,
    )

    with pytest.raises(SharePointSiteNotFoundException):
        await connector.get_site()

    authentication_provider.get_headers.assert_awaited_once_with()

    http_client.get.assert_awaited_once_with(
        url=(
            "https://graph.microsoft.com/v1.0"
            "/sites/"
            "contoso.sharepoint.com:"
            "/sites/MissingSite"
        ),
        headers={
            "Authorization": "Bearer test-token",
        },
    )


@pytest.mark.anyio
async def test_get_site_raises_when_authentication_fails() -> None:
    authentication_provider = Mock(
        spec=AuthenticationProviderProtocol,
    )
    authentication_provider.get_headers = AsyncMock(
        return_value=AuthenticationHeaders(
            {
                "Authorization": "Bearer test-token",
            }
        )
    )

    http_client = Mock(spec=HttpClientProtocol)
    http_client.get = AsyncMock(
        return_value=HttpResponse(
            status_code=401,
            headers={
                "content-type": "application/json",
            },
            content={
                "error": {
                    "code": "InvalidAuthenticationToken",
                    "message": "Access token is invalid.",
                }
            },
        )
    )

    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    connector = SharePointConnector(
        http_client=http_client,
        authentication_provider=authentication_provider,
        configuration=configuration,
    )

    with pytest.raises(SharePointAuthenticationException):
        await connector.get_site()

    authentication_provider.get_headers.assert_awaited_once_with()

    http_client.get.assert_awaited_once_with(
        url=(
            "https://graph.microsoft.com/v1.0"
            "/sites/"
            "contoso.sharepoint.com:"
            "/sites/QualityAnalytics"
        ),
        headers={
            "Authorization": "Bearer test-token",
        },
    )


@pytest.mark.anyio
async def test_get_site_raises_when_authorization_fails() -> None:
    authentication_provider = Mock(
        spec=AuthenticationProviderProtocol,
    )
    authentication_provider.get_headers = AsyncMock(
        return_value=AuthenticationHeaders(
            {
                "Authorization": "Bearer test-token",
            }
        )
    )

    http_client = Mock(spec=HttpClientProtocol)
    http_client.get = AsyncMock(
        return_value=HttpResponse(
            status_code=403,
            headers={
                "content-type": "application/json",
            },
            content={
                "error": {
                    "code": "accessDenied",
                    "message": ("Access denied."),
                }
            },
        )
    )

    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    connector = SharePointConnector(
        http_client=http_client,
        authentication_provider=authentication_provider,
        configuration=configuration,
    )

    with pytest.raises(SharePointAuthorizationException):
        await connector.get_site()

    authentication_provider.get_headers.assert_awaited_once_with()

    http_client.get.assert_awaited_once_with(
        url=(
            "https://graph.microsoft.com/v1.0"
            "/sites/"
            "contoso.sharepoint.com:"
            "/sites/QualityAnalytics"
        ),
        headers={
            "Authorization": "Bearer test-token",
        },
    )


@pytest.mark.anyio
async def test_get_default_drive_returns_sharepoint_drive() -> None:
    authentication_provider = Mock(
        spec=AuthenticationProviderProtocol,
    )

    authentication_provider.get_headers = AsyncMock(
        return_value=AuthenticationHeaders(
            {
                "Authorization": "Bearer test-token",
            }
        )
    )

    http_client = Mock(spec=HttpClientProtocol)

    http_client.get = AsyncMock(
        side_effect=[
            HttpResponse(
                status_code=200,
                headers={
                    "content-type": "application/json",
                },
                content={
                    "id": "site-id",
                    "name": "Quality Analytics",
                    "webUrl": ("https://contoso.sharepoint.com/sites/QualityAnalytics"),
                },
            ),
            HttpResponse(
                status_code=200,
                headers={
                    "content-type": "application/json",
                },
                content={
                    "id": "drive-id",
                    "name": "Documents",
                    "driveType": "documentLibrary",
                    "webUrl": (
                        "https://contoso.sharepoint.com/"
                        "sites/QualityAnalytics/Documents"
                    ),
                },
            ),
        ],
    )

    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    connector = SharePointConnector(
        http_client=http_client,
        authentication_provider=authentication_provider,
        configuration=configuration,
    )

    drive = await connector.get_default_drive()

    assert drive == SharePointDrive(
        id="drive-id",
        name="Documents",
        drive_type="documentLibrary",
        web_url=("https://contoso.sharepoint.com/sites/QualityAnalytics/Documents"),
    )


@pytest.mark.anyio
async def test_get_drive_items_returns_sharepoint_drive_items() -> None:
    authentication_provider = Mock(
        spec=AuthenticationProviderProtocol,
    )
    authentication_provider.get_headers = AsyncMock(
        return_value=AuthenticationHeaders(
            {
                "Authorization": "Bearer test-token",
            }
        )
    )

    http_client = Mock(spec=HttpClientProtocol)
    http_client.get = AsyncMock(
        side_effect=[
            HttpResponse(
                status_code=200,
                headers={
                    "content-type": "application/json",
                },
                content={
                    "id": "site-id",
                    "name": "Quality Analytics",
                    "webUrl": ("https://contoso.sharepoint.com/sites/QualityAnalytics"),
                },
            ),
            HttpResponse(
                status_code=200,
                headers={
                    "content-type": "application/json",
                },
                content={
                    "id": "drive-id",
                    "name": "Documents",
                    "driveType": "documentLibrary",
                    "webUrl": (
                        "https://contoso.sharepoint.com/"
                        "sites/QualityAnalytics/Documents"
                    ),
                },
            ),
            HttpResponse(
                status_code=200,
                headers={
                    "content-type": "application/json",
                },
                content={
                    "value": [
                        {
                            "id": "folder-id",
                            "name": "Reports",
                            "webUrl": (
                                "https://contoso.sharepoint.com/"
                                "sites/QualityAnalytics/"
                                "Shared Documents/Reports"
                            ),
                            "is_folder": True,
                        },
                        {
                            "id": "file-id",
                            "name": "employees.xlsx",
                            "webUrl": (
                                "https://contoso.sharepoint.com/"
                                "sites/QualityAnalytics/"
                                "Shared Documents/employees.xlsx"
                            ),
                            "is_folder": False,
                        },
                    ]
                },
            ),
        ]
    )

    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    connector = SharePointConnector(
        http_client=http_client,
        authentication_provider=authentication_provider,
        configuration=configuration,
    )

    items = await connector.get_drive_items()

    assert items == [
        SharePointDriveItem(
            id="folder-id",
            name="Reports",
            web_url=(
                "https://contoso.sharepoint.com/"
                "sites/QualityAnalytics/"
                "Shared Documents/Reports"
            ),
            is_folder=True,
        ),
        SharePointDriveItem(
            id="file-id",
            name="employees.xlsx",
            web_url=(
                "https://contoso.sharepoint.com/"
                "sites/QualityAnalytics/"
                "Shared Documents/employees.xlsx"
            ),
            is_folder=False,
        ),
    ]

    assert http_client.get.await_count == 3


@pytest.mark.anyio
async def test_download_file_returns_bytes() -> None:
    authentication_provider = Mock(
        spec=AuthenticationProviderProtocol,
    )
    authentication_provider.get_headers = AsyncMock(
        return_value=AuthenticationHeaders(
            {
                "Authorization": "Bearer test-token",
            }
        )
    )

    http_client = Mock(spec=HttpClientProtocol)
    http_client.get = AsyncMock(
        side_effect=[
            HttpResponse(
                status_code=200,
                headers={
                    "content-type": "application/json",
                },
                content={
                    "id": "site-id",
                    "name": "Quality Analytics",
                    "webUrl": ("https://contoso.sharepoint.com/sites/QualityAnalytics"),
                },
            ),
            HttpResponse(
                status_code=200,
                headers={
                    "content-type": "application/json",
                },
                content={
                    "id": "drive-id",
                    "name": "Documents",
                    "driveType": "documentLibrary",
                    "webUrl": (
                        "https://contoso.sharepoint.com/"
                        "sites/QualityAnalytics/Documents"
                    ),
                },
            ),
            HttpResponse(
                status_code=200,
                headers={
                    "content-type": (
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                },
                content=b"fake-excel-content",
            ),
        ]
    )

    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    connector = SharePointConnector(
        http_client=http_client,
        authentication_provider=authentication_provider,
        configuration=configuration,
    )

    content = await connector.download_file(
        item_id="item-id",
    )

    assert content == b"fake-excel-content"

    assert http_client.get.await_count == 3
