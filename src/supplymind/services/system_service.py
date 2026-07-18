"""
SupplyMind Enterprise AI

System Service

Contains business logic related to system endpoints.
"""

from supplymind.core.metadata import build_application_metadata


class SystemService:
    """Business logic for system-related operations."""

    def get_root(self) -> dict[str, str]:
        """Return root application information."""
        metadata = build_application_metadata()

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
        metadata = build_application_metadata()

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
        return build_application_metadata().to_dict()