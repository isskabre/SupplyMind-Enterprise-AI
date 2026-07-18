"""
SupplyMind Enterprise AI

Metadata Dependency Providers

Defines reusable providers for application metadata.
"""

from supplymind.core.metadata import (
    ApplicationMetadata,
    build_application_metadata,
)


def get_application_metadata() -> ApplicationMetadata:
    """
    Provide current application metadata.
    """
    return build_application_metadata()