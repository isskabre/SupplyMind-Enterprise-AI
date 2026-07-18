"""
SupplyMind Enterprise AI

System Service

Contains business logic related to system endpoints.
"""

from collections.abc import Callable

from supplymind.core.metadata import (
    ApplicationMetadata,
    build_application_metadata,
)


MetadataProvider = Callable[[], ApplicationMetadata]


class SystemService:
    """Business logic for system-related operations."""

    def __init__(
        self,
        metadata_provider: MetadataProvider = build_application_metadata,
    ) -> None:
        """
        Initialize the system service.

        Args:
            metadata_provider:
                Callable that returns current application metadata.
        """
        self._metadata_provider = metadata_provider

    def get_root(self) -> dict[str, str]:
        """Return root application information."""
        metadata = self._metadata_provider()

        return {
            "application": metadata.application,
            "version": metadata.version,
            "status": "running",
        }

    def get_health(self) -> dict[str, str]:
        """
        Return the legacy application health response.

        Retained for backward compatibility.
        """
        return {
            "status": "healthy",
        }

    def get_version(self) -> dict[str, str]:
        """Return application version."""
        metadata = self._metadata_provider()

        return {
            "version": metadata.version,
        }

    def get_liveness(self) -> dict[str, bool]:
        """
        Return whether the application process is alive.

        This check intentionally avoids external dependencies.
        """
        return {
            "alive": True,
        }

    def get_readiness(self) -> dict[str, bool]:
        """
        Return whether the application can receive traffic.

        Dependency checks will be added in future implementations.
        """
        return {
            "ready": True,
        }

    def get_system_info(self) -> dict[str, str | float | None]:
        """
        Return operational metadata for the running application.
        """
        return self._metadata_provider().to_dict()