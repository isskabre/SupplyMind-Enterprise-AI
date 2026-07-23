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

    @staticmethod
    def drive(
        configuration: SharePointConnectorConfiguration,
        site_id: str,
    ) -> str:
        """
        Build the Microsoft Graph endpoint for a site's default drive.
        """
        return f"{configuration.base_url}/sites/{site_id}/drive"
