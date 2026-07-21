"""
SupplyMind Enterprise AI

Authentication Exceptions

Defines the shared exception hierarchy for authentication providers.
"""

from typing import Any

from supplymind.core.errors.codes import ErrorCode
from supplymind.core.errors.exceptions import SupplyMindException


class AuthenticationException(SupplyMindException):
    """
    Base exception for authentication-provider failures.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
        code: ErrorCode = ErrorCode.AUTHENTICATION_PROVIDER_ERROR,
    ) -> None:
        super().__init__(
            code=code,
            message=message,
            details=details,
        )


class AuthenticationConfigurationException(AuthenticationException):
    """
    Raised when an authentication provider is configured incorrectly.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.AUTHENTICATION_CONFIGURATION_ERROR,
            message=message,
            details=details,
        )


class CredentialUnavailableException(AuthenticationException):
    """
    Raised when required credentials cannot be obtained.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.CREDENTIAL_UNAVAILABLE_ERROR,
            message=message,
            details=details,
        )


class TokenAcquisitionException(AuthenticationException):
    """
    Raised when an access token cannot be acquired.
    """

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            code=ErrorCode.TOKEN_ACQUISITION_ERROR,
            message=message,
            details=details,
        )
