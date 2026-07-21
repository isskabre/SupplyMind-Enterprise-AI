"""
SupplyMind Enterprise AI

Connector Exceptions

Defines the shared exception hierarchy for enterprise connectors.
"""

from typing import Any

from supplymind.core.errors.codes import ErrorCode
from supplymind.core.errors.exceptions import SupplyMindException


class ConnectorException(SupplyMindException):
    """
    Base exception for all connector-related failures.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
        code: ErrorCode = ErrorCode.CONNECTOR_ERROR,
    ) -> None:
        super().__init__(
            code=code,
            message=message,
            details=details,
        )


class ConnectorAuthenticationException(ConnectorException):
    """
    Raised when a connector cannot authenticate with an external system.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.CONNECTOR_AUTHENTICATION_ERROR,
            message=message,
            details=details,
        )


class ConnectorAuthorizationException(ConnectorException):
    """
    Raised when authenticated credentials lack required permissions.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.CONNECTOR_AUTHORIZATION_ERROR,
            message=message,
            details=details,
        )


class ConnectorTimeoutException(ConnectorException):
    """
    Raised when communication with an external system times out.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.CONNECTOR_TIMEOUT_ERROR,
            message=message,
            details=details,
        )


class ConnectorRateLimitException(ConnectorException):
    """
    Raised when an external system rejects requests because of rate limits.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.CONNECTOR_RATE_LIMIT_ERROR,
            message=message,
            details=details,
        )


class ConnectorUnavailableException(ConnectorException):
    """
    Raised when an external system is unavailable or unreachable.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.CONNECTOR_UNAVAILABLE_ERROR,
            message=message,
            details=details,
        )


class ConnectorResponseException(ConnectorException):
    """
    Raised when an external system returns an invalid response.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.CONNECTOR_RESPONSE_ERROR,
            message=message,
            details=details,
        )
