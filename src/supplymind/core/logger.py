import logging

from supplymind.core.config import settings
from supplymind.core.constants import DEFAULT_LOG_FORMAT

_logging_configured = False


def configure_logging() -> None:
    """
    Configure the application's logging system.
    """
    global _logging_configured

    if _logging_configured:
        return

    logging.basicConfig(
        level=settings.log_level,
        format=DEFAULT_LOG_FORMAT,
    )

    _logging_configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger.
    """
    return logging.getLogger(name)