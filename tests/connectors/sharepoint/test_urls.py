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
