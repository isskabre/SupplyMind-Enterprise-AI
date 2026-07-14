"""
SupplyMind Enterprise AI

Application Dependency Providers

Defines reusable FastAPI dependencies used to construct and provide
application services.
"""

from supplymind.services.system_service import SystemService


def get_system_service() -> SystemService:
    """
    Provide a SystemService instance.

    Returns:
        A configured SystemService instance.
    """
    return SystemService()