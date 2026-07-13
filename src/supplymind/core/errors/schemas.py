"""
SupplyMind Enterprise AI

Enterprise Error Response Schemas

Defines standardized error response models used throughout
the platform.
"""

from typing import Any

from pydantic import BaseModel, Field

from supplymind.core.errors.codes import ErrorCode


class ErrorDetails(BaseModel):
    """Standardized error information."""

    code: ErrorCode = Field(
        ...,
        description="Application-specific error code.",
    )

    message: str = Field(
        ...,
        description="Human-readable error message.",
    )

    details: Any | None = Field(
        default=None,
        description="Optional additional error details.",
    )


class ErrorResponse(BaseModel):
    """Enterprise API error response."""

    success: bool = Field(
        default=False,
        description="Indicates the request failed.",
    )

    error: ErrorDetails

    meta: dict[str, Any] | None = Field(
        default=None,
        description="Optional response metadata.",
    )