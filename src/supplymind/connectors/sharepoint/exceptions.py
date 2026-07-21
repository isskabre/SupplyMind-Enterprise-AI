"""
SupplyMind Enterprise AI

SharePoint Connector Exceptions

Defines failures raised by the SharePoint connector.
"""


class SharePointConnectorException(Exception):
    """
    Base exception for all SharePoint connector failures.
    """


class SharePointAuthenticationException(SharePointConnectorException):
    """
    Raised when SharePoint authentication fails.

    This commonly represents an invalid, missing, or expired access token.
    """


class SharePointAuthorizationException(SharePointConnectorException):
    """
    Raised when the authenticated identity lacks required permissions.
    """


class SharePointSiteNotFoundException(SharePointConnectorException):
    """
    Raised when the configured SharePoint site cannot be found.
    """


class SharePointRateLimitException(SharePointConnectorException):
    """
    Raised when Microsoft Graph rate-limits a SharePoint request.
    """


class SharePointServiceException(SharePointConnectorException):
    """
    Raised when Microsoft Graph or SharePoint experiences a server failure.
    """