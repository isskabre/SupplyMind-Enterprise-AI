"""
SupplyMind Enterprise AI

Enterprise Logging Filters

Injects request-scoped context into log records.
"""

import logging

from supplymind.core.logging.context import correlation_id


class CorrelationIdFilter(logging.Filter):
    """
    Add the current correlation ID to every log record.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id.get()
        return True