from supplymind.connectors.sharepoint.exceptions import (
    SharePointAuthenticationException,
    SharePointAuthorizationException,
    SharePointConnectorException,
    SharePointRateLimitException,
    SharePointServiceException,
    SharePointSiteNotFoundException,
)


def test_sharepoint_exceptions_inherit_from_connector_exception() -> None:
    exception_types = (
        SharePointAuthenticationException,
        SharePointAuthorizationException,
        SharePointSiteNotFoundException,
        SharePointRateLimitException,
        SharePointServiceException,
    )

    for exception_type in exception_types:
        assert issubclass(
            exception_type,
            SharePointConnectorException,
        )