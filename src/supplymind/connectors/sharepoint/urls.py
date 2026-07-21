"""
SupplyMind Enterprise AI

SharePoint URL Builder

Builds Microsoft Graph endpoints used by the SharePoint connector.
"""

from supplymind.connectors.sharepoint.models import (
    SharePointConnectorConfiguration,
)


class SharePointUrls:
    """
    Factory for Microsoft Graph SharePoint URLs.
    """

    @staticmethod
    def site(
        configuration: SharePointConnectorConfiguration,
    ) -> str:
        """
        Build the Microsoft Graph endpoint used to retrieve
        a SharePoint site.
        """
        return (
            f"{configuration.base_url}"
            f"/sites/"
            f"{configuration.site_hostname}:"
            f"{configuration.site_path}"
        )
