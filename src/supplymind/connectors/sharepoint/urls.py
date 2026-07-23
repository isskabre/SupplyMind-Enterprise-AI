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

    @staticmethod
    def drive_items(
        configuration: SharePointConnectorConfiguration,
        drive_id: str,
    ) -> str:
        """
        Build the Microsoft Graph endpoint for retrieving
        the root items of a SharePoint drive.

        Args:
            configuration:
                SharePoint connector configuration.

            drive_id:
                Microsoft Graph identifier of the drive.

        Returns:
            URL for retrieving the drive's root items.
        """
        return f"{configuration.base_url}/drives/{drive_id}/root/children"

    @staticmethod
    def download_file(
        configuration: SharePointConnectorConfiguration,
        drive_id: str,
        item_id: str,
    ) -> str:
        """
        Build the Microsoft Graph endpoint for downloading a drive item.

        Args:
            configuration:
                SharePoint connector configuration.

            drive_id:
                Microsoft Graph identifier of the drive.

            item_id:
                Microsoft Graph identifier of the drive item.

        Returns:
            URL for downloading the drive item's binary content.
        """
        return f"{configuration.base_url}/drives/{drive_id}/items/{item_id}/content"
