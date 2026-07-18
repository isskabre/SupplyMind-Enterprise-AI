"""
SupplyMind Enterprise AI

Enterprise Logging Configuration

Centralized logging configuration for the application.
"""

import logging

from supplymind.core.config import settings
from supplymind.core.logging.constants import (
    DEFAULT_DATE_FORMAT,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOGGER_NAME,
)
from supplymind.core.logging.filters import CorrelationIdFilter
from supplymind.core.logging.formatters import EnterpriseFormatter


_logging_configured = False


def configure_logging() -> None:
    """
    Configure the SupplyMind application logging system.

    The SupplyMind logger is isolated from the root logger so that
    external frameworks such as Uvicorn cannot replace or duplicate
    the application's logging handlers.

    Safe to call multiple times.
    """
    global _logging_configured

    if _logging_configured:
        return

    formatter = EnterpriseFormatter(
        fmt=DEFAULT_LOG_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT,
    )

    handler = logging.StreamHandler()
    handler.addFilter(CorrelationIdFilter())
    handler.setFormatter(formatter)

    supplymind_logger = logging.getLogger(DEFAULT_LOGGER_NAME)

    supplymind_logger.setLevel(settings.log_level)
    supplymind_logger.handlers.clear()
    supplymind_logger.addHandler(handler)

    # Prevent SupplyMind logs from also travelling to Uvicorn's root logger.
    supplymind_logger.propagate = False

    _logging_configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Return a named SupplyMind logger.
    """
    configure_logging()
    return logging.getLogger(name)