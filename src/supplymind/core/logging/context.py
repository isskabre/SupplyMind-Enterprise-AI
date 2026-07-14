"""
SupplyMind Enterprise AI

Logging Context

Provides request-scoped logging context.
"""

from contextvars import ContextVar

correlation_id: ContextVar[str] = ContextVar(
    "correlation_id",
    default="-",
)