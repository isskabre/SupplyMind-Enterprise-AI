"""
SupplyMind Enterprise AI

Enterprise Logging Formatters
"""

import logging


class EnterpriseFormatter(logging.Formatter):
    """
    Standard formatter for SupplyMind logs.

    This formatter serves as the foundation for future structured
    logging enhancements, including JSON output.
    """

    def __init__(
        self,
        fmt: str,
        datefmt: str | None = None,
    ) -> None:
        super().__init__(
            fmt=fmt,
            datefmt=datefmt,
        )