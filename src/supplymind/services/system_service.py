"""
SupplyMind Enterprise AI

System Service

Contains business logic related to system endpoints.
"""

import platform

from supplymind import __version__
from supplymind.core.config import settings
from supplymind.core.runtime import get_uptime_seconds


class SystemService:
    """Business logic for system-related operations."""

    def get_root(self) -> dict[str, str]:
        """Return root application information."""
        return {
            "application": settings.app_name,
            "version": __version__,
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
        return {
            "version": __version__,
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

    def get_system_info(self) -> dict[str, str | float]:
        """
        Return operational metadata for the running application.
        """
        return {
            "application": settings.app_name,
            "version": __version__,
            "environment": settings.environment.value,
            "uptime_seconds": get_uptime_seconds(),
            "python_version": platform.python_version(),
        }