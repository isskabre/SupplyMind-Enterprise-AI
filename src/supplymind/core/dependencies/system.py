"""
SupplyMind Enterprise AI

System Service Dependency Providers

Constructs system-related application services.
"""

from fastapi import Depends

from supplymind.core.dependencies.metadata import (
    get_application_metadata,
)
from supplymind.core.metadata import ApplicationMetadata
from supplymind.services.system_service import SystemService


def get_system_service(
    metadata: ApplicationMetadata = Depends(
        get_application_metadata,
    ),
) -> SystemService:
    """
    Provide a configured SystemService instance.
    """
    return SystemService(
        metadata_provider=lambda: metadata,
    )