"""
SupplyMind Enterprise AI

Dependency Provider Package
"""

from supplymind.core.dependencies.http import get_http_client
from supplymind.core.dependencies.metadata import (
    get_application_metadata,
)
from supplymind.core.dependencies.system import get_system_service

__all__ = [
    "get_application_metadata",
    "get_http_client",
    "get_system_service",
]