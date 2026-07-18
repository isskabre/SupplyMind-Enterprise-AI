"""
SupplyMind Enterprise AI

Enterprise Logging Constants

Central location for logging-related constants.

Keeping these values in one place ensures consistency across the
entire logging infrastructure and simplifies future maintenance.
"""

CORRELATION_ID_HEADER = "X-Correlation-ID"

MAX_CORRELATION_ID_LENGTH = 128

CORRELATION_ID_PATTERN = r"^[A-Za-z0-9._-]+$"

DEFAULT_LOGGER_NAME = "supplymind"

DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

DEFAULT_LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "[%(correlation_id)s] | "
    "%(name)s | "
    "%(message)s"
)