"""
SupplyMind Enterprise AI

Enterprise Exception Hierarchy

Defines the application's custom exception hierarchy.
"""

from typing import Any

from supplymind.core.errors.codes import ErrorCode


class SupplyMindException(Exception):
    """
    Base exception for all SupplyMind application errors.
    """

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        details: Any | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.details = details

        super().__init__(message)


class ValidationException(SupplyMindException):
    """Raised when business validation fails."""

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.VALIDATION_ERROR,
            message=message,
            details=details,
        )


class NotFoundException(SupplyMindException):
    """Raised when a requested resource does not exist."""

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.RESOURCE_NOT_FOUND,
            message=message,
            details=details,
        )


class ConflictException(SupplyMindException):
    """Raised when a resource already exists."""

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.RESOURCE_ALREADY_EXISTS,
            message=message,
            details=details,
        )


class AuthorizationException(SupplyMindException):
    """Raised when authorization fails."""

    def __init__(
        self,
        message: str = "Access denied.",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.FORBIDDEN,
            message=message,
            details=details,
        )


class DatabaseException(SupplyMindException):
    """Raised when a database operation fails."""

    def __init__(
        self,
        message: str = "Database operation failed.",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.DATABASE_ERROR,
            message=message,
            details=details,
        )


class ConfigurationException(SupplyMindException):
    """Raised when application configuration is invalid."""

    def __init__(
        self,
        message: str = "Application configuration is invalid.",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.CONFIGURATION_ERROR,
            message=message,
            details=details,
        )


class ConnectorException(SupplyMindException):
    """Raised when an external connector fails."""

    def __init__(
        self,
        message: str = "Connector operation failed.",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.CONNECTOR_ERROR,
            message=message,
            details=details,
        )


class AIProviderException(SupplyMindException):
    """Raised when an AI provider returns an error."""

    def __init__(
        self,
        message: str = "AI provider operation failed.",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.AI_PROVIDER_ERROR,
            message=message,
            details=details,
        )