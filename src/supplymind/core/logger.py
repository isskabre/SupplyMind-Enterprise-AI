"""
SupplyMind Enterprise AI

Enterprise Logger Compatibility Layer

This module exists for backward compatibility.

The actual logging implementation resides in:

    supplymind.core.logging.config

Future implementations should import directly from
`supplymind.core.logging`.
"""

from supplymind.core.logging.config import (
    configure_logging,
    get_logger,
)

__all__ = [
    "configure_logging",
    "get_logger",
]