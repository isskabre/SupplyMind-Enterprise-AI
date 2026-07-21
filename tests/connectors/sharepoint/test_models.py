"""
Tests for SharePoint connector models.
"""

import pytest
from pydantic import ValidationError

from supplymind.connectors.sharepoint.models import (
    SharePointConnectorConfiguration,
    SharePointSite,
)


def test_sharepoint_connector_configuration_with_valid_values() -> None:
    """
    The configuration should store the supplied SharePoint settings
    and use the default Microsoft Graph base URL.
    """
    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    assert configuration.base_url == "https://graph.microsoft.com/v1.0"
    assert configuration.site_hostname == "contoso.sharepoint.com"
    assert configuration.site_path == "/sites/QualityAnalytics"


def test_sharepoint_connector_configuration_requires_site_information() -> None:
    """
    The configuration should reject missing required fields.
    """
    with pytest.raises(ValidationError):
        SharePointConnectorConfiguration()


def test_sharepoint_connector_configuration_rejects_extra_fields() -> None:
    """
    The configuration should reject unsupported configuration fields.
    """
    with pytest.raises(ValidationError):
        SharePointConnectorConfiguration(
            site_hostname="contoso.sharepoint.com",
            site_path="/sites/QualityAnalytics",
            unexpected="value",
        )


def test_sharepoint_connector_configuration_is_immutable() -> None:
    """
    The configuration should not allow values to be changed after creation.
    """
    configuration = SharePointConnectorConfiguration(
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/QualityAnalytics",
    )

    with pytest.raises(ValidationError):
        configuration.site_path = "/sites/NewSite"


def test_sharepoint_site_parses_graph_response() -> None:
    """
    The model should convert a Microsoft Graph response into
    a typed SharePoint site object.
    """
    graph_response = {
        "id": "site-id",
        "name": "Quality Analytics",
        "webUrl": ("https://contoso.sharepoint.com/sites/QualityAnalytics"),
    }

    site = SharePointSite.model_validate(graph_response)

    assert site.id == "site-id"
    assert site.name == "Quality Analytics"
    assert site.web_url == "https://contoso.sharepoint.com/sites/QualityAnalytics"


def test_sharepoint_site_ignores_extra_graph_fields() -> None:
    """
    The model should ignore Microsoft Graph fields that SupplyMind
    does not currently use.
    """
    graph_response = {
        "id": "site-id",
        "name": "Quality Analytics",
        "webUrl": ("https://contoso.sharepoint.com/sites/QualityAnalytics"),
        "displayName": "Quality Analytics Site",
        "createdDateTime": "2026-07-20T12:00:00Z",
        "unusedField": "ignored",
    }

    site = SharePointSite.model_validate(graph_response)

    assert site.id == "site-id"
    assert site.name == "Quality Analytics"
    assert site.web_url == "https://contoso.sharepoint.com/sites/QualityAnalytics"
