"""
SupplyMind Enterprise AI

Enterprise Error Codes

This module defines standardized application error codes used
throughout the SupplyMind platform.

Using centralized error codes ensures:

- Consistent API responses
- Easier client-side error handling
- Stable integrations
- Cleaner logging
- Future localization support
"""

from enum import StrEnum


class ErrorCode(StrEnum):
    """Enterprise application error codes."""

    # Generic

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    BAD_REQUEST = "BAD_REQUEST"

    # Resources

    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"

    # Authentication / Authorization

    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"

    # Infrastructure

    DATABASE_ERROR = "DATABASE_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"


    # External Systems

    CONNECTOR_ERROR = "CONNECTOR_ERROR"

    CONNECTOR_AUTHENTICATION_ERROR = (
        "CONNECTOR_AUTHENTICATION_ERROR"
    )

    CONNECTOR_AUTHORIZATION_ERROR = (
        "CONNECTOR_AUTHORIZATION_ERROR"
    )

    CONNECTOR_TIMEOUT_ERROR = (
        "CONNECTOR_TIMEOUT_ERROR"
    )

    CONNECTOR_RATE_LIMIT_ERROR = (
        "CONNECTOR_RATE_LIMIT_ERROR"
    )

    CONNECTOR_UNAVAILABLE_ERROR = (
        "CONNECTOR_UNAVAILABLE_ERROR"
    )

    CONNECTOR_RESPONSE_ERROR = (
        "CONNECTOR_RESPONSE_ERROR"
    )

    # AI Services

    AI_PROVIDER_ERROR = "AI_PROVIDER_ERROR"