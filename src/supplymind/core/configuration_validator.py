"""
SupplyMind Enterprise AI

Application Configuration Validation

Defines application-level configuration policies that must be
satisfied before the platform starts accepting requests.
"""

from supplymind.core.config import Settings
from supplymind.core.errors.exceptions import ConfigurationException


def validate_configuration(settings: Settings) -> None:
    """
    Validate application-wide configuration policies.

    Args:
        settings: The resolved application settings.

    Raises:
        ConfigurationException: If one or more configuration rules fail.
    """

    errors: list[str] = []

    if not settings.app_name.strip():
        errors.append("app_name must not be empty.")

    if not settings.app_version.strip():
        errors.append("app_version must not be empty.")

    if settings.is_production and settings.debug:
        errors.append(
            "debug must be disabled when running in production."
        )

    if errors:
        raise ConfigurationException(
            message="Application configuration validation failed.",
            details={"errors": errors},
        )