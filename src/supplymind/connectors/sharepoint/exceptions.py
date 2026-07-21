"""
SupplyMind Enterprise AI

SharePoint Connector Exceptions

Defines failures raised by the SharePoint connector.
"""


class SharePointConnectorException(Exception):
    """
    Base exception for SharePoint connector failures.
    """


class SharePointSiteNotFoundException(SharePointConnectorException):
    """
    Raised when the configured SharePoint site cannot be found.
    """
