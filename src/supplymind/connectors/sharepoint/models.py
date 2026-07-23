"""
SupplyMind Enterprise AI

SharePoint Connector Models

Defines configuration and data models used by the SharePoint connector.
"""

from pydantic import BaseModel, ConfigDict, Field


class SharePointConnectorConfiguration(BaseModel):
    """
    Configuration required by the SharePoint connector.

    Attributes:
        base_url:
            Base URL for the Microsoft Graph API.

        site_hostname:
            SharePoint tenant hostname, such as
            ``contoso.sharepoint.com``.

        site_path:
            Server-relative path of the SharePoint site, such as
            ``/sites/QualityAnalytics``.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    base_url: str = Field(
        default="https://graph.microsoft.com/v1.0",
        min_length=1,
    )

    site_hostname: str = Field(
        min_length=1,
    )

    site_path: str = Field(
        min_length=1,
    )


class SharePointSite(BaseModel):
    """
    Represents a SharePoint site.

    Attributes:
        id:
            Microsoft Graph identifier of the site.

        name:
            Display name of the SharePoint site.

        web_url:
            URL used to open the site in a browser.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="ignore",
    )

    id: str

    name: str

    web_url: str = Field(
        alias="webUrl",
    )


class SharePointDrive(BaseModel):
    """
    Represents a SharePoint document library exposed as a Microsoft Graph drive.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="ignore",
        populate_by_name=True,
    )

    id: str
    name: str

    drive_type: str = Field(
        alias="driveType",
    )

    web_url: str = Field(
        alias="webUrl",
    )


class SharePointDriveItem(BaseModel):
    """
    Represents a file or folder stored in a SharePoint document library.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="ignore",
        populate_by_name=True,
    )

    id: str

    name: str

    web_url: str = Field(
        alias="webUrl",
    )

    is_folder: bool
