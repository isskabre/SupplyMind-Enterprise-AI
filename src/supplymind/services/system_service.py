"""
SupplyMind Enterprise AI

System Service

Contains business logic related to system endpoints.
"""

from supplymind import __version__


class SystemService:
    """Business logic for system-related operations."""

    def get_root(self) -> dict[str, str]:
        """Return root application information."""
        return {
            "application": "SupplyMind Enterprise AI",
            "version": __version__,
            "status": "running",
        }

    def get_health(self) -> dict[str, str]:
        """Return application health."""
        return {
            "status": "healthy",
        }

    def get_version(self) -> dict[str, str]:
        """Return application version."""
        return {
            "version": __version__,
        }