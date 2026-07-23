from supplymind.connectors.sharepoint.models import (
    SharePointConnectorConfiguration,
)
from supplymind.connectors.sharepoint.urls import (
    SharePointUrls,
)


def test_build_site_url() -> None:
    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    assert SharePointUrls.site(configuration) == (
        "https://graph.microsoft.com/v1.0"
        "/sites/"
        "contoso.sharepoint.com:"
        "/sites/QualityAnalytics"
    )


def test_build_default_drive_url() -> None:
    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    assert (
        SharePointUrls.drive(
            configuration,
            "site-id",
        )
        == "https://graph.microsoft.com/v1.0/sites/site-id/drive"
    )


def test_build_drive_items_url() -> None:
    """
    The URL builder should create the Microsoft Graph endpoint
    for retrieving the root drive items.
    """
    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    assert SharePointUrls.drive_items(
        configuration,
        "drive-id",
    ) == ("https://graph.microsoft.com/v1.0/drives/drive-id/root/children")


def test_build_download_file_url() -> None:
    """
    The URL builder should generate the Microsoft Graph endpoint
    for downloading a drive item.
    """
    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    url = SharePointUrls.download_file(
        configuration,
        drive_id="drive-id",
        item_id="item-id",
    )

    assert url == (
        "https://graph.microsoft.com/v1.0/drives/drive-id/items/item-id/content"
    )
