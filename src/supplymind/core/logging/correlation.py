"""
SupplyMind Enterprise AI

Correlation ID Utilities

Provides validation and generation of safe correlation identifiers.
"""

import re
from uuid import uuid4

from supplymind.core.logging.constants import (
    CORRELATION_ID_PATTERN,
    MAX_CORRELATION_ID_LENGTH,
)


def is_valid_correlation_id(value: str | None) -> bool:
    """
    Return whether a correlation ID is safe and valid.

    A valid correlation ID:
    - is not empty;
    - does not exceed the configured maximum length;
    - contains only approved characters.
    """
    if value is None:
        return False

    if not value:
        return False

    if len(value) > MAX_CORRELATION_ID_LENGTH:
        return False

    return re.fullmatch(CORRELATION_ID_PATTERN, value) is not None


def resolve_correlation_id(value: str | None) -> str:
    """
    Preserve a valid incoming correlation ID or generate a new UUID.
    """
    if is_valid_correlation_id(value):
        return value

    return str(uuid4())